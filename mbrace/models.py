from core.models import Hugger

def associate_friends_from_opengraph(sender, user, friends, current_friends, inserted_friends, **kwargs):
    """
    associate_friends_from_opengraph

    Call out to celeryqueue to update the user instance
    """
    if created:
        update_friends.delay(user=instance)
signals.facebook_post_store_friends.connect(associate_friends_from_opengraph, sender=Hugger)
