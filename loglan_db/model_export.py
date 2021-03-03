# -*- coding: utf-8 -*-
"""
This module contains an "Export extensions" for LOD dictionary SQL model.
Add export() function to db object for returning its text string presentation.
"""

from loglan_db.model_db.base_word import BaseWord
from loglan_db.model_db.base_word_spell import BaseWordSpell
from loglan_db.model_db.base_definition import BaseDefinition
from loglan_db.model_db.base_type import BaseType
from loglan_db.model_db.base_syllable import BaseSyllable
from loglan_db.model_db.base_setting import BaseSetting
from loglan_db.model_db.base_event import BaseEvent
from loglan_db.model_db.base_author import BaseAuthor


class ExportAuthor(BaseAuthor):
    """
    ExportAuthor Class
    """
    def export(self) -> str:
        """
        Prepare Author data for exporting to text file
        Returns:
            Formatted basic string
        """
        return f"{self.abbreviation}@{self.full_name}@{self.notes}"


class ExportEvent(BaseEvent):
    """
    ExportEvent Class
    """
    def export(self) -> str:
        """
        Prepare Event data for exporting to text file
        Returns:
            Formatted basic string
        """
        return f"{self.id}@{self.name}" \
               f"@{self.date.strftime('%m/%d/%Y')}@{self.definition}" \
               f"@{self.annotation}@{self.suffix}"


class ExportSyllable(BaseSyllable):
    """
    ExportSyllable Class
    """
    def export(self) -> str:
        """
        Prepare Syllable data for exporting to text file
        Returns:
            Formatted basic string
        """
        return f"{self.name}@{self.type}@{self.allowed}"


class ExportSetting(BaseSetting):
    """
    ExportSetting Class
    """
    def export(self) -> str:
        """
        Prepare Setting data for exporting to text file
        Returns:
            Formatted basic string
        """
        return f"{self.date.strftime('%d.%m.%Y %H:%M:%S')}" \
               f"@{self.db_version}" \
               f"@{self.last_word_id}" \
               f"@{self.db_release}"


class ExportType(BaseType):
    """
    ExportType Class
    """
    def export(self) -> str:
        """
        Prepare Type data for exporting to text file
        Returns:
            Formatted basic string
        """
        return f"{self.type}@{self.type_x}@{self.group}@{self.parentable}" \
               f"@{self.description if self.description else ''}"


class AddonExportWordConverter:
    """
    Addon for ExportWord class with converters for properties
    """
    notes = None
    authors = None
    year = None
    complexes = None
    affixes = None
    rank = None

    @property
    def e_source(self) -> str:
        """
        Returns:
        """
        notes = self.notes if self.notes else {}
        w_source = self.authors.all()
        # print(self) if not self.authors.all() else None
        source = '/'.join(sorted([auth.abbreviation for auth in w_source])) \
            if len(w_source) > 1 else w_source[0].abbreviation
        return source + (" " + notes["author"] if notes.get("author", False) else "")

    @property
    def e_year(self) -> str:
        """
        Returns:
        """
        notes = self.notes if self.notes else {}
        return str(self.year.year) + (" " + notes["year"] if notes.get("year", False) else "")

    @property
    def e_usedin(self) -> str:
        """
        Returns:
        """
        w_usedin = list(self.complexes)
        return ' | '.join(sorted({cpx.name for cpx in w_usedin})) if w_usedin else ""

    @property
    def e_affixes(self) -> str:
        """
        Returns:
        """
        w_affixes = list(self.affixes)
        return ' '.join(sorted(
            {afx.name.replace("-", "") for afx in w_affixes}
        )) if w_affixes else ""

    @property
    def e_rank(self):
        """
        Returns:
        """
        notes = self.notes if self.notes else {}
        return self.rank + (" " + notes["rank"] if notes.get("rank", None) else "")


class ExportWord(BaseWord, AddonExportWordConverter):
    """
    ExportWord Class
    """

    def export(self) -> str:
        """
        Prepare Word data for exporting to text file
        Returns:
            Formatted basic string
        """

        match = self.stringer(self.match)
        tid_old = self.stringer(self.TID_old)
        origin_x = self.stringer(self.origin_x)
        origin = self.stringer(self.origin)

        return f"{self.id_old}@{self.type.type}@{self.type.type_x}@{self.e_affixes}" \
               f"@{match}@{self.e_source}@{self.e_year}@{self.e_rank}" \
               f"@{origin}@{origin_x}@{self.e_usedin}@{tid_old}"


class ExportDefinition(BaseDefinition):
    """
    ExportDefinition Class
    """
    @property
    def e_grammar(self) -> str:
        """
        Prepare grammar data for export
        Returns:
            Formatted string
        """
        return f"{self.slots if self.slots else ''}" \
            f"{self.grammar_code if self.grammar_code else ''}"

    def export(self) -> str:
        """
        Prepare Definition data for exporting to text file
        Returns:
            Formatted basic string
        """
        return f"{self.source_word.id_old}@{self.position}@{self.usage if self.usage else ''}" \
               f"@{self.e_grammar}@{self.body}@@{self.case_tags if self.case_tags else ''}"


class ExportWordSpell(BaseWordSpell, BaseWord):
    """
    ExportWordSpell Class
    """
    def export(self) -> str:
        """
        Prepare WordSpell data for exporting to text file
        Returns:
            Formatted basic string
        """
        code_name = "".join(["0" if symbol.isupper() else "5" for symbol in str(self.name)])

        return f"{self.id_old}@{self.name}@{self.name.lower()}@{code_name}" \
               f"@{self.event_start_id}@{self.event_end_id if self.event_end else 9999}@"


export_models_pg = (
    ExportAuthor, ExportDefinition, ExportEvent, ExportSetting,
    ExportSyllable, ExportType, ExportWord, ExportWordSpell, )
