# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903

"""HTML Model unit tests."""

import pytest

from loglan_db.model import Type, Author
from loglan_db.model_html import HTMLExportWord as Word, HTMLExportDefinition as Definition
from tests.data import definitions, words, types, authors, word_1, connect_authors, connect_words
from tests.functions import db_add_and_return, db_add_objects, db_connect_authors, db_connect_words


@pytest.mark.usefixtures("db")
class TestDefinition:
    """Definition tests."""

    def test_format_body(self):
        """
        Test formatting definition's body.
        This method replace some punctuation signs
        and specific marks with HTML tags.
        """
        string_1 = "<test string>"
        string_2 = "«test string»"
        string_3 = "{test string}"
        string_4 = "test string..."
        string_5 = "test -- string"

        assert Definition.format_body(string_1) == "&lt;test string&gt;"
        assert Definition.format_body(string_2) == "<k>test string</k>"
        assert Definition.format_body(string_3) == "<l>test string</l>"
        assert Definition.format_body(string_4) == "test string…"
        assert Definition.format_body(string_5) == "test — string"

    def test_highlight_key(self):
        """
        Test highlighting specified key in definition's body.
        """
        def_body = 'K <k>test</k>/<k>examine</k> B for P with test V.'
        result = Definition.highlight_key(def_body, "test")

        assert result == "K <k>test</k>/examine B for P with test V."

    def test_export_for_english(self):
        """Test exporting definition as HTML block for E-L Dictionary"""
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_add_objects(Definition, definitions)
        definition = Definition.get_by_id(13527)

        result = definition.export_for_english(word="test", style="ultra")
        assert result == "<ld><wn>prukao</wn>, <o>&lt;test act&gt;</o> <d>[K&zwj;-&zwj;BPV]" \
                         " (4v) K <k>test</k>/examine B for P with test V.</d></ld>"

        result = definition.export_for_english(word="test", style="normal")
        assert result == '<div class="d_line"><span class="w_name">prukao</span>, ' \
                         '<span class="w_origin">&lt;test act&gt;</span> ' \
                         '<span class="definition" id=13527><span class="dt">' \
                         '[K&zwj;-&zwj;BPV]</span> <span class="dg">(4v)</span>' \
                         ' <span class="db">K <k>test</k>/examine ' \
                         'B for P with test V.</span></span></div>'

    def test_export_for_loglan(self):
        """Test exporting definition as HTML block for L-E Dictionary"""
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_add_objects(Definition, definitions)
        definition = Definition.get_by_id(13527)

        result = definition.export_for_loglan(style="ultra")
        assert result == "<d>(4v) K <k>test</k>/<k>examine</k> " \
                         "B for P with test V. [K&zwj;-&zwj;BPV]</d>"

        result = definition.export_for_loglan(style="normal")
        assert result == '<div class="definition" id=13527><span class="dg">' \
                         '(4v)</span> <span class="db">K <k>test</k>/' \
                         '<k>examine</k> B for P with test V.</span> ' \
                         '<span class="dt">[K&zwj;-&zwj;BPV]</span></div>'


@pytest.mark.usefixtures("db")
class TestWord:
    """Word tests."""

    def test_html_origin(self):
        """Test formatting 'origin' field as HTML block"""
        word = db_add_and_return(Word, word_1)

        result = word.html_origin(style="ultra")
        assert result == "<o>&lt;pru(ci)+ka(kt)o=test act&gt;</o> "

        result = word.html_origin(style="normal")
        assert result == '<span class="m_origin">&lt;pru(ci)+ka(kt)o=test act&gt;</span> '

    def test_html_definitions(self):
        """Test exporting word's definitions as a list of HTML strings"""
        db_add_objects(Word, words)
        db_add_objects(Definition, definitions)
        word = Word.get_by_id(7315)

        result = word.html_definitions(style="ultra")
        assert isinstance(result, list)
        assert len(result) == 4
        assert result[0] == "<d>(3n) V is a <k>test</k>/<k>examination</k> " \
                            "for property B in any member of class F. [V&zwj;-&zwj;BF]</d>"

        result = word.html_definitions(style="normal")
        assert isinstance(result, list)
        assert len(result) == 4
        assert result[0] == '<div class="definition" id=13523><span class="dg">' \
                            '(3n)</span> <span class="db">V is a <k>test</k>/' \
                            '<k>examination</k> for property B in any member of class F.' \
                            '</span> <span class="dt">[V&zwj;-&zwj;BF]</span></div>'

    def test_meaning(self):
        """Test generating data for word's HTML block"""
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_add_objects(Author, authors)
        db_add_objects(Definition, definitions)
        db_connect_authors(connect_authors)
        db_connect_words(connect_words)
        word = Word.get_by_id(7315)

        result = word.meaning(style="ultra")
        expected_value = {
            'mid': 7315,
            'technical': '<afx>pru</afx> <o>&lt;3/4E prove | 2/4C sh yen |'
                         ' 3/6S prueba | 2/5R proba | 2/5F epreuve | 2/5G probe |'
                         ' 2/6J tameshi&gt;</o> <tec>49% C-Prim L4 1975 1.9</tec>',
            'definitions': [
                '<d>(3n) V is a <k>test</k>/<k>examination</k> for property '
                'B in any member of class F. [V&zwj;-&zwj;BF]</d>',
                '<d>(vt) <k>test</k>, test for … a property … in a member of ….</d>',
                '<d><du>fu —</du> (a) <k>testable</k>, of classes with -able members.</d>',
                '<d><du>nu —</du> (a) <k>testable</k>, of testable properties.</d>'],
            'used_in': '<use>prukao</use>'}
        assert isinstance(result, dict)
        assert result == expected_value

        word = Word.get_by_id(3802)

        result = word.meaning(style="normal")
        expected_value = {
            'mid': 3802,
            'technical': '<span class="m_origin">&lt;kak(to)&gt;</span> <span class="m_technical">'
                         '<span class="m_type">Afx</span> <span class="m_author">JCB</span> '
                         '<span class="m_year">1988</span> <span class="m_rank">7+</span></span>',
            'definitions': ['<div class="definition" id=7240><span class="dg">(af)'
                            '</span> <span class="db">a combining form of '
                            '<l>kakto</l>, <k>act</k>.</span></div>'],
            'used_in': None}

        assert isinstance(result, dict)
        assert result == expected_value
