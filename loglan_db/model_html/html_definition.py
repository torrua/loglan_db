# -*- coding: utf-8 -*-
"""
This module contains a HTMLExportDefinition Model
"""
import re
from loglan_db.model_db.base_definition import BaseDefinition
from loglan_db.model_html import DEFAULT_HTML_STYLE


class DefinitionFormatter:
    """
    Additional methods for definition's formatting
    """
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
    def highlight_key(def_body, word, case_sensitive: bool = False) -> str:
        """
        Highlights the current key from the list, deselecting the rest
        :param def_body:
        :param word:
        :param case_sensitive:
        :return:
        """

        to_key = '<k>'  # key
        tc_key = '</k>'
        to_del = '<do_not_delete>'
        tc_del = '</do_not_delete>'

        key_pattern = f"{to_key}{word.replace('*', '.*')}{tc_key}"
        list_of_keys = def_body.replace("</k>", "</k>@").split("@")

        for key in list_of_keys:
            res = re.search(key_pattern, key, flags=0 if case_sensitive else re.IGNORECASE)
            if not res:
                continue
            original_key = res[0]
            replace_key = original_key.replace(to_key, to_del).replace(tc_key, tc_del)
            def_body = def_body.replace(original_key, replace_key)

        def_body = def_body.replace(tc_key, str()).replace(to_key, str())
        def_body = def_body.replace(to_del, to_key).replace(tc_del, tc_key)

        return def_body

    @staticmethod
    def tagged_word_origin_x(d_source_word, tag: str) -> str:
        """
        Generate Word.origin_x as HTML tag
        Args:
            d_source_word:
            tag:

        Returns:

        """
        w_origin_x = d_source_word.origin_x \
            if d_source_word.origin_x and d_source_word.type.group == "Cpx" else str()
        return tag % w_origin_x if w_origin_x else str()

    @staticmethod
    def tagged_word_name(usage: str, d_source_word, tag: str) -> str:
        """
        Generate Word.name as HTML tag
        Args:
            usage:
            d_source_word:
            tag:

        Returns:

        """
        w_name = d_source_word.name if not usage \
            else usage.replace("%", d_source_word.name)
        return tag % w_name

    @classmethod
    def tagged_definition_body(cls, body: str, key_word: str, tag: str) -> str:
        """
        Generate Definition.body as HTML tag with highlighted key word
        Args:
            body:
            key_word:
            tag:

        Returns:

        """
        definition_body = cls.format_body(body)
        definition_body = cls.highlight_key(definition_body, key_word)
        definition_body = tag % definition_body
        return definition_body


class HTMLExportDefinition(BaseDefinition, DefinitionFormatter):
    """
    HTMLExportDefinition Class
    """

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
            "ultra": [
                '(%s)', '[%s] ', ' %s', '<de>%s</de>',
                '<ld>%s</ld>', '<wn>%s</wn>, ', '<o>&lt;%s&gt;</o> ', ],
        }

        t_d_gram, t_d_tags, t_d_body, t_def, t_def_line, t_word_name, t_word_origin = tags[style]

        gram_form = self.stringer(self.slots) + self.grammar_code
        def_gram = t_d_gram % gram_form if gram_form else ''
        def_tags = t_d_tags % self.case_tags.replace("-", "&zwj;-&zwj;") if self.case_tags else ''

        def_body = self.tagged_definition_body(self.body, word, t_d_body)
        word_name = self.tagged_word_name(self.usage, self.source_word, t_word_name)
        word_origin_x = self.tagged_word_origin_x(self.source_word, t_word_origin)

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
                '<span class="du">%s</span> ', '<span class="dg">(%s)</span> ',
                '<span class="db">%s</span>', ' <span class="dt">[%s]</span>',
                f'<div class="definition log" id={self.id}>%s</div>', ],
            "ultra": ['<du>%s</du> ', '(%s) ', '%s', ' [%s]', '<dl>%s</dl>', ],
        }
        t_d_usage, t_d_gram, t_d_body, t_d_tags, t_definition = tags[style]

        def_usage = t_d_usage % self.usage.replace("%", "—") if self.usage else ''
        gram_form = f"{str(self.slots) if self.slots else ''}" + self.grammar_code
        def_gram = t_d_gram % gram_form if gram_form else ''
        def_body = t_d_body % self.format_body(self.body)
        def_tags = t_d_tags % self.case_tags.replace("-", "&zwj;-&zwj;") if self.case_tags else ''
        return t_definition % f'{def_usage}{def_gram}{def_body}{def_tags}'
