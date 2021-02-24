# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains a basic LOD dictionary model for a SQL database.
Each class is a detailed description of a db table:
Authors, Events, Keys, Definitions, Words, etc.
Also it contains additional necessary variables.
"""

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
