# -*- coding: utf-8 -*-
"""
This module contains a basic Type Model
"""
from typing import Union, List

from flask_sqlalchemy import BaseQuery
from sqlalchemy import or_

from loglan_db import db
from loglan_db.model_db import t_name_types
from loglan_db.model_init import InitBase, DBBase

__pdoc__ = {
    'BaseType.words': 'words',
    'BaseType.created': False, 'BaseType.updated': False,
}


class BaseType(db.Model, InitBase, DBBase):
    """BaseType model"""
    __tablename__ = t_name_types

    id = db.Column(db.Integer, primary_key=True)
    """Type's internal ID number: Integer - E.g. 4, 8"""

    type = db.Column(db.String(16), nullable=False)  # E.g. 2-Cpx, C-Prim
    type_x = db.Column(db.String(16), nullable=False)  # E.g. Predicate, Predicate
    group = db.Column(db.String(16))  # E.g. Cpx, Prim
    parentable = db.Column(db.Boolean, nullable=False)  # E.g. True, False
    description = db.Column(db.String(255))  # E.g. Two-term Complex, ...

    words = db.relationship(
        "BaseWord", back_populates="type",
        foreign_keys="BaseWord.type_id")

    @classmethod
    def by(cls, type_filter: Union[str, List[str]]) -> BaseQuery:
        """

        Args:
          type_filter: Union[str, List[str]]:

        Returns:

        """
        type_filter = [type_filter, ] if isinstance(type_filter, str) else type_filter

        return cls.query.filter(or_(
            cls.type.in_(type_filter), cls.type_x.in_(type_filter), cls.group.in_(type_filter), ))
