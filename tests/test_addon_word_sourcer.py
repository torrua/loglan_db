# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""
import pytest

from loglan_db.model_db.base_type import BaseType as Type
from loglan_db.model_db.base_word import BaseWord
from loglan_db.model_db.addons.addon_word_sourcer import AddonWordSourcer
from loglan_db.model_db.base_word_source import BaseWordSource as WordSource
from tests.data import littles, little_types
from tests.data import words, types, prim_words, prim_types, other_word_2
from tests.functions import db_add_objects


class Word(BaseWord, AddonWordSourcer):
    """BaseWord class with Sourcer addon"""


@pytest.mark.usefixtures("db")
class TestWord:
    """Word tests."""

    def test_get_sources_prim(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_add_objects(Word, prim_words)
        db_add_objects(Type, prim_types)

        afx = Word.get_by_id(3802)
        result = afx.get_sources_prim()
        assert result is None

        result = Word.get_by_id(3813).get_sources_prim()
        assert len(result) == 5
        assert isinstance(result, list)
        assert isinstance(result[0], WordSource)

        result = Word.get_by_id(291).get_sources_prim()
        assert isinstance(result, str)
        assert result == "balna: balnu"

        result = Word.get_by_id(318).get_sources_prim()
        assert isinstance(result, str)
        assert result == "banko: Int."

        result = Word.get_by_id(984).get_sources_prim()
        assert isinstance(result, str)
        assert result == "cimpe: abbreviation of cimpenizi"

        result = Word.get_by_id(5655).get_sources_prim()
        assert isinstance(result, str)
        assert result == "murmu: Onamatopoetic"

        result = Word.get_by_id(641).get_sources_prim()
        assert isinstance(result, str)
        assert result == "bordo: Fr. Bordeaux"

        result = Word.get_by_id(849).get_sources_prim()
        assert isinstance(result, str)
        assert result == "carbo: ISV"

    def test__get_sources_c_prim(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)

        result = Word.get_by_id(3813)._get_sources_c_prim()

        assert len(result) == 5
        assert isinstance(result, list)
        assert isinstance(result[0], WordSource)

        afx = Word.get_by_id(3802)
        result = afx._get_sources_c_prim()
        assert result is None

    def test__get_sources_c_prim_with_partial_data(self):
        db_add_objects(Word, [other_word_2, ])
        db_add_objects(Type, types)
        result = Word.get_by_id(3813)._get_sources_c_prim()
        assert len(result) == 5

    def test_get_sources_cpx(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)

        result = Word.get_by_id(7316).get_sources_cpx()
        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

        result = Word.get_by_id(7316).get_sources_cpx(as_str=True)
        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], str)
        assert result == ['pruci', 'kakto', ]

        result = Word.get_by_id(3813).get_sources_cpx()
        assert result == []

    def test_get_sources_cpd(self):
        db_add_objects(Word, littles)
        db_add_objects(Type, little_types)

        result = Word.get_by_id(479).get_sources_cpd()
        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

        result = Word.get_by_id(479).get_sources_cpd(as_str=True)
        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], str)
        assert result == ['bi', 'cio']

        db_add_objects(Word, words)
        db_add_objects(Type, types)

        afx = Word.get_by_id(3802)
        result = afx.get_sources_cpd()
        assert result == []
