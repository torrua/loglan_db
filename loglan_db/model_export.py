# -*- coding: utf-8 -*-
"""
Export extensions of LOD database models
Add export() function to db object for returning its text string presentation
"""

from loglan_db.model_base import BaseAuthor, BaseEvent, BaseSyllable, \
    BaseSetting, BaseType, BaseWord, BaseDefinition, BaseWordSpell


class ExportAuthor(BaseAuthor):
    def export(self):
        return f"{self.abbreviation}@{self.full_name}@{self.notes}"


class ExportEvent(BaseEvent):
    def export(self):
        return f"{self.id}@{self.name}" \
               f"@{self.date.strftime('%m/%d/%Y')}@{self.definition}" \
               f"@{self.annotation}@{self.suffix}"


class ExportSyllable(BaseSyllable):
    def export(self):
        return f"{self.name}@{self.type}@{self.allowed}"


class ExportSetting(BaseSetting):
    def export(self):
        return f"{self.date.strftime('%d.%m.%Y %H:%M:%S')}@{self.db_version}@{self.last_word_id}@{self.db_release}"


class ExportType(BaseType):
    def export(self):
        return f"{self.type}@{self.type_x}@{self.group}@{self.parentable}" \
               f"@{self.description if self.description else ''}"


class ExportWord(BaseWord):
    @property
    def e_affixes(self) -> str:
        w_affixes = self.affixes
        return ' '.join(sorted({afx.name.replace("-", "") for afx in w_affixes})) if w_affixes else ""

    @property
    def e_source(self) -> str:
        notes = self.notes if self.notes else {}
        w_source = self.authors.all()
        # print(self) if not self.authors.all() else None
        source = '/'.join(sorted([auth.abbreviation for auth in w_source])) \
            if len(w_source) > 1 else w_source[0].abbreviation
        return source + (" " + notes["author"] if notes.get("author", False) else "")

    @property
    def e_year(self) -> str:
        notes = self.notes if self.notes else {}
        return str(self.year.year) + (" " + notes["year"] if notes.get("year", False) else "")

    @property
    def e_usedin(self):
        w_usedin = self.complexes
        return ' | '.join(sorted({cpx.name for cpx in w_usedin})) if w_usedin else ""

    def export(self):
        """
                Prepare Word data for exporting to text file
                :return: Formatted basic string
                """
        notes = self.notes if self.notes else {}
        w_match = self.match
        match = w_match if w_match else ""
        rank = self.rank + (" " + notes["rank"] if notes.get("rank", False) else "")
        tid_old = self.TID_old if self.TID_old else ""
        origin_x = self.origin_x if self.origin_x else ""
        origin = self.origin if self.origin else ""
        return f"{self.id_old}@{self.type.type}@{self.type.type_x}@{self.e_affixes}" \
               f"@{match}@{self.e_source}@{self.e_year}@{rank}" \
               f"@{origin}@{origin_x}@{self.e_usedin}@{tid_old}"


class ExportDefinition(BaseDefinition):
    def export(self):
        return f"{self.source_word.id_old}@{self.position}@{self.usage if self.usage else ''}" \
               f"@{self.slots if self.slots else ''}" \
               f"{self.grammar_code if self.grammar_code else ''}" \
               f"@{self.body}@@{self.case_tags if self.case_tags else ''}"


class ExportWordSpell(BaseWordSpell, BaseWord):
    def export(self):
        """
        Prepare Word Spell data for exporting to text file
        :return: Formatted basic string
        """
        code_name = "".join(["0" if symbol.isupper() else "5" for symbol in self.name])

        return f"{self.id_old}@{self.name}@{self.name.lower()}@{code_name}" \
               f"@{self.event_start_id}@{self.event_end_id if self.event_end else 9999}@"


export_models_pg = (
    ExportAuthor, ExportDefinition, ExportEvent, ExportSetting,
    ExportSyllable, ExportType, ExportWord, ExportWordSpell, )
