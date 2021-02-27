# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import datetime

import pytest

from loglan_db.model_db.base_event import BaseEvent as Event
from loglan_db.model_db.base_word import BaseWord as Word
from tests.data import changed_words, changed_events, all_events
from tests.functions import db_add_objects, dar


@pytest.mark.usefixtures("db")
class TestEvent:
    """Event tests."""

    @pytest.mark.parametrize("item", all_events)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        event = dar(Event, item)
        event_from_db = Event.get_by_id(item["id"])

        assert event == event_from_db
        assert isinstance(event, Event)
        assert isinstance(event.id, int)
        assert isinstance(event.date, datetime.date)
        assert isinstance(event.name, str)
        assert isinstance(event.definition, str)
        assert isinstance(event.annotation, str)
        assert isinstance(event.suffix, str)

    def test_relationship_deprecated_words(self):
        db_add_objects(Word, changed_words)
        db_add_objects(Event, changed_events)
        event = Event.get_by_id(5)

        assert isinstance(event.appeared_words, list)
        assert len(event.appeared_words) == 3

    def test_relationship_appeared_words(self):
        db_add_objects(Word, changed_words)
        db_add_objects(Event, changed_events)
        event = Event.get_by_id(5)

        assert isinstance(event.deprecated_words, list)
        assert len(event.deprecated_words) == 4

    def test_latest(self):
        db_add_objects(Event, all_events)
        latest = Event.latest()

        assert latest.id == 6
        assert latest.annotation == 'Torrua Repair'
