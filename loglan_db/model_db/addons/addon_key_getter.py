
from typing import Union

from flask_sqlalchemy import BaseQuery
from sqlalchemy import or_

from loglan_db.model_db.base_key import db
from loglan_db.model_db.base_event import BaseEvent
from loglan_db.model_db.base_word import BaseWord
from loglan_db.model_db.base_definition import BaseDefinition
from loglan_db.model_db.base_connect_tables import t_connect_keys


class AddonKeyGetter:
    """AddonKeyGetter model"""

    query: BaseQuery = None
    word: db.Column = None
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
        return cls._filter_event(event_id, request)

    @classmethod
    def _filter_event(cls, event_id: Union[BaseEvent, int], add_to: BaseQuery) -> BaseQuery:
        return add_to.join(t_connect_keys).join(BaseDefinition).join(BaseWord) \
            .filter(BaseWord.event_start_id <= event_id) \
            .filter(or_(BaseWord.event_end_id > event_id, BaseWord.event_end_id.is_(None)))
