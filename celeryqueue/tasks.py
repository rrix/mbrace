from celery import task
import core.models


@task
def update_friends(user):
    user.friend_objects.clear()
    for friend in user.friends():
        try:
            user_object = core.models.Hugger.objects.get(facebook_id=friend.facebook_id)[0]
            user.friend_objects.add(user_object)
        except:
            user_object = None

    user.save()
    return user.friend_objects.all()


@task
def update_friends_for_all():
    for user in core.models.Hugger.objects.all():
        update_friends.delay(user=user)
