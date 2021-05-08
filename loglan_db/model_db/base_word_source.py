# -*- coding: utf-8 -*-
"""
This module contains a basic WordSource Model
"""
import re
from loglan_db.model_db import t_name_word_sources


class BaseWordSource:
    """Word Source from BaseWord.origin for Prims"""
    __tablename__ = t_name_word_sources
    PATTERN_SOURCE = r"\d+\/\d+\w"

    def __init__(self, source):

        compatibility_search = re.search(self.PATTERN_SOURCE, source)

        if compatibility_search:
            self.coincidence = int(compatibility_search[0][:-1].split("/")[0])
            self.length = int(compatibility_search[0][:-1].split("/")[1])
            self.language = compatibility_search[0][-1:]
        else:
            self.coincidence = self.length = self.language = None

        transcription_search = re.search(rf"(?!{self.PATTERN_SOURCE}) .+", source)
        self.transcription = str(transcription_search[0]).strip() if transcription_search else None

    LANGUAGES = {
        "E": "English",
        "C": "Chinese",
        "H": "Hindi",
        "R": "Russian",
        "S": "Spanish",
        "F": "French",
        "J": "Japanese",
        "G": "German", }

    @property
    def as_string(self) -> str:
        """
        Format WordSource as string, for example, '3/5R mesto'
        Returns:
            str
        """
        if not all([self.coincidence, self.length, self.language, self.transcription]):
            return str()
        return f"{self.coincidence}/{self.length}{self.language} {self.transcription}"
