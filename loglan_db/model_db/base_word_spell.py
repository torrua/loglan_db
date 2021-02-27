# -*- coding: utf-8 -*-
"""
This module contains a basic WordSpell Model
"""
from loglan_db.model_db import t_name_word_spells
from loglan_db.model_init import InitBase


class BaseWordSpell(InitBase):
    """BaseWordSpell model"""
    __tablename__ = t_name_word_spells
