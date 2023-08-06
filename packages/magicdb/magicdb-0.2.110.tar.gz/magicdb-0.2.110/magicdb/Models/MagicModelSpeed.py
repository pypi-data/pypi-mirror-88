from __future__ import annotations
from typing import List, Dict, Any, ClassVar
from datetime import datetime
import time
from copy import deepcopy
import json
import os
import pprint
import uuid
from glom import glom

from magicdb.Timing.decorator import timing


from pydantic import BaseModel, Field, PrivateAttr
from pydantic.main import ModelMetaclass

import magicdb
from magicdb.Queries import QuerySpeed
from magicdb.utils.Serverless.span import safe_span

from magicdb.utils.updating_objects import make_update_obj
from magicdb.utils.async_helpers import magic_async

from magicdb.Models.magic_fields_maker import FieldMaker

from magicdb.Models.MagicCache import MagicCache


class DatabaseError(Exception):
    def __init__(self, key):
        self.message = (
            f"There is no document with key {key} to update. Add update.(create=True) to save the document"
            f" if it does not exist. Otherwise, you can save the document: save()."
        )


class QueryMeta(type):
    """https://stackoverflow.com/questions/128573/using-property-on-classmethods"""

    @property
    def collection(cls) -> QuerySpeed:
        return QuerySpeed(cls)

    @property
    def collection_group(cls) -> QuerySpeed:
        return QuerySpeed(cls).collection_group()


class QueryAndBaseMetaClasses(ModelMetaclass, QueryMeta):
    pass


class MagicModelSpeed(BaseModel, metaclass=QueryAndBaseMetaClasses):
    """
    When this gets inited, if given an id or key, assign based on that.
    Otherwise, assign them based on what Firestore gives it
    """

    id: str = Field(default_factory=uuid.uuid4)
    _key: str = PrivateAttr(None)
    _ref: magicdb.DocumentReference = PrivateAttr(None)
    _doc: magicdb.DocumentSnapshot = PrivateAttr(None)
    _parent: MagicModelSpeed = PrivateAttr(None)
    _data_from_db: dict = PrivateAttr(None)

    __call__ = ...  # to satisfy Query python linter

    @timing
    def __init__(self, from_db: bool = False, **data):
        data_from_db = deepcopy(data)
        super().__init__(**data)

        FieldMaker(
            **data, _collection_name=self.get_collection_name()
        ).set_model_fields(self)

        self._data_from_db = {} if not from_db else data_from_db

    @classmethod
    @timing
    def construct(cls, from_db: bool = False, **data):
        data_from_db = deepcopy(data)
        new_obj = super().construct(**data)

        FieldMaker(
            **data, _collection_name=new_obj.get_collection_name()
        ).set_model_fields(new_obj)

        new_obj._data_from_db = {} if not from_db else data_from_db
        return new_obj

    """GETTING AND SETTING FIELDS"""

    def set_id(self, id: str):
        FieldMaker(
            id=id, _parent=self._parent, _collection_name=self.get_collection_name()
        ).set_model_fields(self)

    def set_key(self, key: str):
        FieldMaker(
            _key=key, _collection_name=self.get_collection_name()
        ).set_model_fields(self)

    def set_ref(self, ref: magicdb.DocumentReference):
        FieldMaker(
            _ref=ref, _collection_name=self.get_collection_name()
        ).set_model_fields(self)

    def set_parent(self, parent: MagicModelSpeed):
        FieldMaker(
            _parent=parent, id=self.id, _collection_name=self.get_collection_name()
        ).set_model_fields(self)

    """PRINTING AND RETURNING"""

    def __repr__(self, *args, **kwargs):
        return f"{self.__class__.__name__}({self.__repr_str__(', ')})"

    def __str__(self, *args, **kwargs):
        return f"{self.__repr_str__(' ')}"

    def __repr_str__(self, join_str=", "):
        key_values: List[str] = []
        for field, val in self.__dict__.items():
            key_values.append(f"{repr(field)}={repr(val)}")
        return join_str.join(key_values)

    def print_magic_fields(self, join_str=" "):
        key_values = []
        for field in ["id", *self.__private_attributes__.keys()]:
            key_values.append(f"{repr(field)}={repr(getattr(self, field, None))}")
        print(join_str.join(key_values))

    """META"""

    class Meta:
        """Init the meta class so you can use it and know it is there"""

        """Looks like having Meta in the TestModel actually overrites this one, not inherits it"""
        ...

    @property
    def collection_name(self) -> str:
        return self.get_collection_name()

    @classmethod
    def make_default_collection_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def get_collection_name(cls) -> str:
        return getattr(cls.Meta, "collection_name", cls.make_default_collection_name())

    """COMPARISONS"""

    def equal(self, model: BaseModel, path_to_compare=None):
        """The difference between objects will be firestore adds nanoseconds to the object. So parse those out"""
        replace_text = "+00:00"
        self_json = self.json().replace(replace_text, "")
        other_json = model.json().replace(replace_text, "")
        if path_to_compare:
            self_json = json.dumps(
                glom(json.loads(self_json), ".".join(path_to_compare))
            )
            other_json = json.dumps(
                glom(json.loads(other_json), ".".join(path_to_compare))
            )
        return self_json == other_json

    def been_updated(self, path_to_compare=None):
        from_db = self.__class__.get_with_error(self.id)
        return not self.equal(from_db, path_to_compare=path_to_compare)

    class Serverless:
        """Fills this with the latest context if it exists"""

        context = None

    class Config:
        anystr_strip_whitespace: bool = True
        arbitrary_types_allowed: bool = True
        json_encoders = {magicdb.DocumentReference: lambda doc_ref: doc_ref.path}

    """ ADDING TO FIRESTORE """

    def remove_magic_fields(self, og_d) -> dict:
        new_d = deepcopy(og_d)
        for field in self.__private_attributes__:
            if field in new_d:
                del new_d[field]
        if "id" in new_d:
            del new_d["id"]
        return new_d

    @timing
    def validate_all_fields(self):
        valid_obj_no_magic = self.__class__(**self.dict())
        self.__dict__.update(valid_obj_no_magic.__dict__)

    @magic_async
    @timing
    def save(self, batch=None, transaction=None, merge=False, ignore_fields=False):
        """Will create a new obj_to_save and save it so that all of the validation happens properly on a new obj."""
        batch_or_transaction = batch or transaction
        # make sure all the fields are correct by validating again
        if not ignore_fields:
            self.validate_all_fields()

        new_d = self.dict()
        new_d = self.remove_magic_fields(new_d)  # must remove id

        with safe_span(f"save-{self._key}", use=(batch_or_transaction is None)):
            if batch_or_transaction:
                res = batch_or_transaction.set(self._ref, new_d, merge=merge)
            else:
                res = self._ref.set(new_d, merge=merge)

        if not merge:
            self._data_from_db = deepcopy(new_d)

        # update self just in case
        return self

    @magic_async
    @timing
    def update(
        self,
        batch=None,
        transaction=None,
        create=False,
        ignore_fields=False,
        print_update_d=False,
        only_print_update_d=False,
    ):
        batch_or_transaction = batch or transaction
        if not ignore_fields:
            self.validate_all_fields()

        new_d = self.dict()
        new_d = self.remove_magic_fields(new_d)  # must remove id
        data_from_db = self.remove_magic_fields(self._data_from_db)

        if not data_from_db:
            update_d = new_d
        else:
            update_d = make_update_obj(original=data_from_db, new=new_d)

        if print_update_d or only_print_update_d:
            pprint.pprint({f"update_d_for_{self.id}": update_d})
        if only_print_update_d:
            return
        try:
            if update_d != {}:
                with safe_span(
                    f"update-{self._key}", use=(batch_or_transaction is None)
                ):
                    self._ref.update(
                        update_d
                    ) if not batch_or_transaction else batch_or_transaction.update(
                        self._ref, update_d
                    )
            else:
                print(f"update_d was empty so did not update for {self.id}.")
            return self
        except Exception as e:
            if hasattr(e, "message") and "no document to update" in e.message.lower():
                if create:
                    return self.save(batch=batch, transaction=transaction)
                else:
                    db_error = DatabaseError(self._key)
                    raise DatabaseError(db_error.message)
            raise e

    @magic_async
    @timing
    def delete(
        self,
        batch=None,
        transaction=None,
        print_update_d=False,
        only_print_update_d=False,
    ):
        if print_update_d or only_print_update_d:
            print(f"About to delete {self.id}.")
        if only_print_update_d:
            return

        batch_or_transaction = batch or transaction
        with safe_span(f"delete-{self._key}", use=(batch_or_transaction is None)):
            return (
                self._ref.delete()
                if not batch_or_transaction
                else batch_or_transaction.delete(self._ref)
            )

    """QUERYING AND COLLECTIONS"""

    def exists(self):
        return self.__class__.collection.get(self.id) is not None

    def get_subcollections(self):
        return list(self.__class__.collection.document(self.id).collections())

    @classmethod
    def get_ref(cls, id) -> magicdb.DocumentReference:
        temp_cls = cls.construct(id=id)
        return temp_cls._ref

    @classmethod
    def get_default_exception(cls):
        return getattr(cls.Meta, "default_exception", Exception)

    @classmethod
    @magic_async
    def get_with_error(
        cls,
        id,
        error=None,
        cache: MagicCache = None,
        **kwargs,
    ):
        if cache is not None:
            if val := cache.get(cls=cls, id=id):
                print("cache hit!")
                return val
        if not error:
            error = cls.get_default_exception()
        val = cls.collection.get(id, **kwargs)
        if not val:
            raise error(f"{cls.__name__} with id {id} does not exist.")
        if cache is not None:
            cache.add(cls=cls, id=id, val=val)
        return val

    """GETTING SUBCLASSES"""

    @classmethod
    def get_subclasses(cls):
        all_subs = []
        for sub in cls.__subclasses__():
            all_subs.append(sub)
            all_subs += sub.get_subclasses()
        return list(set(all_subs))

    @staticmethod
    def get_all_subclasses_of_model():
        all_subs = []
        for sub in list(MagicModelSpeed.__subclasses__()):
            all_subs.append(sub)
            all_subs += sub.get_subclasses()
        return list(set(all_subs))

    @classmethod
    @magic_async
    def get_by_field(cls, field_name: str, value):
        models = cls.collection.where(
            magicdb.db.conn.field_path(field_name), "==", value
        ).stream()
        return None if not models else models[0]

    @classmethod
    @magic_async
    def get_by_field_with_error(cls, field_name: str, value, error=None):
        if not error:
            error = cls.get_default_exception()
        model = cls.get_by_field(field_name=field_name, value=value)
        if not model:
            raise error(f"{cls.__name__} with {field_name} {value} does not exist.")
        return model
