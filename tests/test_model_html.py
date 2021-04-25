# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903

"""HTML Model unit tests."""

import pytest

from loglan_db.model import Type, Author, Key, Event
from loglan_db.model_html.html_word import HTMLExportWord, Meaning
from loglan_db.model_html.html_definition import HTMLExportDefinition as Definition
from tests.data import definitions, words, types, authors, events
from tests.data import word_1, connect_authors, connect_words, keys, connect_keys
from tests.functions import db_add_and_return, db_add_objects, \
    db_connect_authors, db_connect_words, db_connect_keys
from loglan_db.model_db.addons.addon_word_getter import AddonWordGetter


class Word(HTMLExportWord, AddonWordGetter):
    """HTMLExportWord class with Getter addon"""


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
        assert result == "<ld><wn>prukao</wn>, <o>&lt;test act&gt;</o> <de>[K&zwj;-&zwj;BPV]" \
                         " (4v) K <k>test</k>/examine B for P with test V.</de></ld>"

        result = definition.export_for_english(word="test", style="normal")
        assert result == '<div class="d_line"><span class="w_name">prukao</span>, ' \
                         '<span class="w_origin">&lt;test act&gt;</span> ' \
                         '<span class="definition eng" id=13527><span class="dt">' \
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
        assert result == "<dl>(4v) K <k>test</k>/<k>examine</k> " \
                         "B for P with test V. [K&zwj;-&zwj;BPV]</dl>"

        result = definition.export_for_loglan(style="normal")
        assert result == '<div class="definition log" id=13527><span class="dg">' \
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

        word.origin = None
        result = word.html_origin()
        assert result == "<o>&lt;test act&gt;</o> "

        word.origin_x = None
        result = word.html_origin()
        assert result == ""

    def test_html_definitions(self):
        """Test exporting word's definitions as a list of HTML strings"""
        db_add_objects(Word, words)
        db_add_objects(Definition, definitions)
        word = Word.get_by_id(7315)

        result = word.html_definitions(style="ultra")
        assert isinstance(result, list)
        assert len(result) == 4
        assert result[0] == "<dl>(3n) V is a <k>test</k>/<k>examination</k> " \
                            "for property B in any member of class F. [V&zwj;-&zwj;BF]</dl>"

        result = word.html_definitions(style="normal")
        assert isinstance(result, list)
        assert len(result) == 4
        assert result[0] == '<div class="definition log" id=13523><span class="dg">' \
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
                '<dl>(3n) V is a <k>test</k>/<k>examination</k> for property '
                'B in any member of class F. [V&zwj;-&zwj;BF]</dl>',
                '<dl>(vt) <k>test</k>, test for … a property … in a member of ….</dl>',
                '<dl><du>fu —</du> (a) <k>testable</k>, of classes with -able members.</dl>',
                '<dl><du>nu —</du> (a) <k>testable</k>, of testable properties.</dl>'],
            'used_in': '<use>prukao</use>'}
        assert isinstance(result, Meaning)
        assert result.__dict__ == expected_value

        word = Word.get_by_id(3802)

        result = word.meaning(style="normal")
        expected_value = {
            'mid': 3802,
            'technical': '<span class="m_origin">&lt;kak(to)&gt;</span> <span class="m_technical">'
                         '<span class="m_type">Afx</span> <span class="m_author">JCB</span> '
                         '<span class="m_year">1988</span> <span class="m_rank">7+</span></span>',
            'definitions': ['<div class="definition log" id=7240><span class="dg">(af)'
                            '</span> <span class="db">a combining form of '
                            '<l>kakto</l>, <k>act</k>.</span></div>'],
            'used_in': None}

        assert isinstance(result, Meaning)
        assert result.__dict__ == expected_value

    def test_html_meaning(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_add_objects(Author, authors)
        db_add_objects(Definition, definitions)
        db_connect_authors(connect_authors)
        db_connect_words(connect_words)
        word = Word.get_by_id(7315)
        expected_result_ultra = """<m>
<t><afx>pru</afx> <o>&lt;3/4E prove | 2/4C sh yen | 3/6S prueba | 2/5R proba | 2/5F epreuve | 2/5G probe | 2/6J tameshi&gt;</o> <tec>49% C-Prim L4 1975 1.9</tec></t>
<ds>
<dl>(3n) V is a <k>test</k>/<k>examination</k> for property B in any member of class F. [V&zwj;-&zwj;BF]</dl>
<dl>(vt) <k>test</k>, test for … a property … in a member of ….</dl>
<dl><du>fu —</du> (a) <k>testable</k>, of classes with -able members.</dl>
<dl><du>nu —</du> (a) <k>testable</k>, of testable properties.</dl>
</ds>
<us>Used In: <use>prukao</use></us>
</m>"""
        result = word.html_meaning(style="ultra")
        assert result == expected_result_ultra

        expected_result_normal = """<div class="meaning" id="7315">
<div class="technical"><span class="m_afx">pru</span> <span class="m_origin">&lt;3/4E prove | 2/4C sh yen | 3/6S prueba | 2/5R proba | 2/5F epreuve | 2/5G probe | 2/6J tameshi&gt;</span> <span class="m_technical"><span class="m_match">49%</span> <span class="m_type">C-Prim</span> <span class="m_author">L4</span> <span class="m_year">1975</span> <span class="m_rank">1.9</span></span></div>
<div class="definitions">
<div class="definition log" id=13523><span class="dg">(3n)</span> <span class="db">V is a <k>test</k>/<k>examination</k> for property B in any member of class F.</span> <span class="dt">[V&zwj;-&zwj;BF]</span></div>
<div class="definition log" id=13524><span class="dg">(vt)</span> <span class="db"><k>test</k>, test for … a property … in a member of ….</span></div>
<div class="definition log" id=13525><span class="du">fu —</span> <span class="dg">(a)</span> <span class="db"><k>testable</k>, of classes with -able members.</span></div>
<div class="definition log" id=13526><span class="du">nu —</span> <span class="dg">(a)</span> <span class="db"><k>testable</k>, of testable properties.</span></div>
</div>
<div class="used_in">Used In: <span class="m_use">prukao</span></div>
</div>"""
        result = word.html_meaning(style="normal")
        assert result == expected_result_normal

    def test_html_all_by_name(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_add_objects(Author, authors)
        db_add_objects(Event, events)
        db_add_objects(Definition, definitions)
        db_connect_authors(connect_authors)
        db_connect_words(connect_words)

        result = Word.html_all_by_name("buuku", style="ultra")
        assert result is None

        expected_result_ultra = """<ws>
<w wid="pruci"><wl>pruci,</wl>
<ms>
<m>
<t><afx>pru</afx> <o>&lt;3/4E prove | 2/4C sh yen | 3/6S prueba | 2/5R proba | 2/5F epreuve | 2/5G probe | 2/6J tameshi&gt;</o> <tec>49% C-Prim L4 1975 1.9</tec></t>
<ds>
<dl>(3n) V is a <k>test</k>/<k>examination</k> for property B in any member of class F. [V&zwj;-&zwj;BF]</dl>
<dl>(vt) <k>test</k>, test for … a property … in a member of ….</dl>
<dl><du>fu —</du> (a) <k>testable</k>, of classes with -able members.</dl>
<dl><du>nu —</du> (a) <k>testable</k>, of testable properties.</dl>
</ds>
<us>Used In: <use>prukao</use></us>
</m>
</ms>
</w>
</ws>
"""

        result = Word.html_all_by_name("pruci", style="ultra")
        assert result == expected_result_ultra

        expected_result_normal = """<div class="words">
<div class="word" wid="pruci">
<div class="word_line"><span class="word_name">pruci</span>,</div>
<div class="meanings">
<div class="meaning" id="7315">
<div class="technical"><span class="m_afx">pru</span> <span class="m_origin">&lt;3/4E prove | 2/4C sh yen | 3/6S prueba | 2/5R proba | 2/5F epreuve | 2/5G probe | 2/6J tameshi&gt;</span> <span class="m_technical"><span class="m_match">49%</span> <span class="m_type">C-Prim</span> <span class="m_author">L4</span> <span class="m_year">1975</span> <span class="m_rank">1.9</span></span></div>
<div class="definitions">
<div class="definition log" id=13523><span class="dg">(3n)</span> <span class="db">V is a <k>test</k>/<k>examination</k> for property B in any member of class F.</span> <span class="dt">[V&zwj;-&zwj;BF]</span></div>
<div class="definition log" id=13524><span class="dg">(vt)</span> <span class="db"><k>test</k>, test for … a property … in a member of ….</span></div>
<div class="definition log" id=13525><span class="du">fu —</span> <span class="dg">(a)</span> <span class="db"><k>testable</k>, of classes with -able members.</span></div>
<div class="definition log" id=13526><span class="du">nu —</span> <span class="dg">(a)</span> <span class="db"><k>testable</k>, of testable properties.</span></div>
</div>
<div class="used_in">Used In: <span class="m_use">prukao</span></div>
</div>
</div>
</div>
</div>
"""
        result = Word.html_all_by_name("Pruci", style="normal")
        assert result == expected_result_normal

        result = Word.html_all_by_name("pruci", style="normal", event_id=1)
        assert result == expected_result_normal

        result = Word.html_all_by_name("Pruci", style="normal", case_sensitive=True)
        assert result is None

        expected_result_normal = """<div class="words">
<div class="word" wid="pru">
<div class="word_line"><span class="word_name">pru</span>,</div>
<div class="meanings">
<div class="meaning" id="7314">
<div class="technical"><span class="m_origin">&lt;pru(ci)&gt;</span> <span class="m_technical"><span class="m_type">Afx</span> <span class="m_author">JCB</span> <span class="m_year">1988</span> <span class="m_rank">7+</span></span></div>
<div class="definitions">
<div class="definition log" id=13521><span class="dg">(af)</span> <span class="db">a combining form of <l>pruci</l>, <k>test</k>.</span></div>
</div>
</div>
</div>
</div>
<div class="word" wid="pruci">
<div class="word_line"><span class="word_name">pruci</span>,</div>
<div class="meanings">
<div class="meaning" id="7315">
<div class="technical"><span class="m_afx">pru</span> <span class="m_origin">&lt;3/4E prove | 2/4C sh yen | 3/6S prueba | 2/5R proba | 2/5F epreuve | 2/5G probe | 2/6J tameshi&gt;</span> <span class="m_technical"><span class="m_match">49%</span> <span class="m_type">C-Prim</span> <span class="m_author">L4</span> <span class="m_year">1975</span> <span class="m_rank">1.9</span></span></div>
<div class="definitions">
<div class="definition log" id=13523><span class="dg">(3n)</span> <span class="db">V is a <k>test</k>/<k>examination</k> for property B in any member of class F.</span> <span class="dt">[V&zwj;-&zwj;BF]</span></div>
<div class="definition log" id=13524><span class="dg">(vt)</span> <span class="db"><k>test</k>, test for … a property … in a member of ….</span></div>
<div class="definition log" id=13525><span class="du">fu —</span> <span class="dg">(a)</span> <span class="db"><k>testable</k>, of classes with -able members.</span></div>
<div class="definition log" id=13526><span class="du">nu —</span> <span class="dg">(a)</span> <span class="db"><k>testable</k>, of testable properties.</span></div>
</div>
<div class="used_in">Used In: <span class="m_use">prukao</span></div>
</div>
</div>
</div>
<div class="word" wid="prukao">
<div class="word_line"><span class="word_name">prukao</span>,</div>
<div class="meanings">
<div class="meaning" id="7316">
<div class="technical"><span class="m_origin">&lt;pru(ci)+ka(kt)o=test act&gt;</span> <span class="m_technical"><span class="m_type">2-Cpx</span> <span class="m_author">L4</span> <span class="m_year">1975</span> <span class="m_rank">1.9</span></span></div>
<div class="definitions">
<div class="definition log" id=13527><span class="dg">(4v)</span> <span class="db">K <k>test</k>/<k>examine</k> B for P with test V.</span> <span class="dt">[K&zwj;-&zwj;BPV]</span></div>
<div class="definition log" id=13528><span class="dg">(n)</span> <span class="db">a <k>tester</k>, one who uses tests.</span></div>
<div class="definition log" id=13529><span class="du">nu —</span> <span class="dg">(a)</span> <span class="db"><k>testable</k>, of one who/that which is -ed.</span></div>
<div class="definition log" id=13530><span class="du">nu —</span> <span class="dg">(n)</span> <span class="db">a <k>testee</k>, one who is -ed.</span></div>
<div class="definition log" id=13531><span class="du">po —</span> <span class="dg">(n)</span> <span class="db">a <k>test</k>/<k>examination</k>, an act of testing.</span></div>
</div>
</div>
</div>
</div>
</div>
"""
        result = Word.html_all_by_name("pru", style="normal", case_sensitive=True, partial_results=True)
        assert result == expected_result_normal

        result = Word.html_all_by_name("Pru", style="normal", case_sensitive=False, partial_results=True)
        assert result == expected_result_normal

    def test_definitions_by_key(self):
        import itertools
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_add_objects(Author, authors)
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_authors(connect_authors)
        db_connect_words(connect_words)
        db_connect_keys(connect_keys)

        current_words = Word.by_key(
            "test", case_sensitive=True, partial_results=True).all()

        current_definitions = Word.definitions_by_key(
            "test", current_words, case_sensitive=True,
            partial_results=True).values()
        ab = itertools.chain(*current_definitions)
        result = len(list(ab))
        assert result == 10

        current_definitions = Word.definitions_by_key(
            "test", current_words, case_sensitive=True,
            partial_results=False).values()
        ab = itertools.chain(*current_definitions)
        result = len(list(ab))
        assert result == 5

    def test_translation_by_key(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_add_objects(Author, authors)
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_authors(connect_authors)
        db_connect_words(connect_words)
        db_connect_keys(connect_keys)

        expected_result_ultra = """<ld><wn>pru</wn>, <de>(af) a combining form of <l>pruci</l>, <k>test</k>.</de></ld>
<ld><wn>pruci</wn>, <de>[V&zwj;-&zwj;BF] (3n) V is a <k>test</k>/examination for property B in any member of class F.</de></ld>
<ld><wn>pruci</wn>, <de>(vt) <k>test</k>, test for … a property … in a member of ….</de></ld>
<ld><wn>prukao</wn>, <o>&lt;test act&gt;</o> <de>[K&zwj;-&zwj;BPV] (4v) K <k>test</k>/examine B for P with test V.</de></ld>
<ld><wn>po prukao</wn>, <o>&lt;test act&gt;</o> <de>(n) a <k>test</k>/examination, an act of testing.</de></ld>"""
        result = Word.translation_by_key("test")
        assert result == expected_result_ultra

        expected_result_normal = """<div class="d_line"><span class="w_name">pru</span>, <span class="definition eng" id=13521><span class="dg">(af)</span> <span class="db">a combining form of <l>pruci</l>, <k>test</k>.</span></span></div>
<div class="d_line"><span class="w_name">pruci</span>, <span class="definition eng" id=13523><span class="dt">[V&zwj;-&zwj;BF]</span> <span class="dg">(3n)</span> <span class="db">V is a <k>test</k>/examination for property B in any member of class F.</span></span></div>
<div class="d_line"><span class="w_name">pruci</span>, <span class="definition eng" id=13524><span class="dg">(vt)</span> <span class="db"><k>test</k>, test for … a property … in a member of ….</span></span></div>
<div class="d_line"><span class="w_name">prukao</span>, <span class="w_origin">&lt;test act&gt;</span> <span class="definition eng" id=13527><span class="dt">[K&zwj;-&zwj;BPV]</span> <span class="dg">(4v)</span> <span class="db">K <k>test</k>/examine B for P with test V.</span></span></div>
<div class="d_line"><span class="w_name">po prukao</span>, <span class="w_origin">&lt;test act&gt;</span> <span class="definition eng" id=13531><span class="dg">(n)</span> <span class="db">a <k>test</k>/examination, an act of testing.</span></span></div>"""
        result = Word.translation_by_key("test", style="normal")
        assert result == expected_result_normal

        result = Word.translation_by_key("word_that_does_not_exist")
        assert result is None
