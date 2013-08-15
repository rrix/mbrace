from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django_facebook.models import FacebookProfileModel

from django_facebook import signals
#from celeryqueue.tasks import update_friends
import celeryqueue.tasks


class Hugger(AbstractUser, FacebookProfileModel):
    objects = UserManager()
    zip_code = models.CharField(max_length=5, null=True)
    # TODO: Pull GeoDjango in to the mix
    last_location = models.CharField(max_length=512, null=True)
    # XXX: Make sure this is US style using https://docs.djangoproject.com/en/1.4/ref/contrib/localflavor/#django.contrib.localflavor.us.models.PhoneNumberField
    phone_number = models.CharField(max_length=20, null=True)
    last_hug_date = models.DateTimeField(null=True)

    friend_objects = models.ManyToManyField('Hugger')

    def has_open_hugs(self):
        """
        This goes through the user's hugs, both requested and delivering, and
        makes sure that none of them are open.
        """
        for meeting in self.requestor_set.all():
            if meeting.open(self) is True:
                return True

        return False

    def display_name(self, requestor):
        """
        This returns username or full name, depending on whether or not the
        requestor is a facebook friend of the user or not.
        """
        display_name = u''
        try:
            friend = self.friend_objects.get(id=requestor.id)
            display_name = self.facebook_name
        except:
            friend = None
            display_name = self.username

        return display_name

    def filled_out(self):
        """This is basically a validation, but not enforced at the model
        level, just at the view level. Makes sure that name, zip email and
        phone number are added to a profile"""
        is_valid = True

        if self.zip_code == "":
            is_valid = False
        if self.email == "":
            is_valid = False
        if self.phone_number == "":
            is_valid = False

        return is_valid


class Meeting(models.Model):
    user_in_need = models.ForeignKey('Hugger', related_name='requestor_set')
    user_delivering = models.ForeignKey('Hugger',
                                        related_name='deliverer_set',
                                        null=True)
    review_1 = models.ForeignKey('Review',
                                 related_name='requestor_review_set',
                                 null=True)
    review_2 = models.ForeignKey('Review',
                                 related_name='deliverer_review_set',
                                 null=True)

    def open(self, for_whom):
        if self.user_delivering is None:
            return True

    @classmethod
    def nearby(self, user):
        # FIXME This should pull from geodjango eventually
        #objects = Meeting.objects.filter(user_in_need__zip_code=user.zip_code)
        objects = Meeting.objects.all()
        return objects


class Review(models.Model):
    rating = models.SmallIntegerField()
    notes = models.TextField()

    author = models.ForeignKey('Hugger', related_name='review_author_set')
    owner = models.ForeignKey('Hugger', related_name='review_for_set')


class Message(models.Model):
    text = models.CharField(max_length=140)
    sender = models.ForeignKey('Hugger')
    meeting = models.ForeignKey('Meeting')


def associate_friends_from_opengraph(sender, user, friends, current_friends, inserted_friends, **kwargs):
    """
    associate_friends_from_opengraph

    Call out to celeryqueue to update the user relationships of friends
    """
    celeryqueue.tasks.update_friends.delay(user=user)

signals.facebook_post_store_friends.connect(associate_friends_from_opengraph)
