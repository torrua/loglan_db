# -*- coding: utf-8 -*-
# pylint: disable=C0303
"""
This module contains a basic Syllable Model
"""
from loglan_db import db
from loglan_db.model_db import t_name_syllables
from loglan_db.model_init import InitBase, DBBase

__pdoc__ = {
    'BaseSyllable.created': False, 'BaseSyllable.updated': False,
}


class BaseSyllable(db.Model, InitBase, DBBase):
    """Base Syllable's DB Model

    Describes a table structure for storing information about loglan syllables.

    <details><summary>Show Examples</summary><p>
    ```python
    {'id': 37, 'name': 'zv', 'type': 'InitialCC', 'allowed': True}

    {'id': 38, 'name': 'cdz', 'type': 'UnintelligibleCCC', 'allowed': False}
    ```
    </p></details>
    """

    __tablename__ = t_name_syllables

    id = db.Column(db.Integer, primary_key=True)
    """*Syllable's internal ID number*  
        **int** : primary_key=True"""
    name = db.Column(db.String(8), nullable=False, unique=False)
    """*Syllable itself*  
            **str** : max_length=8, nullable=False, unique=False"""
    type = db.Column(db.String(32), nullable=False, unique=False)
    """*Syllable's type*  
            **str** : max_length=8, nullable=False, unique=False"""
    allowed = db.Column(db.Boolean, nullable=True, unique=False)
    """*Is this syllable acceptable in grammar*  
            **bool** : nullable=True, unique=False"""
