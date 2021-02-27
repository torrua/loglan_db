# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import pytest

from loglan_db.model_db.base_syllable import BaseSyllable as Syllable
from tests.data import syllables
from tests.functions import dar


@pytest.mark.usefixtures("db")
class TestSyllable:
    """Syllable tests."""

    @pytest.mark.parametrize("item", syllables)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        syllable = dar(Syllable, item)
        syllable_from_db = Syllable.get_by_id(item["id"])

        assert syllable == syllable_from_db
        assert isinstance(syllable, Syllable)
        assert isinstance(syllable.id, int)
        assert isinstance(syllable.name, str)
        assert isinstance(syllable.type, str)
        assert isinstance(syllable.allowed, (bool, type(None)))
