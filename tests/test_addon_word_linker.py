# -*- coding: utf-8 -*-
# pylint: disable=R0201, C0116, C0103, W0212
"""Base Addon Word Linker unit tests."""

import pytest

from loglan_db.model_db.addons.addon_word_linker import AddonWordLinker
from loglan_db.model_db.base_word import BaseWord
from loglan_db.model_db.base_author import BaseAuthor as Author

from tests.functions import db_add_objects

from tests.data import words, authors
from tests.data import word_1, word_2, word_3


class Word(BaseWord, AddonWordLinker):
    """BaseWord class with Linker addon"""


@pytest.mark.usefixtures("db")
class TestWord:
    """Word tests."""

    def test_add_child(self):
        db_add_objects(Word, words)
        cmp = Word.get_by_id(word_1.get("id"))
        assert cmp._parents.count() == 0

        for p in [word_2, word_3]:
            prim = Word.get_by_id(p.get("id"))
            result = prim.add_child(cmp)
            assert result == cmp.name

        assert cmp._parents.count() == 2

        prim = Word.get_by_id(word_3.get("id"))
        prim.add_child(cmp)
        assert cmp._parents.count() == 2

    def test_add_children(self):
        db_add_objects(Word, words)
        cmp = Word.get_by_id(word_1.get("id"))
        assert cmp._parents.count() == 0

        for p in [word_2, word_3]:
            prim = Word.get_by_id(p.get("id"))
            prim.add_children([cmp, ])

        assert cmp._parents.count() == 2

    def test_add_author(self):
        db_add_objects(Word, words)
        db_add_objects(Author, authors)

        word = Word.get_by_id(7316)
        author = Author.get_by_id(29)
        assert word.authors.count() == 0

        word.add_author(author)
        assert word.authors.count() == 1
        assert word.authors[0] == author

        word.add_author(author)
        assert word.authors.count() == 1

    def test_add_authors(self):
        db_add_objects(Word, words)
        db_add_objects(Author, authors)

        word = Word.get_by_id(7316)
        assert word.authors.count() == 0

        local_authors = Author.get_all()
        word.add_authors(local_authors)

        assert word.authors.count() == 2
        assert isinstance(word.authors[0], Author)
