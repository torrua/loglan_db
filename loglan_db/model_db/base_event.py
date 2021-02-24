# -*- coding: utf-8 -*-
# pylint: disable=C0303

"""
This module contains a basic Event Model
"""
from __future__ import annotations
from loglan_db.model_db import t_name_events
from loglan_db.model_db.base_word import db
from loglan_db.model_init import InitBase, DBBase


class BaseEvent(db.Model, InitBase, DBBase):
    """Base Event's DB Model

    Describes a table structure for storing information about lexical events.

    <details><summary>Show Examples</summary><p>
    ```python
    {'suffix': 'INIT', 'definition': 'The initial vocabulary before updates.',
     'date': datetime.date(1975, 1, 1), 'annotation': 'Initial', 'name': 'Start', 'id': 1}

    {'suffix': 'RDC', 'definition': 'parsed all the words in the dictionary,
    identified ones that the parser did not recognize as words',
    'date': datetime.date(2016, 1, 15), 'annotation': 'Randall Cleanup',
    'name': 'Randall Dictionary Cleanup', 'id': 5}
    ```
    </p></details>
    """
    __tablename__ = t_name_events

    id = db.Column(db.Integer, primary_key=True)
    """*Event's internal ID number*  
        **int** : primary_key=True"""
    date = db.Column(db.Date, nullable=False, unique=False)
    """*Event's starting day*  
        **dateime.date** : nullable=False, unique=False"""
    name = db.Column(db.String(64), nullable=False, unique=False)
    """*Event's short name*  
        **str** : max_length=64, nullable=False, unique=False"""
    definition = db.Column(db.Text, nullable=False, unique=False)
    """*Event's definition*  
        **str** : nullable=False, unique=False"""
    annotation = db.Column(db.String(16), nullable=False, unique=False)
    """*Event's annotation (displayed in old format dictionary HTML file)*  
        **str** : max_length=16, nullable=False, unique=False"""
    suffix = db.Column(db.String(16), nullable=False, unique=False)
    """*Event's suffix (used to create filename when exporting HTML file)*  
        **str** : max_length=16, nullable=False, unique=False"""

    @classmethod
    def latest(cls) -> BaseEvent:
        """
        Gets the latest (current) `BaseEvent` from DB
        """
        return cls.query.order_by(-cls.id).first()
