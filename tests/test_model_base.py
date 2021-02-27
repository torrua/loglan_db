# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903, C0116, C0103
"""Base Model unit tests."""

import datetime
import pytest
import sqlalchemy.exc

from loglan_db.model_db.base_word import BaseWord as Word
from loglan_db.model_db.base_word_source import BaseWordSource as WordSource
from loglan_db.model_db.base_definition import BaseDefinition as Definition
from loglan_db.model_db.base_type import BaseType as Type
from loglan_db.model_db.base_syllable import BaseSyllable as Syllable
from loglan_db.model_db.base_setting import BaseSetting as Setting
from loglan_db.model_db.base_key import BaseKey as Key
from loglan_db.model_db.base_event import BaseEvent as Event
from loglan_db.model_db.base_author import BaseAuthor as Author

from tests.functions import db_connect_authors, db_connect_keys, db_connect_words, \
    db_add_objects, dar, db_add_object

from tests.data import keys, definitions, words, types, authors, settings, syllables, word_1_source_1
from tests.data import changed_words, changed_events, all_events, doubled_words
from tests.data import definition_1, definition_2, word_1
from tests.data import un_key_1, un_key_2, un_key_3

from tests.data import connect_authors
from tests.data import connect_keys
from tests.data import connect_words


@pytest.mark.usefixtures("db")
class TestAuthor:
    """Author tests."""
    @pytest.mark.parametrize("item", authors)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        author = dar(Author, item)
        author_from_db = Author.get_by_id(item["id"])

        assert author == author_from_db
        assert isinstance(author, Author)
        assert isinstance(author.id, int)
        assert isinstance(author.abbreviation, str)
        assert isinstance(author.full_name, (str, type(None)))
        assert isinstance(author.notes, (str, type(None)))

    def test_relationship_contribution(self):
        db_add_objects(Author, authors)
        db_add_objects(Word, words)
        db_connect_authors(connect_authors)

        test_author = Author.get_by_id(29)
        assert len(test_author.contribution) == 3
        assert isinstance(test_author.contribution, list)
        assert [w.name for w in test_author.contribution] == ['kakto', 'pruci', 'prukao']

        test_author = Author.get_by_id(13)
        assert len(test_author.contribution) == 3
        assert [w.name for w in test_author.contribution] == ['kak', 'kao', 'pru']


@pytest.mark.usefixtures("db")
class TestEvent:
    """Event tests."""

    @pytest.mark.parametrize("item", all_events)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        event = dar(Event, item)
        event_from_db = Event.get_by_id(item["id"])

        assert event == event_from_db
        assert isinstance(event, Event)
        assert isinstance(event.id, int)
        assert isinstance(event.date, datetime.date)
        assert isinstance(event.name, str)
        assert isinstance(event.definition, str)
        assert isinstance(event.annotation, str)
        assert isinstance(event.suffix, str)

    def test_relationship_deprecated_words(self):
        db_add_objects(Word, changed_words)
        db_add_objects(Event, changed_events)
        event = Event.get_by_id(5)

        assert isinstance(event.appeared_words, list)
        assert len(event.appeared_words) == 3

    def test_relationship_appeared_words(self):
        db_add_objects(Word, changed_words)
        db_add_objects(Event, changed_events)
        event = Event.get_by_id(5)

        assert isinstance(event.deprecated_words, list)
        assert len(event.deprecated_words) == 4

    def test_latest(self):
        db_add_objects(Event, all_events)
        latest = Event.latest()

        assert latest.id == 6
        assert latest.annotation == 'Torrua Repair'


@pytest.mark.usefixtures("db")
class TestKey:
    """Key tests."""

    @pytest.mark.parametrize("item", keys)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        key = dar(Key, item)
        key_from_db = Key.get_by_id(item["id"])

        assert key == key_from_db
        assert isinstance(key, Key)
        assert isinstance(key.id, int)
        assert isinstance(key.word, str)
        assert isinstance(key.language, (str, type(None)))

    def test_relationship_definitions(self):
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_keys(connect_keys)
        key = Key.get_by_id(12474)

        assert isinstance(key.definitions, list)
        assert len(key.definitions) == 5
        assert [d.id for d in key.definitions] == [13521, 13523, 13524, 13527, 13531]

    def test_uniqueness(self):
        db_add_objects(Key, [un_key_1, un_key_2, ])
        result = [k.word for k in Key.get_all()]
        assert result == ["examine", "examine", ]

        with pytest.raises(sqlalchemy.exc.IntegrityError) as _:
            assert isinstance(dar(Key, un_key_3), Key)


@pytest.mark.usefixtures("db")
class TestSetting:
    """Setting tests."""

    @pytest.mark.parametrize("item", settings)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        setting = dar(Setting, item)
        setting_from_db = Setting.get_by_id(item["id"])

        assert setting == setting_from_db
        assert isinstance(setting, Setting)
        assert isinstance(setting.id, int)
        assert isinstance(setting.date, (datetime.datetime, type(None)))
        assert isinstance(setting.db_version, int)
        assert isinstance(setting.last_word_id, int)
        assert isinstance(setting.db_release, str)


@pytest.mark.usefixtures("db")
class TestSyllable:
    """Syllable tests."""

    @pytest.mark.parametrize("item", syllables)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""

        syllable = dar(Syllable, item)
        syllable_from_db = Syllable.get_by_id(item["id"])

        assert syllable == syllable_from_db
        assert isinstance(syllable, Syllable)
        assert isinstance(syllable.id, int)
        assert isinstance(syllable.name, str)
        assert isinstance(syllable.type, str)
        assert isinstance(syllable.allowed, (bool, type(None)))


@pytest.mark.usefixtures("db")
class TestType:
    """Type tests."""

    @pytest.mark.parametrize("item", types)
    def test_create_from_dict_with_data(self, item):
        type_ = dar(Type, item)
        type_from_db = Type.get_by_id(item["id"])

        assert type_ == type_from_db
        assert isinstance(type_.id, int)
        assert isinstance(type_.type, str)
        assert isinstance(type_.type_x, str)
        assert isinstance(type_.group, (str, type(None)))
        assert isinstance(type_.parentable, bool)
        assert isinstance(type_.description, (str, type(None)))
        with pytest.raises(Exception) as _:
            assert type_.type == "A-Prim"

    def test_by(self):
        db_add_objects(Type, types)
        test_type = Type.by("Little").first()
        assert test_type.type == "Afx"

        test_type = Type.by("Little")
        assert test_type[0].type == "Afx"

        test_type = Type.by("2-Cpx").first()
        assert test_type.group == "Cpx"

        test_type = Type.by("Predicate").count()
        assert test_type == 2

    def test_relationship_words(self):
        db_add_objects(Type, types)
        db_add_objects(Word, words)

        test_type = Type.by("Little").first()
        assert len(test_type.words) == 3

        test_type = Type.by("C-Prim").first()
        assert len(test_type.words) == 2

        test_type = Type.by("Cpx").first()
        assert len(test_type.words) == 1


@pytest.mark.usefixtures("db")
class TestDefinition:
    """Definition tests."""

    @pytest.mark.parametrize("item", definitions)
    def test_create_from_dict_with_data(self, item):
        definition = dar(Definition, item)
        definition_from_db = Definition.get_by_id(item["id"])

        assert definition == definition_from_db
        assert isinstance(definition.id, int)
        assert isinstance(definition.word_id, int)
        assert isinstance(definition.position, int)
        assert isinstance(definition.usage, (str, type(None)))
        assert isinstance(definition.grammar_code, (str, type(None)))
        assert isinstance(definition.slots, (int, type(None)))
        assert isinstance(definition.case_tags, (str, type(None)))
        assert isinstance(definition.body, str)
        assert isinstance(definition.language, (str, type(None)))
        assert isinstance(definition.notes, (str, type(None)))

    def test_relationship_keys(self):
        pass

    def test_relationship_source_word(self):
        pass

    def test_grammar(self):
        db_add_objects(Definition, definitions)
        d = Definition.get_by_id(13527)
        assert d.grammar == "(4v)"

        d = Definition.get_by_id(13529)
        assert d.grammar == "(a)"

    def test_link_keys_from_list_of_str(self):
        db_add_objects(Definition, definitions)
        db_add_objects(Key, keys)

        keys_to_add = ["test", "examine"]
        d = Definition.get_by_id(13527)
        assert d.keys.count() == 0

        d.link_keys_from_list_of_str(keys_to_add)
        assert d.keys.count() == 2
        assert sorted([k.word for k in d.keys]) == sorted(keys_to_add)

    def test_link_key_from_str(self):
        db_add_objects(Key, keys)
        d = dar(Definition, definition_2)
        assert d.keys.count() == 0

        key_to_add = "tester"
        d.link_key_from_str(key_to_add)
        assert d.keys.count() == 1
        assert d.keys.first().word == key_to_add

    def test_link_keys_from_definition_body(self):
        db_add_objects(Key, keys)
        d = dar(Definition, definition_1)
        assert d.keys.count() == 0

        d.link_keys_from_definition_body()
        assert d.keys.count() == 2
        assert sorted([k.word for k in d.keys]) == sorted(["test", "examine"])

    def test_link_keys(self):
        db_add_objects(Key, keys)

        d0 = dar(Definition, definitions[0])
        assert d0.keys.count() == 0
        keys_to_add_str = ["test", "examine"]
        d0.link_keys(keys_to_add_str)
        assert d0.keys.count() == 2

        d1 = dar(Definition, definitions[1])
        assert d1.keys.count() == 0
        key_to_add_str = "tester"
        d1.link_keys(key_to_add_str)
        assert d1.keys.count() == 1

        d2 = dar(Definition, definitions[10])
        assert d2.keys.count() == 0
        d2.link_keys()
        assert d2.keys.count() == 2

        d3 = dar(Definition, definitions[3])
        es_word, es_code = "probar", "es"
        ru_word, ru_code = "тест", "ru"
        db_add_object(Key, {"word": es_word, "language": es_code})
        db_add_object(Key, {"word": ru_word, "language": ru_code})

        d3.link_keys(source=ru_word, language=ru_code)
        assert d3.keys.first().language == ru_code

        d3.link_keys(source=es_word, language=es_code)
        assert d3.keys.count() == 2
        assert sorted([k.language for k in d3.keys.all()]) == [es_code, ru_code]

        d4 = dar(Definition, definitions[4])
        with pytest.raises(TypeError) as _:
            d4.link_keys(source=1234)

    def test_by_key(self):
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_keys(connect_keys)

        result = Definition.by_key("Test", case_sensitive=True).all()
        assert len(result) == 0

        result = Definition.by_key("test", case_sensitive=True, partial_results=True).all()
        assert len(result) == 10

        result = Definition.by_key("test", case_sensitive=True, partial_results=False, language="en").all()
        assert len(result) == 5

        result = Definition.by_key("Test", case_sensitive=False, partial_results=True).all()
        assert len(result) == 10

        result = Definition.by_key("test", language="es").all()
        assert len(result) == 0


@pytest.mark.usefixtures("db")
class TestWord:
    """Word tests."""

    @pytest.mark.parametrize("item", words)
    def test_create_from_dict_with_data(self, item):
        """Get Word by ID."""
        word = dar(Word, item)
        word_from_db = Word.get_by_id(item["id"])

        assert word == word_from_db
        assert isinstance(word.id, int)
        assert isinstance(word.id_old, int)
        assert isinstance(word.name, str)
        assert isinstance(word.origin, (str, type(None)))
        assert isinstance(word.origin_x, (str, type(None)))
        assert isinstance(word.match, (str, type(None)))
        assert isinstance(word.rank, (str, type(None)))
        assert isinstance(word.year, (datetime.date, type(None)))
        assert isinstance(word.notes, (dict, type(None)))
        assert isinstance(word.TID_old, (int, type(None)))

    @pytest.mark.parametrize("item", words)
    def test_type_relationship(self, item):
        word = dar(Word, item)

        type_data = [t for t in types if t["id"] == word.type_id][0]
        type_ = dar(Type, type_data)

        type_from_db = Type.get_by_id(word.type_id)

        assert isinstance(type_, Type)
        assert isinstance(type_from_db, Type)
        assert type_from_db == type_ == word.type

    @pytest.mark.parametrize("item", words)
    def test_event_relationship(self, item):
        db_add_objects(Event, all_events)
        word = dar(Word, item)

        event_start_from_db = Event.get_by_id(word.event_start_id)
        assert isinstance(event_start_from_db, Event)
        assert event_start_from_db == word.event_start

        if word.event_end_id:
            event_end_from_db = Event.get_by_id(word.event_end_id)
            assert isinstance(event_end_from_db, Event)
            assert event_end_from_db == word.event_start
        else:
            assert word.event_end is None

    def test_authors_relationship(self):
        db_add_objects(Word, words)
        db_add_objects(Author, authors)
        db_connect_authors(connect_authors)

        word = Word.get_by_id(7316)
        author = Author.get_by_id(29)

        assert word.authors.count() == 1
        assert word.authors[0] == author
        assert word.authors.first() == author
        assert isinstance(word.authors.all(), list)
        assert len(word.authors.all()) == 1

    def test_definitions_relationship(self):
        word = dar(Word, word_1)
        definitions_to_add = [d for d in definitions if d["word_id"] == word.id]
        db_add_objects(Definition, definitions_to_add)

        assert word.definitions.count() == len(definitions_to_add) == 5
        assert isinstance(word.definitions[0], Definition)

    def test_query_derivatives(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        p1 = Word.get_by_id(3813)
        p2 = Word.get_by_id(7315)

        assert p1.query_derivatives().count() == 3
        assert p2.query_derivatives().count() == 2
        assert isinstance(p2.query_derivatives().first(), Word)

        assert p1.query_derivatives(word_type="Afx").count() == 2
        assert p1.query_derivatives(word_type="2-Cpx").count() == 1

        assert p1.query_derivatives(word_type_x="Predicate").count() == 1
        assert p2.query_derivatives(word_type_x="Affix").count() == 1

        assert p1.query_derivatives(word_group="Little").count() == 2
        assert p2.query_derivatives(word_group="Cpx").count() == 1

    def test_query_cpx(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        p1 = Word.get_by_id(3813)
        p2 = Word.get_by_id(7315)

        assert p1.query_cpx().count() == 1
        assert p2.query_cpx().count() == 1

    def test_query_afx(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        p1 = Word.get_by_id(3813)
        p2 = Word.get_by_id(7315)

        assert p1.query_afx().count() == 2
        assert p2.query_afx().count() == 1

    def test_query_keys(self):
        db_add_objects(Word, words)
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_keys(connect_keys)

        result = Word.get_by_id(7316).query_keys().count()

        assert result == 7

    def test_parents(self):
        db_add_objects(Word, words)
        db_connect_words(connect_words)

        result = Word.get_by_id(7316).parents

        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

    def test_complexes(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        result = Word.get_by_id(3813).complexes

        assert len(result) == 1
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

    def test_affixes(self):
        db_add_objects(Word, words)
        db_add_objects(Type, types)
        db_connect_words(connect_words)

        result = Word.get_by_id(3813).affixes

        assert len(result) == 2
        assert isinstance(result, list)
        assert isinstance(result[0], Word)

    def test_keys(self):
        db_add_objects(Word, words)
        db_add_objects(Key, keys)
        db_add_objects(Definition, definitions)
        db_connect_keys(connect_keys)

        result = Word.get_by_id(7316).keys

        assert len(result) == 6
        assert isinstance(result, list)
        assert isinstance(result[0], Key)


@pytest.mark.usefixtures("db")
class TestWordSource:
    """WordSource tests."""

    def test_create_from_dict_with_data(self):
        """Get WordSource"""
        word_source = WordSource(**word_1_source_1)
        assert isinstance(word_source.coincidence, int)
        assert isinstance(word_source.length, int)
        assert isinstance(word_source.language, str)
        assert isinstance(word_source.transcription, str)

    def test_as_string(self):
        word_source = WordSource(**word_1_source_1)
        result = word_source.as_string

        assert isinstance(result, str)
        assert result == "2/2E do"
