# -*- coding: utf-8 -*-
# pylint: disable=R0903
"""
This module contains a default LOD dictionary model for a SQL database.
"""

from loglan_db.model_db.base_word import BaseWord
from loglan_db.model_db.base_word_spell import BaseWordSpell
from loglan_db.model_db.base_word_source import BaseWordSource
from loglan_db.model_db.base_definition import BaseDefinition
from loglan_db.model_db.base_type import BaseType
from loglan_db.model_db.base_syllable import BaseSyllable
from loglan_db.model_db.base_setting import BaseSetting
from loglan_db.model_db.base_key import BaseKey
from loglan_db.model_db.base_event import BaseEvent
from loglan_db.model_db.base_author import BaseAuthor


class DictionaryBase:
    """
    Workaround for separating classes and making inheritance selections
    """


class Author(DictionaryBase, BaseAuthor):
    """
    Author Class
    """
    __mapper_args__ = {
        'polymorphic_identity': "authors",
    }


class Event(DictionaryBase, BaseEvent):
    """
    Event Class
    """


class Key(DictionaryBase, BaseKey):
    """
    Key Class
    """


class Setting(DictionaryBase, BaseSetting):
    """
    Setting Class
    """


class Syllable(DictionaryBase, BaseSyllable):
    """
    Syllable Class
    """


class Type(DictionaryBase, BaseType):
    """
    Type Class
    """


class Definition(DictionaryBase, BaseDefinition):
    """
    Author Class
    """


class Word(DictionaryBase, BaseWord):
    """
    Word Class
    """


class WordSpell(DictionaryBase, BaseWordSpell):
    """
    WordSpell Class
    """


class WordSource(BaseWordSource):
    """
    WordSource Class
    """
