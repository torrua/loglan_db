# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import datetime

import pytest

from loglan_db.model_db.base_setting import BaseSetting as Setting
from tests.data import settings
from tests.functions import dar


@pytest.mark.usefixtures("db")
class TestSetting:
    """Setting tests."""

    @pytest.mark.parametrize("item", settings)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        setting = dar(Setting, item)
        setting_from_db = Setting.get_by_id(item["id"])

        assert setting == setting_from_db
        assert isinstance(setting, Setting)
        assert isinstance(setting.id, int)
        assert isinstance(setting.date, (datetime.datetime, type(None)))
        assert isinstance(setting.db_version, int)
        assert isinstance(setting.last_word_id, int)
        assert isinstance(setting.db_release, str)
