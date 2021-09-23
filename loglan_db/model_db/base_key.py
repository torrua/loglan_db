# -*- coding: utf-8 -*-
# pylint: disable=C0303
"""
This module contains a basic Key Model
"""
from loglan_db import db
from loglan_db.model_db import t_name_keys
from loglan_db.model_init import InitBase, DBBase
from loglan_db.model_db.base_connect_tables import t_connect_keys

__pdoc__ = {
    'BaseKey.definitions':
        """*Relationship query for getting a list of definitions related to this key*

    **query** : Optional[List[BaseDefinition]]""",
    'BaseKey.created': False, 'BaseKey.updated': False, }


class BaseKey(db.Model, InitBase, DBBase):
    """Base Key's DB Model

    Describes a table structure for storing information
    about key words of the word's definitions.
    Some key words could belong to many definitions
    and some definitions could have many key words.
    That's why the relationship between Key
    and Definition should be many-to-many. See `t_connect_keys`.

    There is additional `word_language` UniqueConstraint here.

    <details><summary>Show Examples</summary><p>
    ```python
    {'language': 'en', 'word': 'aura', 'id': 1234}

    {'language': 'en', 'word': 'emotionality', 'id': 4321}
    ```
    </p></details>
    """
    __tablename__ = t_name_keys
    __table_args__ = (
        db.UniqueConstraint('word', 'language', name='_word_language_uc'), )

    id = db.Column(db.Integer, primary_key=True)
    """*Key's internal ID number*  
        **int** : primary_key=True"""
    word = db.Column(db.String(64), nullable=False, unique=False)
    """*Key's vernacular word*  
        **str** : max_length=64, nullable=False, unique=False  
    It is non-unique, as words can be the same in spelling in different languages"""
    language = db.Column(db.String(16), nullable=False, unique=False)
    """*Key's language*  
        **str** : max_length=16, nullable=False, unique=False"""

    _definitions = db.relationship(
        "BaseDefinition", secondary=t_connect_keys, lazy='dynamic', back_populates="_keys")

    @property
    def definitions(self):
        return self._definitions
