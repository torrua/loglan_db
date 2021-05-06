# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import pytest

from loglan_db.model_db.base_definition import BaseDefinition as Definition
from loglan_db.model_db.base_event import BaseEvent as Event
from loglan_db.model_db.base_key import BaseKey as Key
from loglan_db.model_db.base_word import BaseWord
from loglan_db.model_db.addons.addon_word_getter import AddonWordGetter

from tests.data import changed_words, all_events, doubled_words
from tests.data import connect_keys
from tests.data import keys, definitions, words, events
from tests.functions import db_connect_keys, db_add_objects


class Word(BaseWord, AddonWordGetter):
    """BaseWord class with Getter addon"""


@pytest.mark.usefixtures("db")
class TestWord:
    """Word tests."""

    def test_by_event(self):
        db_add_objects(Word, changed_words + words)
        db_add_objects(Event, all_events)

        result = Word.get_all()
        assert len(result) == 13

        result = Word.by_event(1).all()
        assert len(result) == 10

        result = Word.by_event(5).all()
        assert len(result) == 9

        result = Word.by_event().all()
        assert len(result) == 9

    def test_by_name(self):
        db_add_objects(Word, doubled_words)
        db_add_objects(Event, events)
        result = Word.by_name("duo").count()
        assert result == 2

        result = Word.by_name("duo").all()
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

        result = sorted([w.type_id for w in result])
        assert result == [2, 17]

        result = Word.by_name("duo").first()
        assert isinstance(result, Word)

    def test_by_key(self):
        db_add_objects(Word, words)
        db_add_objects(Definition, definitions)
        db_add_objects(Key, keys)
        db_add_objects(Event, all_events)

        db_connect_keys(connect_keys)

        result = Word.by_key("test").count()
        assert result == 5

        result = Word.by_key("Test").count()
        assert result == 5

        result = [w.name for w in Word.by_key("test").all()]
        assert result == ['pru', 'pruci', 'prukao']

        result = Word.by_key("test", language="es").count()
        assert result == 0

        result = Word.by_key("test", language="en").count()
        assert result == 5
