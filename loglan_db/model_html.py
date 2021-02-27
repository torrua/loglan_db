# -*- coding: utf-8 -*-
"""
HTML Export extensions of LOD database models
"""
import os
from itertools import groupby
from typing import Optional, Union, List

from sqlalchemy import or_

from loglan_db.model_db.base_event import BaseEvent
from loglan_db.model_export import ExportWord, ExportDefinition

DEFAULT_HTML_STYLE = os.getenv("DEFAULT_HTML_STYLE", "ultra")


class HTMLExportDefinition(ExportDefinition):
    """
    HTMLExportDefinition Class
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

        def _word_origin_x(d_source_word, tag):
            w_origin_x = d_source_word.origin_x \
                if d_source_word.origin_x and d_source_word.type.group == "Cpx" else ''
            return tag % w_origin_x if w_origin_x else ''

        def _word_name(usage, d_source_word, tag):
            w_name = d_source_word.name if not usage \
                else usage.replace("%", d_source_word.name)
            return tag % w_name

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

        def_body = HTMLExportDefinition.format_body(self.body)
        def_body = HTMLExportDefinition.highlight_key(def_body, word)
        def_body = t_d_body % def_body

        word_name = _word_name(self.usage, self.source_word, t_word_name)
        word_origin_x = _word_origin_x(self.source_word, t_word_origin)

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


class HTMLExportWord(ExportWord):
    """
    HTMLExportWord Class
    """

    @classmethod
    def html_all_by_name(
            cls, name: str, style: str = DEFAULT_HTML_STYLE,
            event_id: Union[BaseEvent, int, str] = None,
            case_sensitive: bool = False,
            partial_results: bool = False) -> Optional[str]:
        """
        Convert all words found by name into one HTML string
        Args:
            name: Name of the search word
            style: HTML design style
            event_id:
            case_sensitive:
            partial_results:
        Returns:

        """

        words_template = {
            "normal": '<div class="words">\n%s\n</div>\n',
            "ultra": '<ws>\n%s\n</ws>\n',
        }

        if not event_id:
            event_id = BaseEvent.latest().id

        event_id = int(event_id) if isinstance(event_id, (int, str)) else BaseEvent.id

        words = cls.query.filter(cls.event_start_id <= event_id) \
            .filter(or_(cls.event_end_id > event_id, cls.event_end_id.is_(None)))

        if case_sensitive:
            words = cls.__case_sensitive_words(name, words, partial_results)
        else:
            words = cls.__case_insensitive_words(name, words, partial_results)

        words = words.order_by(cls.name).all()

        if not words:
            return None

        items = cls._get_stylized_words(words, style)

        return words_template[style] % "\n".join(items)

    @classmethod
    def __case_insensitive_words(cls, name, words, partial_results):
        return words.filter(cls.name.ilike(f"{name}%")) \
            if partial_results else words.filter(cls.name.ilike(name))

    @classmethod
    def __case_sensitive_words(cls, name, words, partial_results):
        return words.filter(cls.name.like(f"{name}%")) \
            if partial_results else words.filter(cls.name == name)

    @staticmethod
    def _get_stylized_words(
            words: list, style: str = DEFAULT_HTML_STYLE) -> List[str]:
        """

        Args:
            words:
            style:

        Returns:

        """
        word_template = {
            "normal": '<div class="word" wid="%s">\n'
                      '<div class="word_line"><span class="word_name">%s</span>,</div>\n'
                      '<div class="meanings">\n%s\n</div>\n</div>',
            "ultra": '<w wid="%s"><wl>%s,</wl>\n<ms>\n%s\n</ms>\n</w>',
        }
        grouped_words = groupby(words, lambda ent: ent.name)
        group_words = {k: list(g) for k, g in grouped_words}
        items = []
        for word_name, words_list in group_words.items():
            meanings = "\n".join([word.html_meaning(style) for word in words_list])
            items.append(word_template[style] % (word_name.lower(), word_name, meanings))
        return items

    def html_origin(self, style: str = DEFAULT_HTML_STYLE):
        """

        Args:
            style:

        Returns:

        """
        orig = self.origin
        orig_x = self.origin_x

        if not (orig or orig_x):
            return str()

        origin = self.__generate_origin(orig, orig_x)

        if style == "normal":
            return f'<span class="m_origin">&lt;{origin}&gt;</span> '
        return f'<o>&lt;{origin}&gt;</o> '

    @staticmethod
    def __generate_origin(orig: str, orig_x: str) -> str:
        """
        Generate basic 'origin' string
        Args:
            orig:
            orig_x:

        Returns:

        """
        if not orig_x:
            return orig

        if not orig:
            return orig_x

        return f'{orig}={orig_x}'

    def html_definitions(self, style: str = DEFAULT_HTML_STYLE):
        """

        :param style:
        :return:
        """
        return [HTMLExportDefinition.export_for_loglan(
            d, style=style) for d in list(self.definitions)]

    def meaning(self, style: str = DEFAULT_HTML_STYLE) -> dict:
        """

        :param style:
        :return:
        """
        html_affixes, html_match, html_rank,\
            html_source, html_type, html_used_in,\
            html_year, t_technical = self.get_styled_values(style)

        html_tech = t_technical % f'{html_match}{html_type}{html_source}{html_year}{html_rank}'
        html_tech = f'{html_affixes}{self.html_origin(style)}{html_tech}'

        return {
            "mid": self.id,
            "technical": html_tech,
            "definitions": self.html_definitions(style),
            "used_in": html_used_in
        }

    def get_styled_values(self, style: str = DEFAULT_HTML_STYLE) -> tuple:
        """

        Args:
            style:

        Returns:

        """
        tags = {
            "normal": [
                '<span class="m_afx">%s</span> ', '<span class="m_match">%s</span> ',
                '<span class="m_rank">%s</span>', '<span class="m_author">%s</span> ',
                '<span class="m_type">%s</span> ', '<span class="m_use">%s</span>',
                '<span class="m_year">%s</span> ', '<span class="m_technical">%s</span>'],
            "ultra": [
                '<afx>%s</afx> ', '%s ', '%s', '%s ', '%s ',
                '<use>%s</use>', '%s ', '<tec>%s</tec>'],
        }

        def _stringer(tag: str, value: Optional[str], default_value: Optional[str] = str()):
            return tag % value if value else default_value

        # t_afx, t_match, t_type, t_author, t_year, t_rank, t_use, t_technical = tags[style]
        values = [self.e_affixes, self.match, self.rank, self.e_source, self.type.type,
                  self.e_usedin.replace("| ", "|&nbsp;"), self.e_year, None]
        default_values = [str(), str(), str(), str(), str(), None, str(), tags[style][-1]]

        return tuple([_stringer(tag, value, default_value) for tag, value, default_value in
                      zip(tags[style], values, default_values)])

    def html_meaning(self, style: str = DEFAULT_HTML_STYLE) -> str:
        """

        Args:
            style:

        Returns:

        """
        n_l = "\n"
        meaning_dict = self.meaning(style)
        if style == "normal":
            used_in_list = f'<div class="used_in">Used In: ' \
                           f'{meaning_dict.get("used_in")}</div>\n</div>' \
                if meaning_dict.get("used_in") else "</div>"
            return f'<div class="meaning" id="{meaning_dict.get("mid")}">\n' \
                   f'<div class="technical">{meaning_dict.get("technical")}</div>\n' \
                   f'<div class="definitions">{n_l}' \
                   f'{n_l.join(meaning_dict.get("definitions"))}\n</div>\n{used_in_list}'

        used_in_list = f'<us>Used In: {meaning_dict.get("used_in")}</us>\n</m>' \
            if meaning_dict.get("used_in") else '</m>'
        return f'<m>\n<t>{meaning_dict.get("technical")}</t>\n' \
               f'<ds>{n_l}' \
               f'{n_l.join(meaning_dict.get("definitions"))}\n</ds>\n{used_in_list}'

    @classmethod
    def translation_by_key(
            cls, key: str, language: str = None,
            style: str = DEFAULT_HTML_STYLE) -> Optional[str]:
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

        result = cls.__definitions_by_key(key, words, style)

        new = '\n'

        return new.join([f"{new.join(definitions)}"
                         for _, definitions in result.items()]).strip()

    @classmethod
    def __definitions_by_key(cls, key, words, style):
        result = {}
        for word in words:
            result[word.name] = []
            definitions = [
                HTMLExportDefinition.export_for_english(d, word=key, style=style)
                for d in word.definitions if key.lower() in [key.word.lower() for key in d.keys]]
            result[word.name].extend(definitions)
        return result
