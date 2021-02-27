# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import pytest

from loglan_db.model_db.base_definition import BaseDefinition as Definition
from loglan_db.model_db.base_key import BaseKey as Key
from tests.data import connect_keys
from tests.data import definition_1, definition_2
from tests.data import keys, definitions
from tests.functions import db_connect_keys, db_add_objects, dar, db_add_object


@pytest.mark.usefixtures("db")
class TestDefinition:
    """Definition tests."""

    @pytest.mark.parametrize("item", definitions)
    def test_create_from_dict_with_data(self, item):
        definition = dar(Definition, item)
        definition_from_db = Definition.get_by_id(item["id"])

        assert definition == definition_from_db
        assert isinstance(definition.id, int)
        assert isinstance(definition.word_id, int)
        assert isinstance(definition.position, int)
        assert isinstance(definition.usage, (str, type(None)))
        assert isinstance(definition.grammar_code, (str, type(None)))
        assert isinstance(definition.slots, (int, type(None)))
        assert isinstance(definition.case_tags, (str, type(None)))
        assert isinstance(definition.body, str)
        assert isinstance(definition.language, (str, type(None)))
        assert isinstance(definition.notes, (str, type(None)))

    def test_relationship_keys(self):
        pass

    def test_relationship_source_word(self):
        pass

    def test_grammar(self):
        db_add_objects(Definition, definitions)
        d = Definition.get_by_id(13527)
        assert d.grammar == "(4v)"

        d = Definition.get_by_id(13529)
        assert d.grammar == "(a)"

    def test_link_keys_from_list_of_str(self):
        db_add_objects(Definition, definitions)
        db_add_objects(Key, keys)

        keys_to_add = ["test", "examine"]
        d = Definition.get_by_id(13527)
        assert d.keys.count() == 0

        d.link_keys_from_list_of_str(keys_to_add)
        assert d.keys.count() == 2
        assert sorted([k.word for k in d.keys]) == sorted(keys_to_add)

    def test_link_key_from_str(self):
        db_add_objects(Key, keys)
        d = dar(Definition, definition_2)
        assert d.keys.count() == 0

        key_to_add = "tester"
        d.link_key_from_str(key_to_add)
        assert d.keys.count() == 1
        assert d.keys.first().word == key_to_add

    def test_link_keys_from_definition_body(self):
        db_add_objects(Key, keys)
        d = dar(Definition, definition_1)
        assert d.keys.count() == 0

        d.link_keys_from_definition_body()
        assert d.keys.count() == 2
        assert sorted([k.word for k in d.keys]) == sorted(["test", "examine"])

    def test_link_keys(self):
        db_add_objects(Key, keys)

        d0 = dar(Definition, definitions[0])
        assert d0.keys.count() == 0
        keys_to_add_str = ["test", "examine"]
        d0.link_keys(keys_to_add_str)
        assert d0.keys.count() == 2

        d1 = dar(Definition, definitions[1])
        assert d1.keys.count() == 0
        key_to_add_str = "tester"
        d1.link_keys(key_to_add_str)
        assert d1.keys.count() == 1

        d2 = dar(Definition, definitions[10])
        assert d2.keys.count() == 0
        d2.link_keys()
        assert d2.keys.count() == 2

        d3 = dar(Definition, definitions[3])
        es_word, es_code = "probar", "es"
        ru_word, ru_code = "тест", "ru"
        db_add_object(Key, {"word": es_word, "language": es_code})
        db_add_object(Key, {"word": ru_word, "language": ru_code})

        d3.link_keys(source=ru_word, language=ru_code)
        assert d3.keys.first().language == ru_code

        d3.link_keys(source=es_word, language=es_code)
        assert d3.keys.count() == 2
        assert sorted([k.language for k in d3.keys.all()]) == [es_code, ru_code]

        d4 = dar(Definition, definitions[4])
        with pytest.raises(TypeError) as _:
            d4.link_keys(source=1234)

    def test_by_key(self):
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_keys(connect_keys)

        result = Definition.by_key("Test", case_sensitive=True).all()
        assert len(result) == 0

        result = Definition.by_key("test", case_sensitive=True, partial_results=True).all()
        assert len(result) == 10

        result = Definition.by_key("test", case_sensitive=True, partial_results=False, language="en").all()
        assert len(result) == 5

        result = Definition.by_key("Test", case_sensitive=False, partial_results=True).all()
        assert len(result) == 10

        result = Definition.by_key("test", language="es").all()
        assert len(result) == 0
