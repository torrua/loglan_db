# -*- coding: utf-8 -*-
"""
This module contains an addon for basic Word Model,
which makes it possible to work with word's sources
"""
import re
from typing import Optional, List, Union
from flask_sqlalchemy import BaseQuery

from loglan_db.model_db.base_type import BaseType
from loglan_db.model_db.base_word import BaseWord
from loglan_db import db
from loglan_db.model_db.base_word_source import BaseWordSource


class AddonWordSourcer:
    """AddonWordSourcer Model"""

    type: BaseType = None
    name: db.Column = None
    origin: db.Column = None
    origin_x: db.Column = None
    type_id: db.Column = None
    query: BaseQuery = None

    def get_sources_prim(self):
        """

        Returns:

        """
        # existing_prim_types = ["C", "D", "I", "L", "N", "O", "S", ]

        if not self.type.group == "Prim":
            return None

        prim_type = self.type.type[:1]

        if prim_type == "C":
            return self._get_sources_c_prim()

        return f"{self.name}: {self.origin}{' < ' + self.origin_x if self.origin_x else ''}"

    def _get_sources_c_prim(self) -> Optional[List[BaseWordSource]]:
        """

        Returns:

        """
        if self.type.type != "C-Prim":
            return None

        pattern_source = r"\d+\/\d+\w"
        sources = str(self.origin).split(" | ")
        word_sources = []

        for source in sources:
            compatibility = re.search(pattern_source, source)[0]
            c_l = compatibility[:-1].split("/")
            transcription = (re.search(rf"(?!{pattern_source}) .+", source)[0]).strip()
            word_source = BaseWordSource(**{
                "coincidence": int(c_l[0]),
                "length": int(c_l[1]),
                "language": compatibility[-1:],
                "transcription": transcription, })
            word_sources.append(word_source)

        return word_sources

    def get_sources_cpx(self, as_str: bool = False) -> List[Union[str, BaseWord]]:
        """Extract source words from self.origin field accordingly
        Args:
            as_str (bool): return BaseWord objects if False else as simple str
            (Default value = False)
        Example:
            'foldjacea' > ['forli', 'djano', 'cenja']
        Returns:
            List of words from which the self.name was created

        """

        # these prims have switched djifoas like 'flo' for 'folma'
        switch_prims = [
            'canli', 'farfu', 'folma', 'forli', 'kutla', 'marka',
            'mordu', 'sanca', 'sordi', 'suksi', 'surna']

        if not self.type.group == "Cpx":
            return []

        sources = self._prepare_sources_cpx()

        result = self.words_from_source_cpx(sources)

        if not as_str:
            return result

        result_as_str = []
        _ = [result_as_str.append(r) for r in sources if r not in result_as_str]
        return result_as_str

    @classmethod
    def words_from_source_cpx(cls, sources: List[str]) -> List[BaseWord]:
        """

        Args:
            sources:

        Returns:

        """
        exclude_type_ids = [t.id for t in BaseType.by(["LW", "Cpd"]).all()]
        return cls.query \
            .filter(cls.name.in_(sources)) \
            .filter(cls.type_id.notin_(exclude_type_ids)).all()

    def _prepare_sources_cpx(self) -> List[str]:
        """
        # TODO
        Returns:

        """
        sources = self.origin.replace("(", "").replace(")", "").replace("/", "")
        sources = sources.split("+")
        sources = [
            s if not s.endswith(("r", "h")) else s[:-1]
            for s in sources if s not in ["y", "r", "n"]]
        return sources

    def get_sources_cpd(self, as_str: bool = False) -> List[Union[str, BaseWord]]:
        """Extract source words from self.origin field accordingly

        Args:
          as_str: bool: return BaseWord objects if False else as simple str
          (Default value = False)

        Returns:
          List of words from which the self.name was created

        """

        if not self.type.type == "Cpd":
            return []

        sources = self._prepare_sources_cpd()

        result = self.words_from_source_cpd(sources)

        if not as_str:
            return result

        result_as_str = []

        _ = [result_as_str.append(r) for r in sources if r not in result_as_str and r]

        return result_as_str

    def _prepare_sources_cpd(self) -> List[str]:
        """

        Returns:

        """
        sources = self.origin.replace("(", "").replace(")", "").replace("/", "").replace("-", "")
        sources = [s.strip() for s in sources.split("+")]
        return sources

    @classmethod
    def words_from_source_cpd(cls, sources: List[str]) -> List:
        """

        Args:
            sources:

        Returns:

        """
        type_ids = [t.id for t in BaseType.by(["LW", "Cpd"]).all()]
        return cls.query.filter(cls.name.in_(sources)) \
            .filter(cls.type_id.in_(type_ids)).all()
