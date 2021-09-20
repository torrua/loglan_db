# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import pytest

from loglan_db.model_db.base_author import BaseAuthor as Author
from loglan_db.model_db.base_word import BaseWord as Word
from tests.data import connect_authors
from tests.data import words, authors
from tests.functions import db_connect_authors, db_add_objects, dar


@pytest.mark.usefixtures("db")
class TestAuthor:
    """Author tests."""
    @pytest.mark.parametrize("item", authors)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        author = dar(Author, item)
        author_from_db = Author.get_by_id(item["id"])

        assert author == author_from_db
        assert isinstance(author, Author)
        assert isinstance(author.id, int)
        assert isinstance(author.abbreviation, str)
        assert isinstance(author.full_name, (str, type(None)))
        assert isinstance(author.notes, (str, type(None)))

    def test_relationship_contribution(self):
        db_add_objects(Author, authors)
        db_add_objects(Word, words)
        db_connect_authors(connect_authors)

        test_author = Author.get_by_id(29)
        assert len(test_author.contribution) == 3
        assert isinstance(test_author.contribution, list)
        assert [w.name for w in test_author.contribution] == ['kakto', 'pruci', 'prukao']

        test_author = Author.get_by_id(13)
        assert len(test_author.contribution) == 3
        assert [w.name for w in test_author.contribution] == ['kak', 'kao', 'pru']
