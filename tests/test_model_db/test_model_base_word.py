# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import datetime

import pytest

from loglan_db.model_db.base_author import BaseAuthor as Author
from loglan_db.model_db.base_definition import BaseDefinition as Definition
from loglan_db.model_db.base_event import BaseEvent as Event
from loglan_db.model_db.base_key import BaseKey as Key
from loglan_db.model_db.base_type import BaseType as Type
from loglan_db.model_db.base_word import BaseWord as Word
from tests.data import all_events
from tests.data import connect_authors
from tests.data import connect_keys
from tests.data import connect_words
from tests.data import keys, definitions, words, types, authors
from tests.data import word_1
from tests.functions import db_connect_authors, db_connect_keys, db_connect_words, \
    db_add_objects, dar


@pytest.mark.usefixtures("db")
class TestWord:
    """Word tests."""

    @pytest.mark.parametrize("item", words)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""
        word = dar(Word, item)
        word_from_db = Word.get_by_id(item["id"])

        assert word == word_from_db
        assert isinstance(word.id, int)
        assert isinstance(word.id_old, int)
        assert isinstance(word.name, str)
        assert isinstance(word.origin, (str, type(None)))
        assert isinstance(word.origin_x, (str, type(None)))
        assert isinstance(word.match, (str, type(None)))
        assert isinstance(word.rank, (str, type(None)))
        assert isinstance(word.year, (datetime.date, type(None)))
        assert isinstance(word.notes, (dict, type(None)))
        assert isinstance(word.TID_old, (int, type(None)))

    @pytest.mark.parametrize("item", words)
    def test_type_relationship(self, item):
        word = dar(Word, item)

        type_data = [t for t in types if t["id"] == word.type_id][0]
        type_ = dar(Type, type_data)

        type_from_db = Type.get_by_id(word.type_id)

        assert isinstance(type_, Type)
        assert isinstance(type_from_db, Type)
        assert type_from_db == type_ == word.type

    @pytest.mark.parametrize("item", words)
    def test_event_relationship(self, item):
        db_add_objects(Event, all_events)
        word = dar(Word, item)

        event_start_from_db = Event.get_by_id(word.event_start_id)
        assert isinstance(event_start_from_db, Event)
        assert event_start_from_db == word.event_start

        if word.event_end_id:
            event_end_from_db = Event.get_by_id(word.event_end_id)
            assert isinstance(event_end_from_db, Event)
            assert event_end_from_db == word.event_start
        else:
            assert word.event_end is None

    def test_authors_relationship(self):
        db_add_objects(Word, words)
        db_add_objects(Author, authors)
        db_connect_authors(connect_authors)

        word = Word.get_by_id(7316)
        author = Author.get_by_id(29)

        assert word.authors.count() == 1
        assert word.authors[0] == author
        assert word.authors.first() == author
        assert isinstance(word.authors.all(), list)
        assert len(word.authors.all()) == 1

    def test_definitions_relationship(self):
        word = dar(Word, word_1)
        definitions_to_add = [d for d in definitions if d["word_id"] == word.id]
        db_add_objects(Definition, definitions_to_add)

        assert word.definitions.count() == len(definitions_to_add) == 5
        assert isinstance(word.definitions[0], Definition)

    def test_query_derivatives(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        p1 = Word.get_by_id(3813)
        p2 = Word.get_by_id(7315)

        assert p1.query_derivatives().count() == 3
        assert p2.query_derivatives().count() == 2
        assert isinstance(p2.query_derivatives().first(), Word)

        assert p1.query_derivatives(word_type="Afx").count() == 2
        assert p1.query_derivatives(word_type="2-Cpx").count() == 1

        assert p1.query_derivatives(word_type_x="Predicate").count() == 1
        assert p2.query_derivatives(word_type_x="Affix").count() == 1

        assert p1.query_derivatives(word_group="Little").count() == 2
        assert p2.query_derivatives(word_group="Cpx").count() == 1

    def test_query_cpx(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        p1 = Word.get_by_id(3813)
        p2 = Word.get_by_id(7315)

        assert p1.query_cpx().count() == 1
        assert p2.query_cpx().count() == 1

    def test_query_afx(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        p1 = Word.get_by_id(3813)
        p2 = Word.get_by_id(7315)

        assert p1.query_afx().count() == 2
        assert p2.query_afx().count() == 1

    def test_query_keys(self):
        db_add_objects(Word, words)
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_keys(connect_keys)

        result = Word.get_by_id(7316).query_keys().count()

        assert result == 7

    def test_parents(self):
        db_add_objects(Word, words)
        db_connect_words(connect_words)

        result = Word.get_by_id(7316).parents

        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

    def test_complexes(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        result = Word.get_by_id(3813).complexes

        assert len(result) == 1
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

    def test_affixes(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        result = Word.get_by_id(3813).affixes

        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

    def test_keys(self):
        db_add_objects(Word, words)
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_keys(connect_keys)

        result = Word.get_by_id(7316).keys

        assert len(result) == 6
        assert isinstance(result, list)
        assert isinstance(result[0], Key)
