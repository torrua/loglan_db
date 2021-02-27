# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains a basic Word Model and addons
"""

from __future__ import annotations

import os
from typing import List, Union

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import or_

from loglan_db import app_lod, db
from loglan_db.model_db import t_name_words, \
    t_name_types, t_name_events
from loglan_db.model_db.base_author import BaseAuthor
from loglan_db.model_db.base_connect_tables import \
    t_connect_authors, t_connect_words, t_connect_keys
from loglan_db.model_db.base_event import BaseEvent
from loglan_db.model_db.base_key import BaseKey
from loglan_db.model_db.base_type import BaseType
from loglan_db.model_init import InitBase, DBBase
from loglan_db.model_db.base_definition import BaseDefinition

if os.environ.get("IS_PDOC", "False") == "True":
    db = SQLAlchemy(app_lod())
    # TODO Fix pdoc

__pdoc__ = {
    'BaseWord.created': False, 'BaseWord.updated': False,
}


class AddonWordQuerier:

    id: int = None
    _derivatives: BaseQuery = None

    def query_derivatives(self, word_type: str = None,
                          word_type_x: str = None, word_group: str = None) -> BaseQuery:
        """Query to get all derivatives of the word, depending on its parameters

        Args:
          word_type: str:  (Default value = None)
          word_type_x: str:  (Default value = None)
          word_group: str:  (Default value = None)

        Returns:
            BaseQuery
        """
        result = self._derivatives.filter(self.id == t_connect_words.c.parent_id)

        if word_type or word_type_x or word_group:
            result = result.join(BaseType)

        if word_type:
            result = result.filter(BaseType.type == word_type)
        if word_type_x:
            result = result.filter(BaseType.type_x == word_type_x)
        if word_group:
            result = result.filter(BaseType.group == word_group)

        return result.order_by(BaseWord.name.asc())

    def query_cpx(self) -> BaseQuery:
        """Query to qet all the complexes that exist for this word
        Only primitives have affixes

        Args:

        Returns:
            BaseQuery
        """
        return self.query_derivatives(word_group="Cpx")

    def query_afx(self) -> BaseQuery:
        """Query to qet all the affixes that exist for this word
        Only primitives have affixes

        Args:

        Returns:
            BaseQuery
        """
        return self.query_derivatives(word_type="Afx")

    def query_keys(self) -> BaseQuery:
        """Query for the BaseKeys linked with this BaseWord

        Args:

        Returns:
            BaseQuery
        """
        return BaseKey.query.join(
            t_connect_keys, BaseDefinition, BaseWord).filter(BaseWord.id == self.id)


class AddonWordGetter:
    query: BaseQuery = None
    name: db.Column = None
    event_start_id: db.Column = None
    event_end_id: db.Column = None

    @classmethod
    def by_event(cls, event_id: Union[BaseEvent, int] = None) -> BaseQuery:
        """Query filtered by specified Event (latest by default)

        Args:
          event_id: Union[BaseEvent, int]: Event object or Event.id (int) (Default value = None)

        Returns:
          BaseQuery

        """
        if not event_id:
            event_id = BaseEvent.latest().id

        event_id = BaseEvent.id if isinstance(event_id, BaseEvent) else int(event_id)

        return cls.query.filter(cls.event_start_id <= event_id) \
            .filter(or_(cls.event_end_id > event_id, cls.event_end_id.is_(None))) \
            .order_by(cls.name)

    @classmethod
    def by_name(cls, name: str, case_sensitive: bool = False) -> BaseQuery:
        """Word.Query filtered by specified name

        Args:
          name: str:
          case_sensitive: bool:  (Default value = False)

        Returns:
          BaseQuery

        """
        if case_sensitive:
            return cls.query.filter(cls.name == name)
        return cls.query.filter(cls.name.in_([name, name.lower(), name.upper()]))

    @classmethod
    def by_key(
            cls, key: Union[BaseKey, str],
            language: str = None,
            case_sensitive: bool = False) -> BaseQuery:
        """Word.Query filtered by specified key

        Args:
          key: Union[BaseKey, str]:
          language: str: Language of key (Default value = None)
          case_sensitive: bool:  (Default value = False)

        Returns:
          BaseQuery

        """

        key = BaseKey.word if isinstance(key, BaseKey) else str(key)
        request = cls.query.join(BaseDefinition, t_connect_keys, BaseKey)

        if case_sensitive:
            request = request.filter(BaseKey.word == key)
        else:
            request = request.filter(BaseKey.word.in_([key, key.lower(), key.upper()]))

        if language:
            request = request.filter(BaseKey.language == language)
        return request


class BaseWord(db.Model, InitBase, DBBase, AddonWordQuerier, AddonWordGetter):
    """BaseWord model"""
    __tablename__ = t_name_words

    id = db.Column(db.Integer, primary_key=True)
    """Word's internal ID number: Integer"""

    id_old = db.Column(db.Integer, nullable=False)  # Compatibility with the previous database
    name = db.Column(db.String(64), nullable=False)
    origin = db.Column(db.String(128))
    origin_x = db.Column(db.String(64))
    match = db.Column(db.String(8))
    rank = db.Column(db.String(8))
    year = db.Column(db.Date)
    notes = db.Column(db.JSON)
    TID_old = db.Column(db.Integer)  # references

    type_id = db.Column("type", db.ForeignKey(f'{t_name_types}.id'), nullable=False)
    type: BaseType = db.relationship(
        BaseType.__name__, backref="words", enable_typechecks=False)

    event_start_id = db.Column(
        "event_start", db.ForeignKey(f'{t_name_events}.id'), nullable=False)
    event_start: BaseEvent = db.relationship(
        BaseEvent.__name__, foreign_keys=[event_start_id],
        backref="appeared_words", enable_typechecks=False)

    event_end_id = db.Column("event_end", db.ForeignKey(f'{t_name_events}.id'))
    event_end: BaseEvent = db.relationship(
        BaseEvent.__name__, foreign_keys=[event_end_id],
        backref="deprecated_words", enable_typechecks=False)

    authors: BaseQuery = db.relationship(
        BaseAuthor.__name__, secondary=t_connect_authors,
        backref="contribution", lazy='dynamic', enable_typechecks=False)

    definitions: BaseQuery = db.relationship(
        BaseDefinition.__name__, backref="source_word",
        lazy='dynamic', enable_typechecks=False)

    # word's derivatives
    _derivatives = db.relationship(
        'BaseWord', secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.parent_id == id),
        secondaryjoin=(t_connect_words.c.child_id == id),
        backref=db.backref('_parents', lazy='dynamic', enable_typechecks=False),
        lazy='dynamic', enable_typechecks=False)

    @property
    def parents(self) -> List[BaseWord]:
        """Get all parents of the Complexes, Little words or Affixes

        Args:

        Returns:
            List[BaseWord]
        """
        return self._parents.all()  # if self.type in self.__parentable else []

    @property
    def complexes(self) -> List[BaseWord]:
        """Get all word's complexes if exist

        Args:

        Returns:
            List[BaseWord]
        """
        return self.query_cpx().all()

    @property
    def affixes(self) -> List[BaseWord]:
        """Get all word's affixes if exist

        Args:

        Returns:
            List[BaseWord]
        """
        return self.query_afx().all()

    @property
    def keys(self) -> List[BaseKey]:
        """Get all BaseKey object related to this BaseWord
        Keep in mind that duplicate keys for different definitions
        will not be added to the final result

        Args:

        Returns:
            List[BaseKey]
        """
        return self.query_keys().all()
