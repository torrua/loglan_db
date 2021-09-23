# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903

"""Export Model unit tests."""

import pytest

from loglan_db.model_export import ExportAuthor as Author, ExportEvent as Event, \
    ExportSyllable as Syllable, ExportSetting as Setting, ExportType as Type, \
    ExportWord as Word, ExportDefinition as Definition, ExportWordSpell as WordSpell
from tests.data import author_1, other_author_1, event_1, syllable_35, \
    setting_1, type_1, word_1, other_word_1, word_2
from tests.data import connect_authors, connect_words
from tests.data import definitions, words, types, authors
from tests.functions import db_add_and_return, db_add_objects, db_add_object, \
    db_connect_authors, db_connect_words


@pytest.mark.usefixtures("db")
class TestAuthor:
    """Author tests."""
    def test_export(self):
        """Test Author.export() method"""
        obj = db_add_and_return(Author, author_1)

        result = obj.export()
        assert result == "L4@Loglan 4&5@The printed-on-paper " \
                         "book, 1975 version of the dictionary."


@pytest.mark.usefixtures("db")
class TestEvent:
    """Event tests."""
    def test_export(self):
        """Test Event.export() method"""
        obj = db_add_and_return(Event, event_1)

        result = obj.export()
        assert result == "1@Start@01/01/1975@The initial " \
                         "vocabulary before updates.@Initial@INIT"


@pytest.mark.usefixtures("db")
class TestSyllable:
    """Syllable tests."""
    def test_export(self):
        """Test Syllable.export() method"""
        obj = db_add_and_return(Syllable, syllable_35)

        result = obj.export()
        assert result == "vr@InitialCC@True"


@pytest.mark.usefixtures("db")
class TestSetting:
    """Setting tests."""
    def test_export(self):
        """Test Setting.export() method"""
        obj = db_add_and_return(Setting, setting_1)

        result = obj.export()
        assert result == "09.10.2020 09:10:20@2@10141@4.5.9"


@pytest.mark.usefixtures("db")
class TestType:
    """Type tests."""
    def test_export(self):
        """Test Type.export() method"""
        obj = db_add_and_return(Type, type_1)

        result = obj.export()
        assert result == "2-Cpx@Predicate@Cpx@True@Two-term Complex " \
                         "E.g. flicea, from fli(du)+ce(nj)a=liquid-become."


@pytest.mark.usefixtures("db")
class TestWord:
    """Word tests."""
    def test_export(self):
        """Test Word.export() method"""
        db_add_objects(Word, words)
        db_add_objects(Author, authors)
        db_add_objects(Type, types)
        db_connect_authors(connect_authors)
        db_connect_words(connect_words)
        word = Word.get_by_id(3813)

        result = word.export()
        assert result == "3880@C-Prim@Predicate@kak kao@56%@L4@1975@1.0@3/3R akt " \
                         "| 4/4S acto | 3/3F acte | 2/3E act | 2/3H kam@@prukao@"

    def test_e_affixes(self):
        """Test affix conversion"""
        db_add_objects(Word, words)
        db_connect_words(connect_words)
        db_add_objects(Type, types)
        word = Word.get_by_id(3813)

        result = word.e_affixes
        assert result == "kak kao"

    def test_e_source(self):
        """Test source (authors) conversion"""
        db_add_objects(Word, words)
        db_add_objects(Author, authors)
        db_connect_authors(connect_authors)
        word = Word.get_by_id(3911)

        result = word.e_source
        assert result == "JCB (?)"

        db_add_object(Word, other_word_1)
        db_add_object(Author, other_author_1)
        db_connect_authors([(13, 1006), (36, 1006), ])
        word = Word.get_by_id(1006)

        result = word.e_source
        assert result == "JCB/RAM"

    def test_e_year(self):
        """Test year conversion"""
        db_add_objects(Word, words)
        word = Word.get_by_id(3911)

        result = word.e_year
        assert result == "1988 (?)"

    def test_e_usedin(self):
        """Test used_in conversion"""
        db_add_objects(Word, words)
        db_connect_words(connect_words)
        db_add_objects(Type, types)
        word1 = Word.get_by_id(3813)

        result = word1.e_usedin
        assert result == "prukao"

        word2 = Word.get_by_id(7316)

        result = word2.e_usedin
        assert result == ""

    def test_e_usedin_empty(self):
        """Test used_in conversion if no cpx"""
        db_add_object(Word, word_2)
        db_add_objects(Type, types)
        word = Word.get_by_id(3813)

        result = word.e_usedin
        assert result == str()


@pytest.mark.usefixtures("db")
class TestDefinition:
    """Definition tests."""
    def test_export(self):
        """Test Definition.export() method"""
        db_add_objects(Word, words)
        db_add_objects(Definition, definitions)
        definition = Definition.get_by_id(13527)

        result = definition.export()
        assert result == "7191@1@@4v@K «test»/«examine» B for P with test V.@@K-BPV"


@pytest.mark.usefixtures("db")
class TestWordSpell:
    """WordSpell tests."""
    def test_export(self):
        """Test WordSpell.export() method"""
        obj = db_add_and_return(WordSpell, word_1)

        result = obj.export()
        assert result == "7191@prukao@prukao@555555@1@9999@"
