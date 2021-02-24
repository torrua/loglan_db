# -*- coding: utf-8 -*-
# pylint: disable=C0103, C0303
"""
This module contains a basic Word Model and addons
"""

from __future__ import annotations

import os
import re
from typing import List, Optional, Union

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import or_

from loglan_db import app_lod, db
from loglan_db.model_db import t_name_word_spells, t_name_words, \
    t_name_types, t_name_events, t_name_word_sources
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
    'BaseEvent.appeared_words':
        """*Relationship query for getting a list of words appeared during this event*

    **query** : Optional[List[BaseWord]]""",

    'BaseEvent.deprecated_words':
        """*Relationship query for getting a list of words deprecated during this event*

    **query** : Optional[List[BaseWord]]""",

    'BaseAuthor.contribution':
        """*Relationship query for getting a list of words coined by this author*

    **query** : Optional[List[BaseWord]]""",

    'BaseType.words': 'words',
    'BaseDefinition.source_word': 'source_word',
    'BaseKey.definitions':
        """*Relationship query for getting a list of definitions related to this key*

    **query** : Optional[List[BaseDefinition]]""",

    'BaseAuthor.created': False, 'BaseAuthor.updated': False,
    'BaseEvent.created': False, 'BaseEvent.updated': False,
    'BaseKey.created': False, 'BaseKey.updated': False,
    'BaseSetting.created': False, 'BaseSetting.updated': False,
    'BaseSyllable.created': False, 'BaseSyllable.updated': False,
    'BaseType.created': False, 'BaseType.updated': False,
    'BaseDefinition.created': False, 'BaseDefinition.updated': False,
    'BaseWord.created': False, 'BaseWord.updated': False,
}


class BaseWord(db.Model, InitBase, DBBase):
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
    __derivatives = db.relationship(
        'BaseWord', secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.parent_id == id),
        secondaryjoin=(t_connect_words.c.child_id == id),
        backref=db.backref('_parents', lazy='dynamic', enable_typechecks=False),
        lazy='dynamic', enable_typechecks=False)

    def __is_parented(self, child: BaseWord) -> bool:
        """
        Check, if this word is already added as a parent for this 'child'

        Args:
            child: BaseWord: BaseWord object to check

        Returns: bool:

        """
        return self.__derivatives.filter(t_connect_words.c.child_id == child.id).count() > 0

    def add_child(self, child: BaseWord) -> str:
        """Add derivative for the source word
        Get words from Used In and add relationship in database

        Args:
          child: BaseWord: Object to add

        Returns:
            String with the name of the added child (BaseWord.name)

        """
        # TODO add check if type of child is allowed to add to this word
        if not self.__is_parented(child):
            self.__derivatives.append(child)
        return child.name

    def add_children(self, children: List[BaseWord]):
        """Add derivatives for the source word
        Get words from Used In and add relationship in database

        Args:
          children: List[BaseWord]:

        Returns:
          None

        """
        # TODO add check if type of child is allowed to add to this word
        new_children = list(set(children) - set(self.__derivatives))
        _ = self.__derivatives.extend(new_children) if new_children else None

    def add_author(self, author: BaseAuthor) -> str:
        """Connect Author object with BaseWord object

        Args:
          author: BaseAuthor:

        Returns:

        """
        if not self.authors.filter(BaseAuthor.abbreviation == author.abbreviation).count() > 0:
            self.authors.append(author)
        return author.abbreviation

    def add_authors(self, authors: List[BaseAuthor]):
        """Connect Author objects with BaseWord object

        Args:
          authors: List[BaseAuthor]:

        Returns:

        """
        new_authors = list(set(authors) - set(self.authors))
        _ = self.authors.extend(new_authors) if new_authors else None

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
        result = self.__derivatives.filter(self.id == t_connect_words.c.parent_id)

        if word_type or word_type_x or word_group:
            result = result.join(BaseType)

        if word_type:
            result = result.filter(BaseType.type == word_type)
        if word_type_x:
            result = result.filter(BaseType.type_x == word_type_x)
        if word_group:
            result = result.filter(BaseType.group == word_group)

        return result.order_by(BaseWord.name.asc())

    def query_parents(self) -> BaseQuery:
        """Query to get all parents of the Complexes, Little words or Affixes
        :return: Query

        Args:

        Returns:
            BaseQuery
        """
        return self._parents  # if self.type in self.__parentable else []

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

    @property
    def parents(self) -> List[BaseWord]:
        """Get all parents of the Complexes, Little words or Affixes

        Args:

        Returns:
            List[BaseWord]
        """
        return self.query_parents().all()

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

    def get_sources_prim(self):
        """

        Returns:

        """
        # existing_prim_types = ["C", "D", "I", "L", "N", "O", "S", ]

        if not self.type.group == "Prim":
            return None

        prim_type = self.type.type[:1]

        if prim_type == "C":
            return self._get_sources_c_prim()

        return f"{self.name}: {self.origin}{' < ' + self.origin_x if self.origin_x else ''}"

    def _get_sources_c_prim(self) -> Optional[List[BaseWordSource]]:
        """

        Returns:

        """
        if self.type.type != "C-Prim":
            return None

        pattern_source = r"\d+\/\d+\w"
        sources = str(self.origin).split(" | ")
        word_sources = []

        for source in sources:
            compatibility = re.search(pattern_source, source)[0]
            c_l = compatibility[:-1].split("/")
            transcription = (re.search(rf"(?!{pattern_source}) .+", source)[0]).strip()
            word_source = BaseWordSource(**{
                "coincidence": int(c_l[0]),
                "length": int(c_l[1]),
                "language": compatibility[-1:],
                "transcription": transcription, })
            word_sources.append(word_source)

        return word_sources

    def get_sources_cpx(self, as_str: bool = False) -> List[Union[str, BaseWord]]:
        """Extract source words from self.origin field accordingly
        Args:
            as_str (bool): return BaseWord objects if False else as simple str
            (Default value = False)
        Example:
            'foldjacea' > ['forli', 'djano', 'cenja']
        Returns:
            List of words from which the self.name was created

        """

        # these prims have switched djifoas like 'flo' for 'folma'
        switch_prims = [
            'canli', 'farfu', 'folma', 'forli', 'kutla', 'marka',
            'mordu', 'sanca', 'sordi', 'suksi', 'surna']

        if not self.type.group == "Cpx":
            return []

        sources = self._prepare_sources_cpx()

        result = self.words_from_source_cpx(sources)

        if not as_str:
            return result

        result_as_str = []
        _ = [result_as_str.append(r) for r in sources if r not in result_as_str]
        return result_as_str

    @staticmethod
    def words_from_source_cpx(sources: List[str]) -> List[BaseWord]:
        """

        Args:
            sources:

        Returns:

        """
        exclude_type_ids = [t.id for t in BaseType.by(["LW", "Cpd"]).all()]
        return BaseWord.query \
            .filter(BaseWord.name.in_(sources)) \
            .filter(BaseWord.type_id.notin_(exclude_type_ids)).all()

    def _prepare_sources_cpx(self) -> List[str]:
        """
        # TODO
        Returns:

        """
        sources = self.origin.replace("(", "").replace(")", "").replace("/", "")
        sources = sources.split("+")
        sources = [
            s if not s.endswith(("r", "h")) else s[:-1]
            for s in sources if s not in ["y", "r", "n"]]
        return sources

    def get_sources_cpd(self, as_str: bool = False) -> List[Union[str, BaseWord]]:
        """Extract source words from self.origin field accordingly

        Args:
          as_str: bool: return BaseWord objects if False else as simple str
          (Default value = False)

        Returns:
          List of words from which the self.name was created

        """

        if not self.type.type == "Cpd":
            return []

        sources = self._prepare_sources_cpd()

        result = self.words_from_source_cpd(sources)

        if not as_str:
            return result

        result_as_str = []

        _ = [result_as_str.append(r) for r in sources if r not in result_as_str and r]

        return result_as_str

    def _prepare_sources_cpd(self) -> List[str]:
        """

        Returns:

        """
        sources = self.origin.replace("(", "").replace(")", "").replace("/", "").replace("-", "")
        sources = [s.strip() for s in sources.split("+")]
        return sources

    @staticmethod
    def words_from_source_cpd(sources: List[str]) -> List[BaseWord]:
        """

        Args:
            sources:

        Returns:

        """
        type_ids = [t.id for t in BaseType.by(["LW", "Cpd"]).all()]
        return BaseWord.query.filter(BaseWord.name.in_(sources)) \
            .filter(BaseWord.type_id.in_(type_ids)).all()

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


class BaseWordSource(InitBase):
    """Word Source from BaseWord.origin for Prims"""
    __tablename__ = t_name_word_sources

    LANGUAGES = {
        "E": "English",
        "C": "Chinese",
        "H": "Hindi",
        "R": "Russian",
        "S": "Spanish",
        "F": "French",
        "J": "Japanese",
        "G": "German", }

    coincidence: int = None
    length: int = None
    language: str = None
    transcription: str = None

    @property
    def as_string(self) -> str:
        """
        Format WordSource as string, for example, '3/5R mesto'
        Returns:
            str
        """
        return f"{self.coincidence}/{self.length}{self.language} {self.transcription}"


class BaseWordSpell(InitBase):
    """BaseWordSpell model"""
    __tablename__ = t_name_word_spells
