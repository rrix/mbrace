from django.db import models
from django.contrib.auth.models import User


class Hugger(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=5)
    last_location = models.CharField(max_length=20) # TODO: Pull GeoDjango in to the mix
    phone_number = models.CharField(max_length=20) # XXX: Make sure this is US style using https://docs.djangoproject.com/en/1.4/ref/contrib/localflavor/#django.contrib.localflavor.us.models.PhoneNumberField
    email = models.EmailField(null=True)

    def filled_out(self):
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
    user_delivering = models.ForeignKey('Hugger', related_name='deliverer_set')
    review_1 = models.ForeignKey('Review', related_name='requestor_review_set')
    review_2 = models.ForeignKey('Review', related_name='deliverer_review_set')

class Review(models.Model):
    rating = models.SmallIntegerField()
    notes = models.TextField()

    author = models.ForeignKey('Hugger', related_name='review_author_set')
    owner = models.ForeignKey('Hugger', related_name='review_for_set')

