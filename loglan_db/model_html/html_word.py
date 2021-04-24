# -*- coding: utf-8 -*-
# pylint: disable=C0303
"""
This module contains a HTMLExportWord Model
"""
from __future__ import annotations
from itertools import groupby
from typing import Union, Optional, List, Dict
from dataclasses import dataclass

from sqlalchemy import or_
from flask_sqlalchemy import BaseQuery
from loglan_db.model_db.addons.addon_word_getter import AddonWordGetter
from loglan_db.model_db.base_event import BaseEvent
from loglan_db.model_db.base_word import BaseWord
from loglan_db.model_html import DEFAULT_HTML_STYLE
from loglan_db.model_html.html_definition import HTMLExportDefinition
from loglan_db.model_export import AddonExportWordConverter


@dataclass
class Meaning:
    mid: int
    technical: str
    definitions: List[str]
    used_in: str


class AddonWordTranslator:
    """
    Additional methods for HTMLExportWord class
    """
    @staticmethod
    def definitions_by_key(
            key: str, words: List[BaseWord], style: str = DEFAULT_HTML_STYLE) -> dict:
        """

        Args:
            key:
            words:
            style:

        Returns:

        """
        result: Dict[str, List[str]] = {}
        for word in words:
            result[word.name] = []
            definitions = [
                HTMLExportDefinition.export_for_english(d, word=key, style=style)
                for d in word.definitions if key.lower() in [key.word.lower() for key in d.keys]]
            result[word.name].extend(definitions)
        return result

    @staticmethod
    def translation_by_key(
            key: str, language: str = None,
            style: str = DEFAULT_HTML_STYLE,
            case_sensitive: bool = False) -> Optional[str]:
        """
        Get information about loglan words by key in a foreign language
        Args:
            key:
            language:
            style:
            case_sensitive:
        Returns:

        """

        words = HTMLExportWord.by_key(key, language, case_sensitive).order_by(HTMLExportWord.name).all()

        if not words:
            return None

        result = HTMLExportWord.definitions_by_key(key, words, style)

        new = '\n'

        return new.join([f"{new.join(definitions)}"
                         for _, definitions in result.items()]).strip()


class HTMLExportWord(BaseWord, AddonWordGetter, AddonWordTranslator, AddonExportWordConverter):
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

        words = cls.get_words_by(name, event_id, case_sensitive, partial_results)

        if not words:
            return None

        items = cls._get_stylized_words(words, style)

        return words_template[style] % "\n".join(items)

    @classmethod
    def get_words_by(
            cls, name: str, event_id: int,
            case_sensitive: bool, partial_results: bool) -> List[HTMLExportWord]:
        words = cls.query.filter(cls.event_start_id <= event_id) \
            .filter(or_(cls.event_end_id > event_id, cls.event_end_id.is_(None)))
        if case_sensitive:
            words = cls.__case_sensitive_words_filter(name, words, partial_results)
        else:
            words = cls.__case_insensitive_words_filter(name, words, partial_results)
        return words.order_by(cls.name).all()

    @classmethod
    def __case_sensitive_words_filter(
            cls, key: str, request: BaseQuery, partial_results: bool) -> BaseQuery:
        return request.filter(cls.name.like(f"{key}%")) \
            if partial_results else request.filter(cls.name == key)

    @classmethod
    def __case_insensitive_words_filter(
            cls, key: str, request: BaseQuery, partial_results: bool) -> BaseQuery:
        return request.filter(cls.name.ilike(f"{key}%")) \
            if partial_results else request.filter(cls.name.ilike(key))

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

    def meaning(self, style: str = DEFAULT_HTML_STYLE) -> Meaning:
        """
        :param style:
        :return:
        """
        html_affixes, html_match, html_rank,\
            html_source, html_type, html_used_in,\
            html_year, t_technical = self.get_styled_values(style)

        html_tech = t_technical % f'{html_match}{html_type}{html_source}{html_year}{html_rank}'
        html_tech = f'{html_affixes}{self.html_origin(style)}{html_tech}'
        return Meaning(self.id, html_tech, self.html_definitions(style), html_used_in)

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

        def _tagger(tag: str, value: Optional[str], default_value: Optional[str] = str()):
            return tag % value if value else default_value

        values = [self.e_affixes, self.match, self.rank, self.e_source, self.type.type,
                  self.e_usedin.replace("| ", "|&nbsp;"), self.e_year, None]
        default_values = [str(), str(), str(), str(), str(), None, str(), tags[style][-1]]

        return tuple([_tagger(tag, value, default_value) for tag, value, default_value in
                      zip(tags[style], values, default_values)])

    def html_meaning(self, style: str = DEFAULT_HTML_STYLE) -> str:
        """

        Args:
            style:

        Returns:

        """
        n_l = "\n"
        meaning = self.meaning(style)
        if style == "normal":
            used_in_list = f'<div class="used_in">Used In: ' \
                           f'{meaning.used_in}</div>\n</div>' \
                if meaning.used_in else "</div>"
            return f'<div class="meaning" id="{meaning.mid}">\n' \
                   f'<div class="technical">{meaning.technical}</div>\n' \
                   f'<div class="definitions">{n_l}' \
                   f'{n_l.join(meaning.definitions)}\n</div>\n{used_in_list}'

        used_in_list = f'<us>Used In: {meaning.used_in}</us>\n</m>' \
            if meaning.used_in else '</m>'
        return f'<m>\n<t>{meaning.technical}</t>\n' \
               f'<ds>{n_l}' \
               f'{n_l.join(meaning.definitions)}\n</ds>\n{used_in_list}'
