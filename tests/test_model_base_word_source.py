# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import pytest

from loglan_db.model_db.base_word_source import BaseWordSource as WordSource
from tests.data import word_1_source_1


@pytest.mark.usefixtures("db")
class TestWordSource:
    """WordSource tests."""

    def test_create_from_dict_with_data(self):
        """Get WordSource"""
        word_source = WordSource(**word_1_source_1)
        assert isinstance(word_source.coincidence, int)
        assert isinstance(word_source.length, int)
        assert isinstance(word_source.language, str)
        assert isinstance(word_source.transcription, str)

    def test_as_string(self):
        word_source = WordSource(**word_1_source_1)
        result = word_source.as_string

        assert isinstance(result, str)
        assert result == "2/2E do"
