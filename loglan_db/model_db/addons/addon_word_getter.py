# -*- coding: utf-8 -*-
"""
This module contains an addon for basic Word Model,
which makes it possible to get words by event, name or key
"""
from typing import Union

from flask_sqlalchemy import BaseQuery
from sqlalchemy import or_

from loglan_db.model_db.base_connect_tables import t_connect_keys
from loglan_db.model_db.base_definition import BaseDefinition
from loglan_db.model_db.base_event import BaseEvent
from loglan_db.model_db.base_key import BaseKey
from loglan_db.model_db.base_word import BaseWord
from loglan_db.model_db.base_word import db


class AddonWordGetter:
    """AddonWordGetter model"""

    query: BaseQuery = None
    name: db.Column = None
    event_start_id: db.Column = None
    event_end_id: db.Column = None

    @classmethod
    def by_event(
            cls, event_id: Union[BaseEvent, int] = None,
            add_to: BaseQuery = None) -> BaseQuery:
        """Query filtered by specified Event (latest by default)

        Args:
          event_id: Union[BaseEvent, int]: Event object or Event.id (int) (Default value = None)
          add_to:
        Returns:
          BaseQuery

        """
        if not event_id:
            event_id = BaseEvent.latest().id

        event_id = BaseEvent.id if isinstance(event_id, BaseEvent) else int(event_id)

        request = add_to if add_to else cls.query
        return cls._filter_event(event_id, request).order_by(cls.name)

    @staticmethod
    def _filter_event(event_id: Union[BaseEvent, int], add_to: BaseQuery) -> BaseQuery:
        return add_to.filter(BaseWord.event_start_id <= event_id) \
            .filter(or_(BaseWord.event_end_id > event_id, BaseWord.event_end_id.is_(None)))

    @classmethod
    def by_name(
            cls, name: str, event_id: Union[BaseEvent, int] = None,
            case_sensitive: bool = False,
            partial_results: bool = False,
            add_to: BaseQuery = None) -> BaseQuery:
        """Word.Query filtered by specified name

        Args:
          partial_results:
          event_id:
          name: str:
          case_sensitive: bool:  (Default value = False)
          add_to:
        Returns:
          BaseQuery

        """

        request = add_to if add_to else cls.query
        request = cls.by_event(event_id, request)

        if case_sensitive:
            return cls._filter_word_case_sensitive(
                key=name, partial_results=partial_results, add_to=request)
        return cls._filter_word_case_insensitive(
            key=name, partial_results=partial_results, add_to=request)

    @classmethod
    def by_key(
            cls, key: Union[BaseKey, str],
            language: str = None,
            event_id: Union[BaseEvent, int] = None,
            case_sensitive: bool = False,
            partial_results: bool = False,
            add_to: BaseQuery = None) -> BaseQuery:
        """Word.Query filtered by specified key

        Args:
          key: Union[BaseKey, str]:
          language: str: Language of key (Default value = None)
          event_id: Union[BaseEvent, int]:  (Default value = None)
          case_sensitive: bool:  (Default value = False)
          partial_results: bool:
          add_to:
        Returns:
          BaseQuery

        """

        request = add_to if add_to else cls.query
        request = cls.by_event(event_id, request)

        key = BaseKey.word if isinstance(key, BaseKey) else str(key)
        request = request.join(BaseDefinition, t_connect_keys, BaseKey)

        if case_sensitive:
            request = cls._filter_key_case_sensitive(key, partial_results, request)
        request = cls._filter_key_case_insensitive(key, partial_results, request)

        if language:
            request = request.filter(BaseKey.language == language)

        return request.order_by(cls.name)

    @staticmethod
    def _filter_key_case_sensitive(
            key: str, partial_results: bool, add_to: BaseQuery) -> BaseQuery:
        return add_to.filter(BaseKey.word.like(f"{key}%")) \
            if partial_results else add_to.filter(BaseKey.word == key)

    @staticmethod
    def _filter_key_case_insensitive(
            key: str, partial_results: bool, add_to: BaseQuery) -> BaseQuery:
        return add_to.filter(BaseKey.word.ilike(f"{key}%")) \
            if partial_results else add_to.filter(BaseKey.word.ilike(key))

    @staticmethod
    def _filter_word_case_sensitive(
            key: str, partial_results: bool, add_to: BaseQuery) -> BaseQuery:
        return add_to.filter(BaseWord.name.like(f"{key}%")) \
            if partial_results else add_to.filter(BaseWord.name == key)

    @staticmethod
    def _filter_word_case_insensitive(
            key: str, partial_results: bool, add_to: BaseQuery) -> BaseQuery:
        return add_to.filter(BaseWord.name.ilike(f"{key}%")) \
            if partial_results else add_to.filter(BaseWord.name.ilike(key))
