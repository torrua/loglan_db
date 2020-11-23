# -*- coding: utf-8 -*-

"""
Default Model of LOD database
"""

from loglan_db.model_base import BaseAuthor, BaseEvent, \
    BaseKey, BaseSetting, BaseSyllable, BaseType, \
    BaseDefinition, BaseWord, BaseWordSpell, BaseWordSource


class DictionaryBase:
    """Workaround for separating classes and making inheritance selections"""


class Author(DictionaryBase, BaseAuthor):
    __mapper_args__ = {
        'polymorphic_identity': "authors",
    }


class Event(DictionaryBase, BaseEvent):
    pass


class Key(DictionaryBase, BaseKey):
    pass


class Setting(DictionaryBase, BaseSetting):
    pass


class Syllable(DictionaryBase, BaseSyllable):
    pass


class Type(DictionaryBase, BaseType):
    pass


class Definition(DictionaryBase, BaseDefinition):
    pass


class Word(DictionaryBase, BaseWord):
    pass


class WordSpell(DictionaryBase, BaseWordSpell):
    pass


class WordSource(BaseWordSource):
    pass
