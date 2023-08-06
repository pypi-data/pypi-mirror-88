from kitchenart.log.signal import user_activity_log


class LogSerializerMixin:
    def send_activity_log(self, instance_new, instance_old=None, serializer=None):
        serializer_class = serializer if serializer else self.__class__
        user_activity_log.send(sender=self.context['view'],
                               user=self.context['request'].user,
                               event=self.context['event'],
                               entity=self.context['entity'],
                               serializer=serializer_class,
                               instance_new=instance_new,
                               instance_old=instance_old)
