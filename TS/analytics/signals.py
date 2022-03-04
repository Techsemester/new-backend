from django.dispatch import Signal

object_viewed_signal = Signal(providing_args=['instance', 'request', 'user', 'actions', 'replies'])


def manageUsers(objects):
    """
        get object to create notifications
    """

    user = objects.get('user')
    replies = objects.get('replies')
    request = objects.get('request')
    actions = objects.get('actions')
    instance = objects.get('instance')

    if user != replies:
        object_viewed_signal.send(instance.__class__, instance=instance, request=request, user=user, actions=actions,
                                  replies=replies)
