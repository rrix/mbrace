from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django_facebook.models import FacebookProfileModel


class Hugger(AbstractUser, FacebookProfileModel):
    objects = UserManager()
    name = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=5)
    # TODO: Pull GeoDjango in to the mix
    last_location = models.CharField(max_length=100)
    # XXX: Make sure this is US style using https://docs.djangoproject.com/en/1.4/ref/contrib/localflavor/#django.contrib.localflavor.us.models.PhoneNumberField
    phone_number = models.CharField(max_length=20)

    def filled_out(self):
        """This is basically a validation, but not enforced at the model
        level, just at the view level. Makes sure that name, zip email and
        phone number are added to a profile"""
        is_valid = True

        if self.name == "":
            is_valid = False
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

    @classmethod
    def nearby(self, user):
        objects = Meeting.objects.filter(user_in_need__zip_code=user.zip_code)
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
