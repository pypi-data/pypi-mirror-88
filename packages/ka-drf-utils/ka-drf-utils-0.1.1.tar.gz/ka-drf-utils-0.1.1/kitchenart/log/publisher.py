from typing import Type

import msgpack
from django.utils.timezone import now
from rest_framework.serializers import BaseSerializer

from kitchenart.utils.broker import BasicPublisher, EventType


class LogPublisher(BasicPublisher):
    def construct_message(self,
                          actor: str,
                          entity: str,
                          event: EventType,
                          desc: str,
                          data_old: dict =None,
                          data_new: dict =None) -> bytes:
        """ Construct the message to be sent.
        """
        message = {
            "event_time": now().isoformat(),
            "actor": actor,
            "event": event.value,
            "entity": entity,
            "description": desc,
            "data_old": data_old,
            "data_new": data_new
        }
        return msgpack.packb(message, use_bin_type=True)

    def publish(self,
                actor: str,
                event: EventType,
                entity: str,
                desc: str,
                data_serializer: Type[BaseSerializer],
                instance_old: any =None,
                instance_new: any =None) -> None:

        data_old = None
        if instance_old:
            data_old = data_serializer(instance_old, context=self.serializer_context()).data

        data_new = None
        if instance_new:
            data_new = data_serializer(instance_new, context=self.serializer_context()).data

        body = self.construct_message(
            actor=actor,
            entity=entity,
            event=event,
            desc=desc,
            data_old=data_old,
            data_new=data_new
        )

        routing_key = f'log.{entity}.{event.value}'
        self._publish(body, routing_key)
