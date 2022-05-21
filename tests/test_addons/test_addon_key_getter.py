# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import pytest

from loglan_db.model_db.base_event import BaseEvent as Event
from loglan_db.model_db.base_key import BaseKey
from loglan_db.model_db.base_word import BaseWord as Word
from loglan_db.model_db.base_definition import BaseDefinition as Definition
from loglan_db.model_db.addons.addon_key_getter import AddonKeyGetter

from tests.data import changed_words, changed_definitions, all_events
from tests.data import changed_keys, connect_changed_keys
from tests.functions import db_connect_keys, db_add_objects


class Key(BaseKey, AddonKeyGetter):
    """BaseKey class with Getter addon"""


@pytest.mark.usefixtures("db")
class TestWord:
    """Word tests."""

    def test_by_event(self):
        db_add_objects(Word, changed_words)
        db_add_objects(Event, all_events)
        db_add_objects(Key, changed_keys)
        db_add_objects(Definition, changed_definitions)
        db_connect_keys(connect_changed_keys)

        result_1 = sorted([key.id for key in Key.by_event(1).all()])
        assert result_1 == [5926, 8824]

        result_2 = sorted([key.id for key in Key.by_event().all()])
        assert result_2 == [620, 1421]
