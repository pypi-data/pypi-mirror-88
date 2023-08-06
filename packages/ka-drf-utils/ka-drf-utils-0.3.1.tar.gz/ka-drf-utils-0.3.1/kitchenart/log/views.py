from copy import deepcopy

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from kitchenart.log.signal import user_activity_log
from kitchenart.utils.broker import EventType


class LogViewSetMixin(ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # send log signal
        if not request.user.is_anonymous:
            user_activity_log.send(sender=self,
                                   user=request.user,
                                   event=EventType.created,
                                   entity=self.entity,
                                   instance_old=None,
                                   instance_new=serializer.data)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_old = deepcopy(instance)

        result = super().update(request, *args, **kwargs)

        # data old
        serializer_old = self.get_serializer(instance_old, context={'request': request})
        data_old = serializer_old.data

        # data new
        serializer_new = self.get_serializer(self.get_object(), context={'request': request})
        data_new = serializer_new.data

        # send log signal
        if not request.user.is_anonymous:
            user_activity_log.send(sender=self,
                                   user=request.user,
                                   event=EventType.changed,
                                   entity=self.entity,
                                   instance_old=data_old,
                                   instance_new=data_new)

        return result

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        serializer = self.get_serializer(instance, context={'request': request})

        # send log signal
        if not request.user.is_anonymous:
            user_activity_log.send(sender=self,
                                   user=request.user,
                                   event=EventType.deleted,
                                   entity=self.entity,
                                   instance_old=serializer.data,
                                   instance_new=None)

        return Response(status=status.HTTP_204_NO_CONTENT)
