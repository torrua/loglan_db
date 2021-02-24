# -*- coding: utf-8 -*-
# pylint: disable=C0303

"""
This module contains a basic Connection Table Models
"""
from loglan_db import db
from loglan_db.model_db import t_name_connect_authors, \
    t_name_authors, t_name_words, t_name_connect_words, \
    t_name_connect_keys, t_name_keys, t_name_definitions


t_connect_authors = db.Table(
    t_name_connect_authors, db.metadata,
    db.Column('AID', db.ForeignKey(f'{t_name_authors}.id'), primary_key=True),
    db.Column('WID', db.ForeignKey(f'{t_name_words}.id'), primary_key=True), )
"""`(sqlalchemy.sql.schema.Table)`: 
Connecting table for "many-to-many" relationship 
between `BaseAuthor` and `BaseWord` objects"""

t_connect_words = db.Table(
    t_name_connect_words, db.metadata,
    db.Column('parent_id', db.ForeignKey(f'{t_name_words}.id'), primary_key=True),
    db.Column('child_id', db.ForeignKey(f'{t_name_words}.id'), primary_key=True), )
"""`(sqlalchemy.sql.schema.Table)`: 
Connecting table for "many-to-many" relationship 
(parent-child) between `BaseWord` objects"""

t_connect_keys = db.Table(
    t_name_connect_keys, db.metadata,
    db.Column('KID', db.ForeignKey(f'{t_name_keys}.id'), primary_key=True),
    db.Column('DID', db.ForeignKey(f'{t_name_definitions}.id'), primary_key=True), )
"""`(sqlalchemy.sql.schema.Table)`: 
Connecting table for "many-to-many" relationship 
between `BaseDefinition` and `BaseKey` objects"""
