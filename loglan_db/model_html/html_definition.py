# -*- coding: utf-8 -*-
"""
This module contains a HTMLExportDefinition Model
"""
from loglan_db.model_export import ExportDefinition
from loglan_db.model_html import DEFAULT_HTML_STYLE


class DefinitionFormatter:
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

    @staticmethod
    def tagged_word_origin_x(d_source_word, tag):
        w_origin_x = d_source_word.origin_x \
            if d_source_word.origin_x and d_source_word.type.group == "Cpx" else str()
        return tag % w_origin_x if w_origin_x else str()

    @staticmethod
    def tagged_word_name(usage, d_source_word, tag):
        w_name = d_source_word.name if not usage \
            else usage.replace("%", d_source_word.name)
        return tag % w_name

    @staticmethod
    def tagged_definition_body(body, key_word, tag):
        definition_body = HTMLExportDefinition.format_body(body)
        definition_body = HTMLExportDefinition.highlight_key(definition_body, key_word)
        definition_body = tag % definition_body
        return definition_body


class HTMLExportDefinition(ExportDefinition, DefinitionFormatter):
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

        gram_form = f'{str(self.slots) if self.slots else ""}' + self.grammar_code
        def_gram = t_d_gram % gram_form if gram_form else ''
        def_tags = t_d_tags % self.case_tags.replace("-", "&zwj;-&zwj;") if self.case_tags else ''

        def_body = HTMLExportDefinition.tagged_definition_body(self.body, word, t_d_body)
        word_name = HTMLExportDefinition.tagged_word_name(self.usage, self.source_word, t_word_name)
        word_origin_x = HTMLExportDefinition.tagged_word_origin_x(self.source_word, t_word_origin)

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
        def_body = t_d_body % HTMLExportDefinition.format_body(self.body)
        def_tags = t_d_tags % self.case_tags.replace("-", "&zwj;-&zwj;") if self.case_tags else ''
        return t_definition % f'{def_usage}{def_gram}{def_body}{def_tags}'
