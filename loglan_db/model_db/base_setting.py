# -*- coding: utf-8 -*-
# pylint: disable=C0303
"""
This module contains a basic Setting Model
"""
from loglan_db.model_db import t_name_settings
from loglan_db.model_db.base_word import db
from loglan_db.model_init import InitBase, DBBase


class BaseSetting(db.Model, InitBase, DBBase):
    """Base Setting's DB Model

    Describes a table structure for storing dictionary settings.

    <details><summary>Show Examples</summary><p>
    ```python
    {'id': 1, 'last_word_id': 10141,
    'date': datetime.datetime(2020, 10, 25, 5, 10, 20),
    'db_release': '4.5.9', 'db_version': 2}
    ```
    </p></details>
    """
    __tablename__ = t_name_settings

    id = db.Column(db.Integer, primary_key=True)
    """*Setting's internal ID number*  
        **int** : primary_key=True"""
    date = db.Column(db.DateTime, nullable=True, unique=False)
    """*Last modified date*  
        **dateime.datetime** : nullable=True, unique=False"""
    db_version = db.Column(db.Integer, nullable=False, unique=False)
    """*Database version (for old application)*  
        **int** : nullable=False, unique=False"""
    last_word_id = db.Column(db.Integer, nullable=False, unique=False)
    """*ID number of the last word in DB*  
            **int** : nullable=False, unique=False"""
    db_release = db.Column(db.String(16), nullable=False)
    """*Database release (for new application)*  
            **str** : max_length=16, nullable=False, unique=True"""
