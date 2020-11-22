# -*- coding: utf-8 -*-
"""Data for test_models"""

import datetime
from loglan_db.model import Word, Definition, Type, Event, Author, Key

# ===== KEYS ===================================================================
key_1 = {'word': 'examine', 'updated': None, 'language': 'en', 'id': 4647, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
key_2 = {'word': 'test', 'updated': None, 'language': 'en', 'id': 12474, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
key_3 = {'word': 'tester', 'updated': None, 'language': 'en', 'id': 12480, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
key_4 = {'word': 'testable', 'updated': None, 'language': 'en', 'id': 12476, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
key_5 = {'word': 'testee', 'updated': None, 'language': 'en', 'id': 12479, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
key_6 = {'word': 'examination', 'updated': None, 'language': 'en', 'id': 4646, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
key_7 = {'word': 'act', 'updated': None, 'language': 'en', 'id': 514, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
key_8 = {'word': 'undertake', 'updated': None, 'language': 'en', 'id': 13077, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
key_9 = {'word': 'actor', 'updated': None, 'language': 'en', 'id': 526, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
key_10 = {'word': 'end', 'updated': None, 'language': 'en', 'id': 4373, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
key_11 = {'word': 'activity', 'updated': None, 'language': 'en', 'id': 525, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
keys = [key_1, key_2, key_3, key_4, key_5, key_6, key_7, key_8, key_9, key_10, key_11]

# ===== EVENTS =================================================================
event_1 = {'annotation': 'Initial', 'name': 'Start', 'id': 1, 'updated': None, 'suffix': 'INIT', 'definition': 'The initial vocabulary before updates.', 'date': datetime.date(1975, 1, 1), 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
events = [event_1]

# ===== AUTHORS ================================================================
author_1 = {'notes': 'The printed-on-paper book, 1975 version of the dictionary.', 'abbreviation': 'L4', 'updated': None, 'full_name': 'Loglan 4&5', 'id': 29, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
author_2 = {'notes': '', 'abbreviation': 'JCB', 'updated': None, 'full_name': 'James Cooke Brown', 'id': 13, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
authors = [author_1, author_2]

# ===== TYPES ==================================================================
type_1 = {'description': 'Two-term Complex E.g. flicea, from fli(du)+ce(nj)a=liquid-become.', 'group': 'Cpx', 'type': '2-Cpx', 'updated': None, 'parentable': True, 'type_x': 'Predicate', 'id': 5, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
type_2 = {'description': 'Composite Primitives, drawn from several target languages in a way that might make them recognizable in most of them. (See Loglan 1 Section 6.3.)', 'group': 'Prim', 'type': 'C-Prim', 'updated': None, 'parentable': False, 'type_x': 'Predicate', 'id': 9, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
type_3 = {'description': 'Affix.', 'group': 'Little', 'type': 'Afx', 'updated': None, 'parentable': True, 'type_x': 'Affix', 'id': 2, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
types = [type_1, type_2, type_3]

# ===== WORDS ==================================================================
word_1 = {'updated': None, 'notes': None, 'id': 7316, 'TID_old': None, 'id_old': 7191, 'name': 'prukao', 'type_id': 5, 'origin': 'pru(ci)+ka(kt)o', 'event_start_id': 1, 'origin_x': 'test act', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '1.9', 'year': datetime.date(1975, 1, 1)}
word_2 = {'updated': None, 'notes': None, 'id': 3813, 'TID_old': None, 'id_old': 3880, 'name': 'kakto', 'type_id': 9, 'origin': '3/3R akt | 4/4S acto | 3/3F acte | 2/3E act | 2/3H kam', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '56%', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '1.0', 'year': datetime.date(1975, 1, 1)}
word_3 = {'updated': None, 'notes': None, 'id': 7315, 'TID_old': None, 'id_old': 7190, 'name': 'pruci', 'type_id': 9, 'origin': '3/4E prove | 2/4C sh yen | 3/6S prueba | 2/5R proba | 2/5F epreuve | 2/5G probe | 2/6J tameshi', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '49%', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '1.9', 'year': datetime.date(1975, 1, 1)}
word_4 = {'updated': None, 'notes': None, 'id': 3802, 'TID_old': None, 'id_old': 3869, 'name': 'kak', 'type_id': 2, 'origin': 'kak(to)', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '7+', 'year': datetime.date(1988, 1, 1)}
word_5 = {'updated': None, 'notes': {'author': '(?)', 'year': '(?)'}, 'id': 3911, 'TID_old': None, 'id_old': 9983, 'name': 'kao', 'type_id': 2, 'origin': 'ka(kt)o', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '7+?', 'year': datetime.date(1988, 1, 1)}
word_6 = {'updated': None, 'notes': None, 'id': 7314, 'TID_old': None, 'id_old': 7188, 'name': 'pru', 'type_id': 2, 'origin': 'pru(ci)', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '7+', 'year': datetime.date(1988, 1, 1)}
words = [word_1, word_2, word_3, word_4, word_5, word_6]

# ===== DEFINITIONS ============================================================
definition_1 = {'position': 1, 'id': 13527, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'K «test»/«examine» B for P with test V.', 'slots': 4, 'usage': '', 'word_id': 7316, 'updated': None, 'language': 'en', 'case_tags': 'K-BPV', 'grammar_code': 'v'}
definition_2 = {'position': 2, 'id': 13528, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'a «tester», one who uses tests.', 'slots': None, 'usage': '', 'word_id': 7316, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_3 = {'position': 3, 'id': 13529, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': '«testable», of one who/that which is -ed.', 'slots': None, 'usage': 'nu %', 'word_id': 7316, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'a'}
definition_4 = {'position': 4, 'id': 13530, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'a «testee», one who is -ed.', 'slots': None, 'usage': 'nu %', 'word_id': 7316, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_5 = {'position': 5, 'id': 13531, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'a «test»/«examination», an act of testing.', 'slots': None, 'usage': 'po %', 'word_id': 7316, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_6 = {'position': 1, 'id': 7272, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'K «act»/«undertake» action V with end/purpose P.', 'slots': 3, 'usage': '', 'word_id': 3813, 'updated': None, 'language': 'en', 'case_tags': 'K-VP', 'grammar_code': 'v'}
definition_7 = {'position': 2, 'id': 7273, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'an «actor», one who seeks ends, general term.', 'slots': None, 'usage': '', 'word_id': 3813, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_8 = {'position': 3, 'id': 7274, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'an «end», what an actor seeks, but see {furkao}.', 'slots': None, 'usage': 'fu %', 'word_id': 3813, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_9 = {'position': 4, 'id': 7275, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'an «act», what an actor does, but see {nurkao}.', 'slots': None, 'usage': 'nu %', 'word_id': 3813, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_10 = {'position': 5, 'id': 7276, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'an «activity», specific instance.', 'slots': None, 'usage': 'po %', 'word_id': 3813, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_11 = {'position': 1, 'id': 13523, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'V is a «test»/«examination» for property B in any member of class F.', 'slots': 3, 'usage': '', 'word_id': 7315, 'updated': None, 'language': 'en', 'case_tags': 'V-BF', 'grammar_code': 'n'}
definition_12 = {'position': 2, 'id': 13524, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': '«test», test for ... a property ... in a member of ....', 'slots': None, 'usage': '', 'word_id': 7315, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'vt'}
definition_13 = {'position': 3, 'id': 13525, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': '«testable», of classes with -able members.', 'slots': None, 'usage': 'fu %', 'word_id': 7315, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'a'}
definition_14 = {'position': 4, 'id': 13526, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': '«testable», of testable properties.', 'slots': None, 'usage': 'nu %', 'word_id': 7315, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'a'}
definition_15 = {'position': 1, 'id': 7240, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'a combining form of {kakto}, «act».', 'slots': None, 'usage': '', 'word_id': 3802, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'af'}
definition_16 = {'position': 1, 'id': 18573, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'a combining form of {kakto}, «act».', 'slots': None, 'usage': '', 'word_id': 3911, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'af'}
definition_17 = {'position': 1, 'id': 13521, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'notes': None, 'body': 'a combining form of {pruci}, «test».', 'slots': None, 'usage': '', 'word_id': 7314, 'updated': None, 'language': 'en', 'case_tags': '', 'grammar_code': 'af'}
definitions = [definition_1, definition_2, definition_3, definition_4, definition_5, definition_6, definition_7, definition_8, definition_9, definition_10, definition_11, definition_12, definition_13, definition_14, definition_15, definition_16, definition_17]

all_objects = [(Key, keys), (Event, events), (Author, authors), (Type, types), (Word, words), (Definition, definitions)]

# ===== CONNECTIONS ============================================================
connect_authors = [(29, 7316), (29, 3813), (29, 7315), (13, 3802), (13, 3911), (13, 7314)]  # (AID, WID)
connect_keys = [(4647, 13527), (12474, 13527), (12480, 13528), (12476, 13529), (12479, 13530), (4646, 13531), (12474, 13531), (514, 7272), (13077, 7272), (526, 7273), (4373, 7274), (514, 7275), (525, 7276), (4646, 13523), (12474, 13523), (12474, 13524), (12476, 13525), (12476, 13526), (514, 7240), (514, 18573), (12474, 13521)]  # (KID, DID)
connect_words = [(3813, 3802), (3813, 3911), (3813, 7316), (7315, 7314), (7315, 7316)]  # (parent_id, child_id)


# EVENT 5 === appeared_words ===================================================
word_1_appeared_event_5 = {'updated': None, 'notes': {'year': "(to '15)"}, 'id': 964, 'TID_old': None, 'id_old': 10091, 'name': 'cii', 'type_id': 17, 'origin': '', 'event_start_id': 5, 'origin_x': '', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '', 'year': datetime.date(2013, 1, 1)}
word_2_appeared_event_5 = {'updated': None, 'notes': {'year': "(to '15)"}, 'id': 2359, 'TID_old': None, 'id_old': 10098, 'name': 'flekukfoa', 'type_id': 6, 'origin': 'fle(ti)+kuk(ra)+fo(rm)a', 'event_start_id': 5, 'origin_x': 'flying quick form', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '', 'year': datetime.date(2008, 1, 1)}
word_3_appeared_event_5 = {'updated': None, 'notes': {'year': "(to '15)"}, 'id': 4771, 'TID_old': None, 'id_old': 10099, 'name': 'lekveo', 'type_id': 5, 'origin': 'le(n)k(i)+ve(sl)o', 'event_start_id': 5, 'origin_x': 'electricity vessel', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '', 'year': datetime.date(2008, 1, 1)}
words_appeared = [word_1_appeared_event_5, word_2_appeared_event_5, word_3_appeared_event_5]

# EVENT 5 === deprecated_words =================================================
word_1_deprecated_event_5 = {'updated': None, 'notes': {'year': "(fixed bad joint '16)"}, 'id': 6669, 'TID_old': None, 'id_old': 6637, 'name': 'osmio', 'type_id': 8, 'origin': 'ISV', 'event_start_id': 1, 'origin_x': '', 'event_end_id': 5, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '7+', 'year': datetime.date(1988, 1, 1)}
word_2_deprecated_event_5 = {'updated': None, 'notes': {'year': "(corrected CV to CVh '16)"}, 'id': 7802, 'TID_old': None, 'id_old': 7668, 'name': 'riyhasgru', 'type_id': 5, 'origin': 'rih+y+has(fa)+gru(pa)', 'event_start_id': 1, 'origin_x': 'few house group', 'event_end_id': 5, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '7+', 'year': datetime.date(1999, 1, 1)}
word_3_deprecated_event_5 = {'updated': None, 'notes': {'year': "(corrected CV to CVh '16)"}, 'id': 7803, 'TID_old': None, 'id_old': 7669, 'name': 'riyvei', 'type_id': 4, 'origin': 'rih+y+ve(tc)i', 'event_start_id': 1, 'origin_x': 'several events', 'event_end_id': 5, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '7+', 'year': datetime.date(1999, 1, 1)}
word_4_deprecated_event_5 = {'updated': None, 'notes': {'year': "(fixed '16)"}, 'id': 9282, 'TID_old': None, 'id_old': 9036, 'name': 'testuda', 'type_id': 8, 'origin': 'Lin. Testudines', 'event_start_id': 1, 'origin_x': '', 'event_end_id': 5, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '7+', 'year': datetime.date(1997, 1, 1)}
words_deprecated = [word_1_deprecated_event_5, word_2_deprecated_event_5, word_3_deprecated_event_5, word_4_deprecated_event_5]

changed_words = words_appeared + words_deprecated
changed_events = ({'annotation': 'Randall Cleanup', 'name': 'Randall Dictionary Cleanup', 'id': 5, 'updated': None, 'suffix': 'RDC', 'definition': 'parsed all the words in the dictionary, identified ones that the parser did not recognize as words', 'date': datetime.date(2016, 1, 15), 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}, )

# ===== ALL EVENTS =================================================================
event_1 = {'annotation': 'Initial', 'name': 'Start', 'id': 1, 'updated': None, 'suffix': 'INIT', 'definition': 'The initial vocabulary before updates.', 'date': datetime.date(1975, 1, 1), 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
event_2 = {'annotation': 'Syllables', 'name': '94/2', 'id': 2, 'updated': None, 'suffix': 'SC', 'definition': "Any 3+ syllable Complex that is CVC initial AND the C/C is a permissible initial must be 'y' hyphenated. The Slinkui test is vacated, and Tosmabru is replaced by this. Eg: 'paslinkui' -> 'pasylinkui' while the currently prohibitted '*tosmabru' -> 'tosymabru'.", 'date': datetime.date(1994, 1, 2), 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
event_3 = {'annotation': 'Doubled Vowels', 'name': 'No double vowels in borrowings', 'id': 3, 'updated': None, 'suffix': 'DV', 'definition': "Doubled vowels (which require one to be stressed) are prohibited from Borrowings so they can be attached to Complexes without problems. Only 'alkooli' -> 'alkoholi' is affected.", 'date': datetime.date(2013, 1, 1), 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
event_4 = {'annotation': 'Randall Trial', 'name': 'Randall Trial Words 1', 'id': 4, 'updated': None, 'suffix': 'RH1', 'definition': 'Randall Holmes trial words plus grammar vocab', 'date': datetime.date(2013, 12, 18), 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
event_5 = {'annotation': 'Randall Cleanup', 'name': 'Randall Dictionary Cleanup', 'id': 5, 'updated': None, 'suffix': 'RDC', 'definition': 'parsed all the words in the dictionary, identified ones that the parser did not recognize as words', 'date': datetime.date(2016, 1, 15), 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
event_6 = {'annotation': 'Torrua Repair', 'name': 'Torrua Dictionary Repair', 'id': 6, 'updated': None, 'suffix': 'TDR', 'definition': 'Repair of the dictionary by Torrua and Peter Hill', 'date': datetime.date(2019, 5, 25), 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
all_events = [event_1, event_2, event_3, event_4, event_5, event_6]

# ===== SETTINGS ===============================================================
setting_1 = {'last_word_id': 10141, 'db_version': 2, 'id': 1, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'db_release': '4.5.9', 'date': datetime.datetime(2020, 10, 9, 9, 10, 20), 'updated': None}
settings = [setting_1]

# ===== SYLLABLES ==============================================================
syllable_35 = {'id': 35, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'allowed': True, 'name': 'vr', 'updated': None, 'type': 'InitialCC'}
syllable_36 = {'id': 36, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'allowed': True, 'name': 'zb', 'updated': None, 'type': 'InitialCC'}
syllable_37 = {'id': 37, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'allowed': True, 'name': 'zv', 'updated': None, 'type': 'InitialCC'}
syllable_38 = {'id': 38, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'allowed': False, 'name': 'cdz', 'updated': None, 'type': 'UnintelligibleCCC'}
syllable_39 = {'id': 39, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'allowed': False, 'name': 'cvl', 'updated': None, 'type': 'UnintelligibleCCC'}
syllable_40 = {'id': 40, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'allowed': False, 'name': 'ndj', 'updated': None, 'type': 'UnintelligibleCCC'}
syllables = [syllable_35, syllable_36, syllable_37, syllable_38, syllable_39, syllable_40, ]

# ===== COMPOUNDS & LW ==========================================================
little_1 = {'updated': None, 'notes': None, 'id': 479, 'TID_old': None, 'id_old': 382, 'name': 'bicio', 'type_id': 16, 'origin': 'bi+cio', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '15', 'year': datetime.date(1975, 1, 1)}
little_2 = {'updated': None, 'notes': None, 'id': 467, 'TID_old': None, 'id_old': 370, 'name': 'bi', 'type_id': 17, 'origin': '', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '1.0', 'year': datetime.date(1975, 1, 1)}
little_3 = {'updated': None, 'notes': None, 'id': 999, 'TID_old': None, 'id_old': 986, 'name': 'cio', 'type_id': 17, 'origin': '', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '1.0', 'year': datetime.date(1975, 1, 1)}
littles = [little_1, little_2, little_3, ]

little_type_1 = {'description': 'Compound Little Word E.g. enoi from e+no, "and not".', 'group': 'Little', 'type': 'Cpd', 'updated': None, 'parentable': True, 'type_x': 'Struct', 'id': 16, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
little_type_2 = {'description': 'Little Word, a small word used to give Loglan its grammatical structure.', 'group': 'Little', 'type': 'LW', 'updated': None, 'parentable': True, 'type_x': 'Struct', 'id': 17, 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132)}
little_types = [little_type_1, little_type_2, ]

# ===== DOUBLED WORDS ===========================================================
doubled_word_1 = {'updated': None, 'notes': None, 'id': 1835, 'TID_old': None, 'id_old': 1722, 'name': 'duo', 'type_id': 17, 'origin': 'du(rz)o', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '1.0', 'year': datetime.date(1975, 1, 1)}
doubled_word_2 = {'updated': None, 'notes': {'author': '(?)', 'year': '(?)'}, 'id': 1836, 'TID_old': None, 'id_old': 9958, 'name': 'duo', 'type_id': 2, 'origin': 'du(rz)o', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '7+?', 'year': datetime.date(1988, 1, 1)}
doubled_words = [doubled_word_1, doubled_word_2, ]
