# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903

"""HTML Model unit tests."""

import pytest

from loglan_db.model import Word
from tests.data import word_1, words
from tests.functions import db_add_and_return, db_add_object, db_add_objects
from loglan_db.model_init import InitBase


@pytest.mark.usefixtures("db")
class TestInitBase:
    """InitBase class tests."""

    def test___repr__(self):
        w = InitBase()
        result = w.__repr__()
        assert isinstance(result, str)

    def test___str__(self):
        db_add_object(Word, word_1)
        w = Word.get_by_id(word_1.get("id"))
        result = w.__str__()
        assert result == \
            "{'TID_old': None, 'event_end_id': None, 'event_start_id': 1, 'id': 7316, " \
            "'id_old': 7191, 'match': '', 'name': 'prukao', 'notes': None, 'origin': 'pru(ci)+ka(kt)o', " \
            "'origin_x': 'test act', 'rank': '1.9', 'type_id': 5, 'year': datetime.date(1975, 1, 1)}"

    def test_from_dict(self):
        w = Word.from_dict(word_1)
        assert w.name == "prukao"

    def test_stringer(self):
        assert Word.stringer(1) == "1"
        assert Word.stringer(None) == str()
        assert Word.stringer("text") == "text"

    def test_init(self):
        result = InitBase(**{"a": 1, "b": 2})
        assert result.a == 1


@pytest.mark.usefixtures("db")
class TestDBBase:
    """DBBase class tests."""

    @staticmethod
    def test_save():
        w = Word(**word_1)
        assert w.save() is None

    @staticmethod
    def test_update():
        w = db_add_and_return(Word, word_1)
        assert w.update({'name': 'test', }) is None

    @staticmethod
    def test_delete():
        w = db_add_and_return(Word, word_1)
        assert w.delete() is None

    def test_get_all(self):
        db_add_objects(Word, words)
        words_from_db = Word.get_all()
        assert isinstance(words_from_db, list)
        assert len(words_from_db) == 6

    def test_attributes_all(self):
        result = Word.attributes_all()
        assert set(result) == {
            'TID_old', '_authors', 'created', '_definitions',
            '_derivatives', '_event_end', 'event_end_id', '_event_start',
            'event_start_id', 'id', 'id_old', 'match', 'name',
            'notes', 'origin', 'origin_x', 'rank', '_type',
            'type_id', 'updated', 'year', '_parents'}

    def test_attributes_basic(self):
        result = Word.attributes_basic()
        assert set(result) == {
            'TID_old', 'created', 'event_end_id', 'event_start_id',
            'id', 'id_old', 'match', 'name', 'notes', 'origin',
            'origin_x', 'rank', 'type_id', 'updated', 'year'}

    def test_attributes_extended(self):
        result = Word.attributes_extended()
        assert set(result) == {
            'TID_old', '_authors', 'created', '_definitions', '_derivatives',
            '_event_end', '_event_start',
            'id', 'id_old', 'match', 'name', 'notes', 'origin',
            'origin_x', '_parents', 'rank', '_type', 'updated', 'year'}

    def test_relationships(self):
        result = Word.relationships()
        assert set(result) == {
            '_authors', '_definitions', '_derivatives',
            '_parents',  '_event_end', '_event_start', '_type'}

    def test_foreign_keys(self):
        result = Word.foreign_keys()
        assert set(result) == {'event_end_id', 'event_start_id', 'type_id'}

    def test_non_foreign_keys(self):
        result = Word.non_foreign_keys()
        assert set(result) == {
            'TID_old', 'created', 'id', 'id_old', 'match', 'name',
            'notes', 'origin', 'origin_x', 'rank', 'updated', 'year'}
