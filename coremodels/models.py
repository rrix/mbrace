from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=5)
    last_location = models.CharField(max_length=20) # TODO: Pull GeoDjango in to the mix

class Meeting(models.Model):
    user_in_need = models.ForeignKey('User', related_name='requestor_set') 
    user_delivering = models.ForeignKey('User', related_name='deliverer_set')
    review_1 = models.ForeignKey('Review', related_name='requestor_review')
    review_2 = models.ForeignKey('Review', related_name='deliverer_review')

class Review(models.Model):
    rating = models.SmallIntegerField()
    notes = models.TextField()

    author = models.ForeignKey('User', related_name='review_author')
    owner = models.ForeignKey('User', related_name='review_for')

