# -*- coding: utf-8 -*-
# pylint: disable=E1101, C0103

"""
This module contains a basic LOD dictionary model for a SQL database.
Each class is a detailed description of a db table:
Authors, Events, Keys, Definitions, Words, etc.
"""


from __future__ import annotations

import os
import re
from typing import List, Union, Optional

from flask_sqlalchemy import BaseQuery
from sqlalchemy import exists, or_

from loglan_db import db
from loglan_db.model_init import InitBase, DBBase

if os.environ.get("IS_PDOC", "False") == "True":
    from flask_sqlalchemy import SQLAlchemy
    from loglan_db import app_lod
    db = SQLAlchemy(app_lod())


t_name_authors = "authors"
"""`str` : `__tablename__` value for `BaseAuthor` table"""

t_name_events = "events"
"""`str` : `__tablename__` value for `BaseEvent` table"""
t_name_keys = "keys"
"""`str` : `__tablename__` value for `BaseKey` table"""

t_name_settings = "settings"
"""`str` : `__tablename__` value for `BaseSetting` table"""

t_name_syllables = "syllables"
"""`str` : `__tablename__` value for `BaseSyllable` table"""

t_name_types = "types"
"""`str` : `__tablename__` value for `BaseType` table"""

t_name_words = "words"
"""`str` : `__tablename__` value for `BaseWord` table"""

t_name_definitions = "definitions"
"""`str` : `__tablename__` value for `BaseDefinition` table"""

t_name_word_spells = "word_spells"
"""`str` : `__tablename__` value for `BaseWordSpell` table"""

t_name_word_sources = "word_sources"
"""`str` : `__tablename__` value for `BaseWordSource` table"""

t_name_connect_authors = "connect_authors"
"""`str` : `__tablename__` value for `t_connect_authors` table"""

t_name_connect_words = "connect_words"
"""`str` : `__tablename__` value for `t_connect_words` table"""

t_name_connect_keys = "connect_keys"
"""`str` : `__tablename__` value for `t_connect_keys` table"""

__pdoc__ = {
    'BaseEvent.appeared_words': """*Relationship query for getting a list of words appeared during this event*

    **query** : Optional[List[BaseWord]]""",

    'BaseEvent.deprecated_words': """*Relationship query for getting a list of words deprecated during this event*

    **query** : Optional[List[BaseWord]]""",

    'BaseAuthor.contribution': """*Relationship query for getting a list of words coined by this author*

    **query** : Optional[List[BaseWord]]""",

    'BaseType.words': 'words',
    'BaseDefinition.source_word': 'source_word',
    'BaseKey.definitions': """*Relationship query for getting a list of definitions related to this key*

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

t_connect_authors = db.Table(
    t_name_connect_authors, db.metadata,
    db.Column('AID', db.ForeignKey(f'{t_name_authors}.id'), primary_key=True),
    db.Column('WID', db.ForeignKey(f'{t_name_words}.id'), primary_key=True), )
"""`(sqlalchemy.sql.schema.Table)`: 
Connecting table for "many-to-many" relationship 
between `BaseAuthor` and `BaseWord` objects"""

t_connect_words = db.Table(
    t_name_connect_words, db.metadata,
    db.Column('parent_id', db.ForeignKey(f'{t_name_words}.id'), primary_key=True),
    db.Column('child_id', db.ForeignKey(f'{t_name_words}.id'), primary_key=True), )
"""`(sqlalchemy.sql.schema.Table)`: 
Connecting table for "many-to-many" relationship 
(parent-child) between `BaseWord` objects"""

t_connect_keys = db.Table(
    t_name_connect_keys, db.metadata,
    db.Column('KID', db.ForeignKey(f'{t_name_keys}.id'), primary_key=True),
    db.Column('DID', db.ForeignKey(f'{t_name_definitions}.id'), primary_key=True), )
"""`(sqlalchemy.sql.schema.Table)`: 
Connecting table for "many-to-many" relationship 
between `BaseDefinition` and `BaseKey` objects"""


class BaseAuthor(db.Model, InitBase, DBBase):
    """Base Author's DB Model

    Describes a table structure for storing information about words authors.

    Connects with words with "many-to-many" relationship. See `t_connect_authors`.

    <details><summary>Show Examples</summary><p>
    ```python
    {'id': 13, 'full_name': 'James Cooke Brown',
    'abbreviation': 'JCB', 'notes': ''}

    {'id': 29, 'full_name': 'Loglan 4&5',
    'abbreviation': 'L4',
    'notes': 'The printed-on-paper book,
              1975 version of the dictionary.'}
    ```
    </p></details>
    """

    __tablename__ = t_name_authors

    id = db.Column(db.Integer, primary_key=True)
    """*Author's internal ID number*  
        **int** : primary_key=True"""

    abbreviation = db.Column(db.String(64), nullable=False, unique=True)
    """*Author's abbreviation (used in the LOD dictionary)*  
        **str** : max_length=64, nullable=False, unique=True
    Example:
        > JCB, L4
    """

    full_name = db.Column(db.String(64), nullable=True, unique=False)
    """*Author's full name (if exists)*  
        **str** : max_length=64, nullable=True, unique=False
    Example:
        > James Cooke Brown, Loglan 4&5
    """

    notes = db.Column(db.String(128), nullable=True, unique=False)
    """*Any additional information about author*  
        **str** : max_length=128, nullable=True, unique=False
    """


class BaseEvent(db.Model, InitBase, DBBase):
    """Base Event's DB Model

    Describes a table structure for storing information about lexical events.

    <details><summary>Show Examples</summary><p>
    ```python
    {'suffix': 'INIT', 'definition': 'The initial vocabulary before updates.',
     'date': datetime.date(1975, 1, 1), 'annotation': 'Initial', 'name': 'Start', 'id': 1}

    {'suffix': 'RDC', 'definition': 'parsed all the words in the dictionary,
    identified ones that the parser did not recognize as words',
    'date': datetime.date(2016, 1, 15), 'annotation': 'Randall Cleanup',
    'name': 'Randall Dictionary Cleanup', 'id': 5}
    ```
    </p></details>
    """
    __tablename__ = t_name_events

    id = db.Column(db.Integer, primary_key=True)
    """*Event's internal ID number*  
        **int** : primary_key=True"""
    date = db.Column(db.Date, nullable=False, unique=False)
    """*Event's starting day*  
        **dateime.date** : nullable=False, unique=False"""
    name = db.Column(db.String(64), nullable=False, unique=False)
    """*Event's short name*  
        **str** : max_length=64, nullable=False, unique=False"""
    definition = db.Column(db.Text, nullable=False, unique=False)
    """*Event's definition*  
        **str** : nullable=False, unique=False"""
    annotation = db.Column(db.String(16), nullable=False, unique=False)
    """*Event's annotation (displayed in old format dictionary HTML file)*  
        **str** : max_length=16, nullable=False, unique=False"""
    suffix = db.Column(db.String(16), nullable=False, unique=False)
    """*Event's suffix (used to create filename when exporting HTML file)*  
        **str** : max_length=16, nullable=False, unique=False"""

    @classmethod
    def latest(cls) -> BaseEvent:
        """
        Gets the latest (current) `BaseEvent` from DB
        """
        return cls.query.order_by(-cls.id).first()


class BaseKey(db.Model, InitBase, DBBase):
    """Base Key's DB Model

    Describes a table structure for storing information about key words of the word's definitions.
    Some key words could belong to many definitions and some definitions could have many key words.
    That's why the relationship between Key and Definition should be many-to-many. See `t_connect_keys`.

    There is additional `word_language` UniqueConstraint here.

    <details><summary>Show Examples</summary><p>
    ```python
    {'language': 'en', 'word': 'aura', 'id': 1234}

    {'language': 'en', 'word': 'emotionality', 'id': 4321}
    ```
    </p></details>
    """
    __tablename__ = t_name_keys
    __table_args__ = (
        db.UniqueConstraint('word', 'language', name='_word_language_uc'), )

    id = db.Column(db.Integer, primary_key=True)
    """*Key's internal ID number*  
        **int** : primary_key=True"""
    word = db.Column(db.String(64), nullable=False, unique=False)
    """*Key's vernacular word*  
        **str** : max_length=64, nullable=False, unique=False  
    It is non-unique, as words can be the same in spelling in different languages"""
    language = db.Column(db.String(16), nullable=False, unique=False)
    """*Key's language*  
        **str** : max_length=16, nullable=False, unique=False"""


class BaseSetting(db.Model, InitBase, DBBase):
    """Base Setting's DB Model

    Describes a table structure for storing dictionary settings.

    <details><summary>Show Examples</summary><p>
    ```python
    {'id': 1, 'last_word_id': 10141,
    'date': datetime.datetime(2020, 10, 25, 5, 10, 20),
    'db_release': '4.5.9', 'db_version': 2}
    ```
    </p></details>
    """
    __tablename__ = t_name_settings

    id = db.Column(db.Integer, primary_key=True)
    """*Setting's internal ID number*  
        **int** : primary_key=True"""
    date = db.Column(db.DateTime, nullable=True, unique=False)
    """*Last modified date*  
        **dateime.datetime** : nullable=True, unique=False"""
    db_version = db.Column(db.Integer, nullable=False, unique=False)
    """*Database version (for old application)*  
        **int** : nullable=False, unique=False"""
    last_word_id = db.Column(db.Integer, nullable=False, unique=False)
    """*ID number of the last word in DB*  
            **int** : nullable=False, unique=False"""
    db_release = db.Column(db.String(16), nullable=False)
    """*Database release (for new application)*  
            **str** : max_length=16, nullable=False, unique=True"""


class BaseSyllable(db.Model, InitBase, DBBase):
    """Base Syllable's DB Model

    Describes a table structure for storing information about loglan syllables.

    <details><summary>Show Examples</summary><p>
    ```python
    {'id': 37, 'name': 'zv', 'type': 'InitialCC', 'allowed': True}

    {'id': 38, 'name': 'cdz', 'type': 'UnintelligibleCCC', 'allowed': False}
    ```
    </p></details>
    """

    __tablename__ = t_name_syllables

    id = db.Column(db.Integer, primary_key=True)
    """*Syllable's internal ID number*  
        **int** : primary_key=True"""
    name = db.Column(db.String(8), nullable=False, unique=False)
    """*Syllable itself*  
            **str** : max_length=8, nullable=False, unique=False"""
    type = db.Column(db.String(32), nullable=False, unique=False)
    """*Syllable's type*  
            **str** : max_length=8, nullable=False, unique=False"""
    allowed = db.Column(db.Boolean, nullable=True, unique=False)
    """*Is this syllable acceptable in grammar*  
            **bool** : nullable=True, unique=False"""


class BaseType(db.Model, InitBase, DBBase):
    """BaseType model"""
    __tablename__ = t_name_types

    id = db.Column(db.Integer, primary_key=True)
    """Type's internal ID number: Integer - E.g. 4, 8"""

    type = db.Column(db.String(16), nullable=False)  # E.g. 2-Cpx, C-Prim
    type_x = db.Column(db.String(16), nullable=False)  # E.g. Predicate, Predicate
    group = db.Column(db.String(16))  # E.g. Cpx, Prim
    parentable = db.Column(db.Boolean, nullable=False)  # E.g. True, False
    description = db.Column(db.String(255))  # E.g. Two-term Complex, ...

    @classmethod
    def by(cls, type_filter: Union[str, List[str]]) -> BaseQuery:
        """

        Args:
          type_filter: Union[str, List[str]]:

        Returns:

        """
        type_filter = [type_filter, ] if isinstance(type_filter, str) else type_filter

        return cls.query.filter(or_(
            cls.type.in_(type_filter), cls.type_x.in_(type_filter), cls.group.in_(type_filter),))


class BaseDefinition(db.Model, InitBase, DBBase):
    """BaseDefinition model"""
    __tablename__ = t_name_definitions

    id = db.Column(db.Integer, primary_key=True)
    """Definition's internal ID number: Integer"""

    word_id = db.Column(db.Integer, db.ForeignKey(f'{t_name_words}.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    usage = db.Column(db.String(64))
    grammar_code = db.Column(db.String(8))
    slots = db.Column(db.Integer)
    case_tags = db.Column(db.String(16))
    body = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(16))
    notes = db.Column(db.String(255))

    APPROVED_CASE_TAGS = ["B", "C", "D", "F", "G", "J", "K", "N", "P", "S", "V", ]
    KEY_PATTERN = r"(?<=\«)(.+?)(?=\»)"

    keys = db.relationship(BaseKey.__name__, secondary=t_connect_keys,
                           backref="definitions", lazy='dynamic', enable_typechecks=False)

    @property
    def grammar(self) -> str:
        """
        Combine definition's 'slots' and 'grammar_code' attributes

        Returns:
            String with grammar data like (3v) or (2n)
        """
        return f"({self.slots if self.slots else ''}" \
               f"{self.grammar_code if self.grammar_code else ''})"

    def link_keys_from_list_of_str(
            self, source: List[str],
            language: str = None) -> List[BaseKey]:
        """Linking a list of vernacular words with BaseDefinition
        Only new words will be linked, skipping those that were previously linked

        Args:
          source: List[str]: List of words on vernacular language
          language: str: Language of source words (Default value = None)

        Returns:
          List of linked BaseKey objects

        """

        language = language if language else self.language

        new_keys = BaseKey.query.filter(
            BaseKey.word.in_(source),
            BaseKey.language == language,
            ~exists().where(BaseKey.id == self.keys.subquery().c.id),
        ).all()

        self.keys.extend(new_keys)
        return new_keys

    def link_key_from_str(self, word: str, language: str = None) -> Optional[BaseKey]:
        """Linking vernacular word with BaseDefinition object
        Only new word will be linked, skipping this that was previously linked

        Args:
          word: str: name of BaseWord on vernacular language
          language: str: BaseWord's language (Default value = None)

        Returns:
          Linked BaseKey object or None if it were already linked

        """
        language = language if language else self.language
        result = self.link_keys_from_list_of_str(source=[word, ], language=language)
        return result[0] if result else None

    def link_keys_from_definition_body(
            self, language: str = None,
            pattern: str = KEY_PATTERN) -> List[BaseKey]:
        """Extract and link keys from BaseDefinition's body

        Args:
          language: str: Language of BaseDefinition's keys (Default value = None)
          pattern: str: Regex pattern for extracting keys from the BaseDefinition's body
            (Default value = KEY_PATTERN)

        Returns:
          List of linked BaseKey objects

        """
        language = language if language else self.language
        keys = re.findall(pattern, self.body)
        return self.link_keys_from_list_of_str(source=keys, language=language)

    def link_keys(
            self, source: Union[List[str], str, None] = None,
            language: str = None, pattern: str = KEY_PATTERN) -> Optional[BaseKey, List[BaseKey]]:
        """Universal method for linking all available types of key sources with BaseDefinition

        Args:
          source: Union[List[str], str, None]:
            If no source is provided, keys will be extracted from the BaseDefinition's body
            If source is a string or a list of strings, the language of the keys must be specified
            TypeError will be raised if the source contains inappropriate data
            (Default value = None)
          language: str: Language of BaseDefinition's keys (Default value = None)
          pattern: str: Regex pattern for extracting keys from the BaseDefinition's body
            (Default value = KEY_PATTERN)

        Returns:
          None, BaseKey, or List of BaseKeys

        """

        language = language if language else self.language

        if not source:
            return self.link_keys_from_definition_body(language=language, pattern=pattern)

        if isinstance(source, str):
            return self.link_key_from_str(word=source, language=language)

        if isinstance(source, list) and all(isinstance(item, str) for item in source):
            return self.link_keys_from_list_of_str(source=source, language=language)

        raise TypeError("Source for keys should have a string, or list of strings."
                        "You input %s" % type(source))

    @classmethod
    def by_key(
            cls, key: Union[BaseKey, str],
            language: str = None,
            case_sensitive: bool = False,
            partial_results: bool = False,
    ) -> BaseQuery:
        """Definition.Query filtered by specified key

        Args:
          key: Union[BaseKey, str]:
          language: str: Language of key (Default value = None)
          case_sensitive: bool:  (Default value = False)
          partial_results: bool:  (Default value = False)

        Returns:
          BaseQuery

        """

        key = BaseKey.word if isinstance(key, BaseKey) else str(key)
        request = cls.query.join(t_connect_keys, BaseKey).order_by(BaseKey.word)

        if language:
            request = request.filter(BaseKey.language == language)

        if case_sensitive:
            if partial_results:
                return request.filter(BaseKey.word.like(f"{key}%"))
            return request.filter(BaseKey.word == key)

        if partial_results:
            return request.filter(BaseKey.word.ilike(f"{key}%"))

        return request.filter(BaseKey.word.ilike(key))


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

        return f"{self.name}: {self.origin}{' < '+ self.origin_x if self.origin_x else ''}"

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

        sources = self.origin.replace("(", "").replace(")", "").replace("/", "")
        sources = sources.split("+")
        sources = [s for s in sources if s not in ["y", "r", "n"]]
        sources = [
            s if not s.endswith(("r", "h")) else s[:-1]
            for s in sources if s not in ["y", "r"]]

        exclude_type_ids = [t.id for t in BaseType.by(["LW", "Cpd"]).all()]
        result = BaseWord.query \
            .filter(BaseWord.name.in_(sources)) \
            .filter(BaseWord.type_id.notin_(exclude_type_ids)).all()

        if not as_str:
            return result

        result_as_str = []
        _ = [result_as_str.append(r) for r in sources if r not in result_as_str]
        return result_as_str

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

        sources = self.origin.replace("(", "").replace(")", "").replace("/", "").replace("-", "")
        sources = [s.strip() for s in sources.split("+")]

        type_ids = [t.id for t in BaseType.by(["LW", "Cpd"]).all()]
        result = BaseWord.query.filter(BaseWord.name.in_(sources)) \
            .filter(BaseWord.type_id.in_(type_ids)).all()

        if not as_str:
            return result

        result_as_str = []

        _ = [result_as_str.append(r) for r in sources if r not in result_as_str and r]

        return result_as_str

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
