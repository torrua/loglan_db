# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import pytest

from loglan_db.model_db.base_type import BaseType as Type
from loglan_db.model_db.base_word import BaseWord as Word
from tests.data import words, types
from tests.functions import db_add_objects, dar


@pytest.mark.usefixtures("db")
class TestType:
    """Type tests."""

    @pytest.mark.parametrize("item", types)
    def test_create_from_dict_with_data(self, item):
        type_ = dar(Type, item)
        type_from_db = Type.get_by_id(item["id"])

        assert type_ == type_from_db
        assert isinstance(type_.id, int)
        assert isinstance(type_.type, str)
        assert isinstance(type_.type_x, str)
        assert isinstance(type_.group, (str, type(None)))
        assert isinstance(type_.parentable, bool)
        assert isinstance(type_.description, (str, type(None)))
        with pytest.raises(Exception) as _:
            assert type_.type == "A-Prim"

    def test_by(self):
        db_add_objects(Type, types)
        test_type = Type.by("Little").first()
        assert test_type.type == "Afx"

        test_type = Type.by("Little")
        assert test_type[0].type == "Afx"

        test_type = Type.by("2-Cpx").first()
        assert test_type.group == "Cpx"

        test_type = Type.by("Predicate").count()
        assert test_type == 2

    def test_relationship_words(self):
        db_add_objects(Type, types)
        db_add_objects(Word, words)

        test_type = Type.by("Little").first()
        assert len(test_type.words) == 3

        test_type = Type.by("C-Prim").first()
        assert len(test_type.words) == 2

        test_type = Type.by("Cpx").first()
        assert len(test_type.words) == 1
