from django.db import models
from django.contrib.auth.models import User


class Hugger(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=5)
    last_location = models.CharField(max_length=20) # TODO: Pull GeoDjango in to the mix

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

