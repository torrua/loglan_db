# -*- coding: utf-8 -*-
"""
This module contains a basic Definition Model
"""
import re
from typing import List, Optional, Union

from flask_sqlalchemy import BaseQuery
from sqlalchemy import exists

from loglan_db import db
from loglan_db.model_db import t_name_definitions, t_name_words
from loglan_db.model_db.base_connect_tables import t_connect_keys
from loglan_db.model_db.base_key import BaseKey
from loglan_db.model_init import InitBase, DBBase

__pdoc__ = {
    'BaseDefinition.source_word': 'source_word',
    'BaseDefinition.created': False, 'BaseDefinition.updated': False,
}


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
            language: str = None, pattern: str = KEY_PATTERN) -> Union[BaseKey, List[BaseKey]]:
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
