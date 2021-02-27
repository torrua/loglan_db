# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import pytest
import sqlalchemy.exc

from loglan_db.model_db.base_definition import BaseDefinition as Definition
from loglan_db.model_db.base_key import BaseKey as Key
from tests.data import connect_keys
from tests.data import keys, definitions
from tests.data import un_key_1, un_key_2, un_key_3
from tests.functions import db_connect_keys, db_add_objects, dar


@pytest.mark.usefixtures("db")
class TestKey:
    """Key tests."""

    @pytest.mark.parametrize("item", keys)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        key = dar(Key, item)
        key_from_db = Key.get_by_id(item["id"])

        assert key == key_from_db
        assert isinstance(key, Key)
        assert isinstance(key.id, int)
        assert isinstance(key.word, str)
        assert isinstance(key.language, (str, type(None)))

    def test_relationship_definitions(self):
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_keys(connect_keys)
        key = Key.get_by_id(12474)

        assert isinstance(key.definitions, list)
        assert len(key.definitions) == 5
        assert [d.id for d in key.definitions] == [13521, 13523, 13524, 13527, 13531]

    def test_uniqueness(self):
        db_add_objects(Key, [un_key_1, un_key_2, ])
        result = [k.word for k in Key.get_all()]
        assert result == ["examine", "examine", ]

        with pytest.raises(sqlalchemy.exc.IntegrityError) as _:
            assert isinstance(dar(Key, un_key_3), Key)
