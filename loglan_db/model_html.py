# -*- coding: utf-8 -*-
"""
HTML Export extensions of LOD database models
"""
import os
from typing import Optional
from loglan_db.model_export import ExportWord, ExportDefinition

DEFAULT_HTML_STYLE = os.getenv("DEFAULT_HTML_STYLE", "ultra")


class HTMLExportDefinition(ExportDefinition):

    @staticmethod
    def format_body(body: str) -> str:
        """
        Substitutes tags in the definition's body
        Formats punctuation signs
        :param body:
        :return:
        """
        to_key = '<k>'  # key
        tc_key = '</k>'
        to_log = '<l>'  # log
        tc_log = '</l>'

        return body \
            .replace("<", "&lt;").replace(">", "&gt;") \
            .replace("«", to_key).replace("»", tc_key) \
            .replace("{", to_log).replace("}", tc_log) \
            .replace("...", "…").replace("--", "—")

    @staticmethod
    def highlight_key(def_body, word) -> str:
        """
        Highlights the current key from the list, deselecting the rest
        :param def_body:
        :param word:
        :return:
        """

        to_key = '<k>'  # key
        tc_key = '</k>'

        word_template_original = f'{to_key}{word}{tc_key}'
        word_template_temp = f'<do_not_delete>{word}</do_not_delete>'
        def_body = def_body.replace(word_template_original, word_template_temp)
        def_body = def_body.replace(to_key, "").replace(tc_key, "")
        def_body = def_body.replace(word_template_temp, word_template_original)
        return def_body

    def export_for_english(self, word: str, style: str = DEFAULT_HTML_STYLE) -> str:
        """

        :param word:
        :param style:
        :return:
        """
        # de = definition english
        tags = {
            "normal": [
                '<span class="dg">(%s)</span>',
                '<span class="dt">[%s]</span> ',
                ' <span class="db">%s</span>',
                f'<span class="definition eng" id={self.id}>%s</span>',
                '<div class="d_line">%s</div>',
                '<span class="w_name">%s</span>, ',
                '<span class="w_origin">&lt;%s&gt;</span> ',
            ],
            "ultra": ['(%s)', '[%s] ', ' %s', '<de>%s</de>', '<ld>%s</ld>', '<wn>%s</wn>, ', '<o>&lt;%s&gt;</o> ', ],
        }
        t_d_gram, t_d_tags, t_d_body, t_def, t_def_line, t_word_name, t_word_origin = tags[style]

        gram_form = f'{str(self.slots) if self.slots else ""}' + self.grammar_code
        def_gram = t_d_gram % gram_form if gram_form else ''
        def_tags = t_d_tags % self.case_tags.replace("-", "&zwj;-&zwj;") if self.case_tags else ''

        def_body = HTMLExportDefinition.format_body(self.body)
        def_body = HTMLExportDefinition.highlight_key(def_body, word)
        def_body = t_d_body % def_body

        d_source_word = self.source_word
        w_name = d_source_word.name if not self.usage else self.usage.replace("%", d_source_word.name)
        word_name = t_word_name % w_name

        w_origin_x = d_source_word.origin_x if d_source_word.origin_x and d_source_word.type.group == "Cpx" else ''
        word_origin_x = t_word_origin % w_origin_x if w_origin_x else ''

        definition = t_def % f'{def_tags}{def_gram}{def_body}'
        return t_def_line % f'{word_name}{word_origin_x}{definition}'

    def export_for_loglan(self, style: str = DEFAULT_HTML_STYLE) -> str:
        """

        :param style:
        :return:
        """
        tags = {
            # usage, gram, body, tags, definition
            "normal": [
                '<span class="du">%s</span> ', '<span class="dg">(%s)</span> ', '<span class="db">%s</span>',
                ' <span class="dt">[%s]</span>', f'<div class="definition log" id={self.id}>%s</div>', ],
            "ultra": ['<du>%s</du> ', '(%s) ', '%s', ' [%s]', '<dl>%s</dl>', ],
        }
        t_d_usage, t_d_gram, t_d_body, t_d_tags, t_definition = tags[style]

        def_usage = t_d_usage % self.usage.replace("%", "—") if self.usage else ''
        gram_form = f"{str(self.slots) if self.slots else ''}" + self.grammar_code
        def_gram = t_d_gram % gram_form if gram_form else ''
        def_body = t_d_body % HTMLExportDefinition.format_body(self.body)
        def_tags = t_d_tags % self.case_tags.replace("-", "&zwj;-&zwj;") if self.case_tags else ''
        return t_definition % f'{def_usage}{def_gram}{def_body}{def_tags}'


class HTMLExportWord(ExportWord):
    """

    """

    @classmethod
    def html_all_by_name(cls, name: str, style: str = DEFAULT_HTML_STYLE) -> Optional[str]:
        """
        Convert all words found by name into one HTML string
        Args:
            name: Name of the search word
            style: HTML design style

        Returns:

        """
        words = cls.by_name(name=name).all()

        if not words:
            return None

        meanings = "\n".join([word.html_meaning(style) for word in words])

        if style == "normal":
            return f'<div class="word" wid="{words[0].name.lower()}">\n' \
                   f'<div class="word_line"><span class="word_name">{words[0].name}</span>,</div>\n' \
                   f'<div class="meanings">\n{meanings}\n</div>\n</div>'
        else:
            return f'<w wid="{words[0].name.lower()}"><wl>{words[0].name},</wl>\n' \
                   f'<ms>\n{meanings}\n</ms>\n</w>'

    def html_origin(self, style: str = DEFAULT_HTML_STYLE):
        """

        :param style:
        :return:
        """
        o = self.origin
        ox = self.origin_x

        if (not o) and (not ox):
            return ''

        if not ox:
            origin = o
        elif not o:
            origin = ox
        else:
            origin = f'{o}={ox}'

        if style == "normal":
            return f'<span class="m_origin">&lt;{origin}&gt;</span> '
        else:
            return f'<o>&lt;{origin}&gt;</o> '

    def html_definitions(self, style: str = DEFAULT_HTML_STYLE):
        """

        :param style:
        :return:
        """
        return [HTMLExportDefinition.export_for_loglan(d, style=style) for d in self.definitions]

    def meaning(self, style: str = DEFAULT_HTML_STYLE) -> dict:
        """

        :param style:
        :return:
        """
        tags = {
            "normal": [
                '<span class="m_afx">%s</span> ', '<span class="m_match">%s</span> ',
                '<span class="m_type">%s</span> ', '<span class="m_author">%s</span> ',
                '<span class="m_year">%s</span> ', '<span class="m_rank">%s</span>',
                '<span class="m_use">%s</span>', '<span class="m_technical">%s</span>'],
            "ultra": ['<afx>%s</afx> ', '%s ', '%s ', '%s ', '%s ', '%s', '<use>%s</use>', '<tec>%s</tec>'],
        }
        t_afx, t_match, t_type, t_author, t_year, t_rank, t_use, t_technical = tags[style]

        html_affixes = t_afx % self.e_affixes if self.e_affixes else ''
        html_match = t_match % self.match if self.match else ''
        html_type = t_type % self.type.type if self.type.type else ''
        html_source = t_author % self.e_source if self.e_source else ''
        html_year = t_year % self.e_year if self.e_year else ''
        html_rank = t_rank % self.rank if self.rank else ''
        html_usedin = t_use % self.e_usedin.replace("| ", "|&nbsp;") if self.e_usedin else None

        html_tech = t_technical % f'{html_match}{html_type}{html_source}{html_year}{html_rank}'
        html_tech = f'{html_affixes}{self.html_origin(style)}{html_tech}'

        return {
            "mid": self.id,
            "technical": html_tech,
            "definitions": self.html_definitions(style),
            "used_in": html_usedin
        }

    def html_meaning(self, style: str = DEFAULT_HTML_STYLE) -> str:
        n_l = "\n"
        meaning_dict = self.meaning(style)
        if style == "normal":
            used_in_list = f'<div class="used_in">Used In: {meaning_dict.get("used_in")}</div>\n</div>' \
                if meaning_dict.get("used_in") else "</div>"
            return f'<div class="meaning" id="{meaning_dict.get("mid")}">\n' \
                   f'<div class="technical">{meaning_dict.get("technical")}</div>\n' \
                   f'<div class="definitions">{n_l}' \
                   f'{n_l.join(meaning_dict.get("definitions"))}\n</div>\n{used_in_list}'

        else:
            used_in_list = f'<us>Used In: {meaning_dict.get("used_in")}</us>\n</m>' \
                if meaning_dict.get("used_in") else '</m>'
            return f'<m>\n<t>{meaning_dict.get("technical")}</t>\n' \
                   f'<ds>{n_l}' \
                   f'{n_l.join(meaning_dict.get("definitions"))}\n</ds>\n{used_in_list}'

    @classmethod
    def translation_by_key(cls, key: str, language: str = None, style: str = DEFAULT_HTML_STYLE) -> Optional[str]:
        """
        Get information about loglan words by key in a foreign language
        Args:
            key:
            language:
            style:

        Returns:

        """

        words = cls.by_key(key, language).order_by(cls.name).all()

        if not words:
            return None

        result = {}

        for word in words:
            result[word.name] = []
            definitions = [HTMLExportDefinition.export_for_english(d, word=key, style=style) for d in word.definitions if key.lower() in [key.word.lower() for key in d.keys]]
            result[word.name].extend(definitions)

        new = '\n'

        from pprint import pprint
        pprint(result)
        return new.join([f"{new.join(definitions)}"
                         for _, definitions in result.items()]).strip()
