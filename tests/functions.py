# -*- coding: utf-8 -*-
"""Functions for test_models"""

from loglan_db import db
from loglan_db.model import Word, Key, Event, Author, Type, Definition
from loglan_db.model_db.base_connect_tables import t_connect_authors, t_connect_words, t_connect_keys


def print_data_by_word(name: str):

    # get cpx
    word = Word.by_name(name).first()
    sources = word.parents

    affixes = []
    definitions = []
    types = []
    events = []
    authors = []
    keys = []

    relationship_authors = []
    relationship_keys = []
    relationship_words = []

    for s in sources:
        for a in s.affixes:
            relationship_words.append((s.id, a.id))
            affixes.append(a)
        relationship_words.append((s.id, word.id))
    words = [word, ] + sources + affixes

    for w in words:
        for d in w.definitions:
            definitions.append(d)

        for a in w.authors:
            relationship_authors.append((a.id, w.id))
            if a not in authors:
                authors.append(a)

        if w.type not in types:
            types.append(w.type)

        if w.event_start not in events and w.event_start:
            events.append(w.event_start)

        if w.event_end not in events and w.event_end:
            events.append(w.event_end)

    for d in definitions:
        for k in d.keys:
            relationship_keys.append((k.id, d.id))
            if k not in keys:
                keys.append(k)

    all_objects = [
        (Key, keys), (Event, events), (Author, authors),
        (Type, types), (Word, words), (Definition, definitions), ]

    for type_object, objects in all_objects:
        type_object = str(type_object.__name__).lower()
        print(f"# {'='*5} {type_object.upper()}S {'='*(70-len(type_object))}")
        for i, o in enumerate(objects, 1):
            print(f"{type_object}_{i} = {o.__str__()} ")
        list_of_items = [type_object + '_' + str(i) for i in range(1, len(objects) + 1)]
        print(f"{type_object}s = {list_of_items}\n".replace("'", ""))

    types = str([(to.__name__, to.__name__.lower() + 's') for to, _ in all_objects]).replace("'", "")
    print(f"all_objects = {types}\n")
    print(f"# {'=' * 5} CONNECTIONS {'=' * (71 - len('CONNECTIONS'))}")
    print(f"connect_authors = {relationship_authors}  # (AID, WID)")
    print(f"connect_keys = {relationship_keys}  # (KID, DID)")
    print(f"connect_words = {relationship_words}  # (parent_id, child_id)")


def print_elements(objects, is_all: bool = False):
    type_object = str(type(objects[0]).__name__.replace("Base", "")).lower()
    print(f"# {'=' * 5}{' ALL' if is_all else ''} {type_object.upper()}S {'=' * (70 - len(type_object))}")
    for i, o in enumerate(objects, 1):
        print(f"{type_object}_{i} = {o.__str__()} ")
    list_of_items = [type_object + '_' + str(i) for i in range(1, len(objects) + 1)]
    print(f"{'all_' if is_all else ''}{type_object}s = {list_of_items}\n".replace("'", ""))


def db_add_object(obj_class, obj):
    obj = obj_class(**obj)
    obj.save()


def db_add_objects(obj_class, objects):
    [db_add_object(obj_class, obj) for obj in objects]


def db_connect_authors(pairs: list):
    for aid, wid in pairs:
        ins = t_connect_authors.insert().values(WID=wid, AID=aid)
        db.engine.execute(ins)


def db_connect_keys(pairs: list):
    for kid, did in pairs:
        ins = t_connect_keys.insert().values(DID=did, KID=kid)
        db.engine.execute(ins)


def db_connect_words(pairs: list):
    for parent_id, child_id in pairs:
        ins = t_connect_words.insert().values(parent_id=parent_id, child_id=child_id)
        db.engine.execute(ins)


def db_add_and_return(obj_class, data):
    db_add_object(obj_class, data)
    return obj_class.get_by_id(data["id"])


dar = db_add_and_return
