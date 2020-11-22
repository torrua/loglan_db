# -*- coding: utf-8 -*-
# pylint: disable=E1101, C0103

"""
Base Model of LOD database
"""

from __future__ import annotations

import re
from typing import List, Union, Optional

from flask_sqlalchemy import BaseQuery
from sqlalchemy import exists, or_

from loglan_db import db
from loglan_db.model_init import InitBase, DBBase

t_name_authors = "authors"
t_name_events = "events"
t_name_keys = "keys"
t_name_settings = "settings"
t_name_syllables = "syllables"
t_name_types = "types"
t_name_words = "words"
t_name_definitions = "definitions"
t_name_x_words = "x_words"
t_name_word_spells = "word_spells"
t_name_word_sources = "word_sources"

db.metadata.clear()

t_connect_authors = db.Table(
    'connect_authors', db.metadata,
    db.Column('AID', db.ForeignKey(f'{t_name_authors}.id'), primary_key=True),
    db.Column('WID', db.ForeignKey(f'{t_name_words}.id'), primary_key=True), )
t_connect_words = db.Table(
    'connect_words', db.metadata,
    db.Column('parent_id', db.ForeignKey(f'{t_name_words}.id'), primary_key=True),
    db.Column('child_id', db.ForeignKey(f'{t_name_words}.id'), primary_key=True), )
t_connect_keys = db.Table(
    'connect_keys', db.metadata,
    db.Column('KID', db.ForeignKey(f'{t_name_keys}.id'), primary_key=True),
    db.Column('DID', db.ForeignKey(f'{t_name_definitions}.id'), primary_key=True), )


class BaseAuthor(db.Model, InitBase, DBBase):
    """
    Author model
    """
    __tablename__ = t_name_authors

    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(64), unique=True, nullable=False)
    full_name = db.Column(db.String(64))
    notes = db.Column(db.String(128))


class BaseEvent(db.Model, InitBase, DBBase):
    """
    BaseEvent model
    """
    __tablename__ = t_name_events

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    annotation = db.Column(db.String(16), nullable=False)
    suffix = db.Column(db.String(16), nullable=False)

    @classmethod
    def latest(cls):
        """
        :return: the latest (current) event
        """
        return cls.query.order_by(-cls.id).first()


class BaseKey(db.Model, InitBase, DBBase):
    """
    BaseKey model
    """
    __tablename__ = t_name_keys

    id = db.Column(db.Integer, primary_key=True)
    # TODO remove unique from word field but add language checking
    word = db.Column(db.String(64), unique=True, nullable=False)
    language = db.Column(db.String(16))


class BaseSetting(db.Model, InitBase, DBBase):
    """
    BaseSetting model
    """
    __tablename__ = t_name_settings

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
    db_version = db.Column(db.Integer, nullable=False)
    last_word_id = db.Column(db.Integer, nullable=False)
    db_release = db.Column(db.String(16), nullable=False)


class BaseSyllable(db.Model, InitBase, DBBase):
    """
    BaseSyllable model
    """
    __tablename__ = t_name_syllables

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), nullable=False)
    type = db.Column(db.String(32), nullable=False)
    allowed = db.Column(db.Boolean)


class BaseType(db.Model, InitBase, DBBase):
    """
    BaseType model
    """
    __tablename__ = t_name_types

    id = db.Column(db.Integer, primary_key=True)  # E.g. 4, 8
    type = db.Column(db.String(16), nullable=False)  # E.g. 2-Cpx, C-Prim
    type_x = db.Column(db.String(16), nullable=False)  # E.g. Predicate, Predicate
    group = db.Column(db.String(16))  # E.g. Cpx, Prim
    parentable = db.Column(db.Boolean, nullable=False)  # E.g. True, False
    description = db.Column(db.String(255))  # E.g. Two-term Complex, ...

    @classmethod
    def by(cls, type_filter: Union[str, List[str]]) -> BaseQuery:
        """
        :param type_filter:
        :return:
        """
        type_filter = [type_filter, ] if isinstance(type_filter, str) else type_filter

        return cls.query.filter(or_(
            cls.type.in_(type_filter), cls.type_x.in_(type_filter), cls.group.in_(type_filter),))


class BaseDefinition(db.Model, InitBase, DBBase):
    """
    BaseDefinition model
    """
    __tablename__ = t_name_definitions

    id = db.Column(db.Integer, primary_key=True)
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
    def grammar(self):
        """Return definition's grammar data like (3v) or (2n)"""
        return f"({self.slots if self.slots else ''}" \
               f"{self.grammar_code if self.grammar_code else ''})"

    def link_keys_from_list_of_str(
            self, source: List[str],
            language: str = None) -> List[BaseKey]:
        """
        Linking a list of vernacular words with BaseDefinition
        Only new words will be linked, skipping those that were previously linked

        :param source: List of words on vernacular language
        :param language: Language of source words
        :return: List of linked BaseKey objects
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
        """
        Linking vernacular word with BaseDefinition object
        Only new word will be linked, skipping this that was previously linked

        :param word: BaseWord on vernacular language
        :param language: BaseWords language
        :return: Linked BaseKey object or None if it were already linked
        """
        language = language if language else self.language
        result = self.link_keys_from_list_of_str(source=[word, ], language=language)
        return result[0] if result else None

    def link_keys_from_list_of_obj(self, source: List[BaseKey]) -> List[BaseKey]:
        """
        Linking BaseKey objects with BaseDefinition
        Only new BaseKeys will be linked, skipping those that were previously linked

        :param source: List of BaseKey objects from db
        :return: List of linked BaseKey objects
        """
        new_keys = list(set(source) - set(self.keys))
        self.keys.extend(new_keys)
        return new_keys

    def link_key_from_obj(self, key: BaseKey) -> Optional[BaseKey]:
        """
        Linking BaseKey object with BaseDefinition object
        It will be skipped if the BaseKey has already been linked before
        :param key: BaseKey objects from db
        :return: linked BaseKey object or None if it were already linked
        """
        if key and not self.keys.filter(BaseKey.id == key.id).count() > 0:
            self.keys.append(key)
            return key
        return None

    # TODO
    '''
    def link_key_from_obj(self, key: BaseKey, add_new_to_db: bool = True) -> Optional[BaseKey]:
        """
        Linking BaseKey object with BaseDefinition object
        It will be skipped if the BaseKey has already been linked before
        :param key: BaseKey objects from db
        :return: linked BaseKey object or None if it were already linked
        """
        
        if not key.id:  # and BaseKey.query.filter(~exists().where(BaseKey.id == self.keys.subquery().c.id)).all():
            ValueError("A key without an id cannot be added.")
            # There is no key with id = %s in DB.\n"
            # "Please add key to DB first or remove ID field from key's data." % key.id)
        else:
            key = exist_key

        if key and not self.keys.filter(BaseKey.id == key.id).count() > 0:
            self.keys.append(key)
            return key
        return None
    '''

    def link_keys_from_definition_body(
            self, language: str = None,
            pattern: str = KEY_PATTERN) -> List[BaseKey]:
        """
        Extract and link keys from BaseDefinition's body
        :param language: Language of BaseDefinition's keys
        :param pattern: Regex pattern for extracting keys from the BaseDefinition's body
        :return: List of linked BaseKey objects
        """
        language = language if language else self.language
        keys = re.findall(pattern, self.body)
        return self.link_keys_from_list_of_str(source=keys, language=language)

    def link_keys(
            self, source: Union[List[BaseKey], List[str], BaseKey, str, None] = None,
            language: str = None, pattern: str = KEY_PATTERN) -> Union[BaseKey, List[BaseKey]]:
        """
        Universal method for linking all available types of key sources with BaseDefinition

        :param source: Could be a str, BaseKey, List of BaseKeys or str, or None
        If no source is provided, keys will be extracted from the BaseDefinition's body
        If source is a string or a list of strings, the language of the keys must be specified
        TypeError will be raised if the source contains inappropriate data
        :param language: Language of BaseDefinition's keys
        :param pattern: Regex pattern for extracting keys from the BaseDefinition's body
        :return: None, BaseKey, or List of BaseKeys
        """

        language = language if language else self.language

        if not source:
            return self.link_keys_from_definition_body(language=language, pattern=pattern)

        if isinstance(source, str):
            return self.link_key_from_str(word=source, language=language)

        if isinstance(source, BaseKey):
            return self.link_key_from_obj(key=source)

        if isinstance(source, list):

            if all(isinstance(item, BaseKey) for item in source):
                return self.link_keys_from_list_of_obj(source=source)

            if all(isinstance(item, str) for item in source):
                return self.link_keys_from_list_of_str(source=source, language=language)

        raise TypeError("Source for keys should have a string, "
                        "BaseKey or list of strings or BaseKeys type. "
                        "You input %s" % type(source))


class BaseWord(db.Model, InitBase, DBBase):
    """
    BaseWord model
    """
    __tablename__ = t_name_words

    id = db.Column(db.Integer, primary_key=True)
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
    type = db.relationship(
        BaseType.__name__, backref="words", enable_typechecks=False)

    event_start_id = db.Column(
        "event_start", db.ForeignKey(f'{t_name_events}.id'), nullable=False)
    event_start = db.relationship(
        BaseEvent.__name__, foreign_keys=[event_start_id],
        backref="appeared_words", enable_typechecks=False)

    event_end_id = db.Column("event_end", db.ForeignKey(f'{t_name_events}.id'))
    event_end = db.relationship(
        BaseEvent.__name__, foreign_keys=[event_end_id],
        backref="deprecated_words", enable_typechecks=False)

    authors = db.relationship(
        BaseAuthor.__name__, secondary=t_connect_authors,
        backref="contribution", lazy='dynamic', enable_typechecks=False)

    definitions = db.relationship(
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
        :param child: BaseWord object
        :return: bool
        """
        return self.__derivatives.filter(t_connect_words.c.child_id == child.id).count() > 0

    def add_child(self, child: BaseWord) -> str:
        """
        Add derivative for the source word
        Get words from Used In and add relationship in database
        :param child: BaseWord object
        :return: None
        """
        # TODO add check if type of child is allowed to add to this word
        if not self.__is_parented(child):
            self.__derivatives.append(child)
        return child.name

    def add_children(self, children: List[BaseWord]):
        """
        Add derivatives for the source word
        Get words from Used In and add relationship in database
        :param children: List of BaseWord objects
        :return: None
        """
        # TODO add check if type of child is allowed to add to this word
        new_children = list(set(children) - set(self.__derivatives))
        _ = self.__derivatives.extend(new_children) if new_children else None

    def add_author(self, author: BaseAuthor) -> str:
        """
        Connect Author object with BaseWord object
        :param author: Author object
        :return:
        """
        if not self.authors.filter(BaseAuthor.abbreviation == author.abbreviation).count() > 0:
            self.authors.append(author)
        return author.abbreviation

    def add_authors(self, authors: List[BaseAuthor]):
        """
        Connect Author objects with BaseWord object
        :param authors: List of Author object
        :return:
        """
        new_authors = list(set(authors) - set(self.authors))
        _ = self.authors.extend(new_authors) if new_authors else None

    def query_derivatives(self,
                          word_type: str = None,
                          word_type_x: str = None,
                          word_group: str = None) -> BaseQuery:
        """
        Query to get all derivatives of the word, depending on its parameters
        :param word_type:
        :param word_type_x:
        :param word_group:
        :return:
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
        """
        Query to get all parents of the Complexes, Little words or Affixes
        :return: Query
        """
        return self._parents  # if self.type in self.__parentable else []

    def query_cpx(self) -> BaseQuery:
        """
        Query to qet all the complexes that exist for this word
        Only primitives have affixes
        :return: Query
        """
        return self.query_derivatives(word_group="Cpx")

    def query_afx(self) -> BaseQuery:
        """
        Query to qet all the affixes that exist for this word
        Only primitives have affixes
        :return: Query
        """
        return self.query_derivatives(word_type="Afx")

    def query_keys(self) -> BaseQuery:
        """
        Query for the BaseKeys linked with this BaseWord
        :return: Query
        """
        return BaseKey.query.join(
            t_connect_keys, BaseDefinition, BaseWord).filter(BaseWord.id == self.id)

    @property
    def parents(self) -> List[BaseWord]:
        """
        Get all parents of the Complexes, Little words or Affixes
        :return: List of BaseWords
        """
        return self.query_parents().all()

    @property
    def complexes(self) -> List[BaseWord]:
        """
        Get all word's complexes if exist
        :return: List of BaseWords
        """
        return self.query_cpx().all()

    @property
    def affixes(self) -> List[BaseWord]:
        """
        Get all word's affixes if exist
        :return: List of BaseWords
        """
        return self.query_afx().all()

    @property
    def keys(self) -> List[BaseKey]:
        """
        Get all BaseKey object related to this BaseWord
        Keep in mind that duplicate keys for different definitions
            will not be added to the final result
        :return: List of BaseKey
        """
        return self.query_keys().all()

    def get_sources_prim(self):
        """
        :return:
        """
        # existing_prim_types = ["C", "D", "I", "L", "N", "O", "S", ]

        if not self.type.group == "Prim":
            return []

        prim_type = self.type.type[:1]

        if prim_type == "C":
            return self._get_sources_c_prim()

        if prim_type in ["D", "I", "L", "N", "O", "S", ]:  # TODO
            return f"{self.name}: {self.origin} < {self.origin_x}"

        return list()

    def _get_sources_c_prim(self) -> List[BaseWordSource]:
        """
        :return:
        """
        if self.type.type != "C-Prim":
            return []

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
        """
        Extract source words from self.origin field accordingly
        :param as_str: Boolean - return BaseWord objects if False else as simple str
        :return: List of words from which the self.name was created

        Example: 'foldjacea' > ['forli', 'djano', 'cenja']
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
        """
        Extract source words from self.origin field accordingly
        :param as_str: Boolean - return BaseWord objects if False else as simple str
        :return: List of words from which the self.name was created
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
        """
        Query filtered by specified Event (latest by default)
        :param event_id: Event object or Event.id (int)
        :return: Query
        """
        if not event_id:
            event_id = BaseEvent.latest().id

        event_id = BaseEvent.id if isinstance(event_id, BaseEvent) else int(event_id)

        return cls.query.filter(cls.event_start_id <= event_id) \
            .filter(or_(cls.event_end_id > event_id, cls.event_end_id.is_(None))) \
            .order_by(cls.name)

    @classmethod
    def by_name(cls, name: str, case_sensitive: bool = False) -> BaseQuery:
        """
        Word.Query filtered by specified name
        :param name: str
        :param case_sensitive: bool
        :return: Query
        """
        if case_sensitive:
            return cls.query.filter(cls.name == name)
        return cls.query.filter(cls.name.in_([name, name.lower(), name.upper()]))

    @classmethod
    def by_key(
            cls, key: Union[BaseKey, str],
            language: str = None,
            case_sensitive: bool = False) -> BaseQuery:
        """
        Word.Query filtered by specified key
        :param key: BaseKey object or str
        :param language: Language of key
        :param case_sensitive: bool
        :return: Query
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
    """
    Word Source from BaseWord.origin for Prims
    """
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
    def as_string(self):  # For example, '3/5R mesto'
        """
        :return:
        """
        return f"{self.coincidence}/{self.length}{self.language} {self.transcription}"


class BaseWordSpell(InitBase):
    """BaseWordSpell model"""
    __tablename__ = t_name_word_spells
