from rest_framework import status
from rest_framework.response import Response

from kitchenart.log.signal import user_activity_log
from kitchenart.utils.broker import EventType


class LogViewSetMixin:
    def get_serializer_context(self):
        event = None
        if self.action in ["update", "partial_update"]:
            event = EventType.changed
        elif self.action == "create":
            event = EventType.created
        elif self.action == "destroy":
            event = EventType.deleted

        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'entity': self.entity,
            'event': event
        }

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        # send log signal
        user_activity_log.send(sender=self,
                               user=request.user,
                               event=EventType.deleted,
                               entity=self.entity,
                               serializer=self.get_serializer_class(),
                               instance_old=instance,
                               instance_new=None)

        return Response(status=status.HTTP_204_NO_CONTENT)
