# -*- coding: utf-8 -*-
"""
This module contains a basic WordSource Model
"""
from loglan_db.model_db import t_name_word_sources
from loglan_db.model_init import InitBase


class BaseWordSource(InitBase):
    """Word Source from BaseWord.origin for Prims"""
    __tablename__ = t_name_word_sources

    LANGUAGES = {
        "E": "English",
        "C": "Chinese",
        "H": "Hindi",
        "R": "Russian",
        "S": "Spanish",
        "F": "French",
        "J": "Japanese",
        "G": "German", }

    coincidence: int = None
    length: int = None
    language: str = None
    transcription: str = None

    @property
    def as_string(self) -> str:
        """
        Format WordSource as string, for example, '3/5R mesto'
        Returns:
            str
        """
        return f"{self.coincidence}/{self.length}{self.language} {self.transcription}"
