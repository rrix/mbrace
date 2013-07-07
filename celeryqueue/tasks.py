from celery import task
import core.models

@task
def update_friends(user):
    user.friends = []
    for friend in user.friends():
        user_object = core.models.Hugger.objects.find(facebook_id=friend.facebook_id)[0]
        if user_object:
            user.friends.append(user_object)

    user.save()


@task
def update_friends_for_all():
    for user in core.models.Hugger.objects.all():
        update_friends.delay(user=user)
