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
from loglan_db.model_db.base_word import db


class AddonWordGetter:
    """AddonWordGetter model"""

    query: BaseQuery = None
    name: db.Column = None
    event_start_id: db.Column = None
    event_end_id: db.Column = None

    @classmethod
    def by_event(cls, event_id: Union[BaseEvent, int] = None) -> BaseQuery:
        """Query filtered by specified Event (latest by default)

        Args:
          event_id: Union[BaseEvent, int]: Event object or Event.id (int) (Default value = None)

        Returns:
          BaseQuery

        """
        if not event_id:
            event_id = BaseEvent.latest().id

        event_id = BaseEvent.id if isinstance(event_id, BaseEvent) else int(event_id)

        return cls.query.filter(cls.event_start_id <= event_id) \
            .filter(or_(cls.event_end_id > event_id, cls.event_end_id.is_(None))) \
            .order_by(cls.name)

    @classmethod
    def by_name(cls, name: str, case_sensitive: bool = False) -> BaseQuery:
        """Word.Query filtered by specified name

        Args:
          name: str:
          case_sensitive: bool:  (Default value = False)

        Returns:
          BaseQuery

        """
        if case_sensitive:
            return cls.query.filter(cls.name == name)
        return cls.query.filter(cls.name.in_([name, name.lower(), name.upper()]))

    @classmethod
    def by_key(
            cls, key: Union[BaseKey, str],
            language: str = None,
            case_sensitive: bool = False) -> BaseQuery:
        """Word.Query filtered by specified key

        Args:
          key: Union[BaseKey, str]:
          language: str: Language of key (Default value = None)
          case_sensitive: bool:  (Default value = False)

        Returns:
          BaseQuery

        """

        key = BaseKey.word if isinstance(key, BaseKey) else str(key)
        request = cls.query.join(BaseDefinition, t_connect_keys, BaseKey)

        if case_sensitive:
            request = request.filter(BaseKey.word == key)
        else:
            request = request.filter(BaseKey.word.in_([key, key.lower(), key.upper()]))

        if language:
            request = request.filter(BaseKey.language == language)
        return request
