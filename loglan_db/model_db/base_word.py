# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains a basic Word Model
"""

from __future__ import annotations

from flask_sqlalchemy import BaseQuery

from loglan_db import db
from loglan_db.model_db import t_name_words, \
    t_name_types, t_name_events
from loglan_db.model_db.base_author import BaseAuthor
from loglan_db.model_db.base_connect_tables import \
    t_connect_authors, t_connect_words, t_connect_keys
from loglan_db.model_db.base_definition import BaseDefinition
from loglan_db.model_db.base_event import BaseEvent
from loglan_db.model_db.base_key import BaseKey
from loglan_db.model_db.base_type import BaseType
from loglan_db.model_init import InitBase, DBBase

__pdoc__ = {
    'BaseWord.created': False, 'BaseWord.updated': False,
}


class BaseWord(db.Model, InitBase, DBBase):
    """BaseWord model"""
    __tablename__ = t_name_words

    id = db.Column(db.Integer, primary_key=True)
    """Word's internal ID number: Integer"""
    name = db.Column(db.String(64), nullable=False)
    origin = db.Column(db.String(128))
    origin_x = db.Column(db.String(64))
    match = db.Column(db.String(8))
    rank = db.Column(db.String(8))
    year = db.Column(db.Date)
    notes = db.Column(db.JSON)

    # Fields for legacy database compatibility
    id_old = db.Column(db.Integer, nullable=False)
    TID_old = db.Column(db.Integer)  # references

    # Relationships
    type_id = db.Column("type", db.ForeignKey(f'{t_name_types}.id'), nullable=False)
    _type: BaseType = db.relationship(
        BaseType.__name__, back_populates="_words")

    event_start_id = db.Column(
        "event_start", db.ForeignKey(f'{t_name_events}.id'), nullable=False)
    _event_start: BaseEvent = db.relationship(
        BaseEvent.__name__, foreign_keys=[event_start_id],
        back_populates="_appeared_words")

    event_end_id = db.Column("event_end", db.ForeignKey(f'{t_name_events}.id'))
    _event_end: BaseEvent = db.relationship(
        BaseEvent.__name__, foreign_keys=[event_end_id],
        back_populates="_deprecated_words")

    _authors: BaseQuery = db.relationship(
        BaseAuthor.__name__, secondary=t_connect_authors,
        back_populates="_contribution", lazy='dynamic', enable_typechecks=False)

    _definitions: BaseQuery = db.relationship(
        BaseDefinition.__name__, back_populates="_source_word", lazy='dynamic')

    # word's derivatives
    _derivatives = db.relationship(
        'BaseWord', secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.parent_id == id),
        secondaryjoin=(t_connect_words.c.child_id == id),
        backref=db.backref('_parents', lazy='dynamic', enable_typechecks=False),
        lazy='dynamic', enable_typechecks=False)

    @property
    def type(self) -> BaseQuery:
        return self._type

    @property
    def event_start(self) -> BaseQuery:
        return self._event_start

    @property
    def event_end(self) -> BaseQuery:
        return self._event_end

    @property
    def authors(self) -> BaseQuery:
        return self._authors

    @property
    def definitions(self) -> BaseQuery:
        return self._definitions

    @property
    def derivatives(self) -> BaseQuery:
        return self._derivatives

    def query_derivatives(
            self, word_type: str = None, word_type_x: str = None,
            word_group: str = None) -> BaseQuery:
        """Query to get all derivatives of the word, depending on its parameters

        Args:
          word_type: str:  (Default value = None)
          E.g. "2-Cpx", "C-Prim", "LW"<hr>

          word_type_x: str:  (Default value = None)
          E.g. "Predicate", "Name", "Affix"<hr>

          word_group: str:  (Default value = None)
          E.g. "Cpx", "Prim", "Little"<hr>

        Returns:
            BaseQuery
        """

        type_values = [
                (BaseType.type, word_type),
                (BaseType.type_x, word_type_x),
                (BaseType.group, word_group), ]

        type_filters = [i[0] == i[1] for i in type_values if i[1]]

        return self._derivatives.join(BaseType)\
            .filter(self.id == t_connect_words.c.parent_id, *type_filters)\
            .order_by(type(self).name.asc())

    @property
    def parents(self) -> BaseQuery:
        """Query to get all parents for Complexes, Little words or Affixes

        Returns:
            BaseQuery
        """
        return self._parents

    @property
    def complexes(self) -> BaseQuery:
        """
        Get all word's complexes if exist
        Only primitives and Little Words have complexes.

        Returns:
            BaseQuery
        """
        return self.query_derivatives(word_group="Cpx")

    @property
    def affixes(self) -> BaseQuery:
        """
        Get all word's affixes if exist
        Only primitives have affixes.

        Returns:
            BaseQuery
        """
        return self.query_derivatives(word_type="Afx")

    @property
    def keys(self) -> BaseQuery:
        """Get all BaseKey object related to this BaseWord.

        Keep in mind that duplicated keys from related definitions
        will be counted with ```.count()``` but excluded from ```.all()``` request

        Returns:
            BaseQuery
        """
        return BaseKey.query.join(
            t_connect_keys, BaseDefinition, BaseWord).filter(BaseWord.id == self.id)
