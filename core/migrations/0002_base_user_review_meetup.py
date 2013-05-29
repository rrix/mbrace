# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Meeting'
        db.create_table(u'coremodels_meeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_in_need', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requestor_set', to=orm['coremodels.User'])),
            ('user_delivering', self.gf('django.db.models.fields.related.ForeignKey')(related_name='deliverer_set', to=orm['coremodels.User'])),
            ('review_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requestor_review_set', to=orm['coremodels.Review'])),
            ('review_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='deliverer_review_set', to=orm['coremodels.Review'])),
        ))
        db.send_create_signal(u'coremodels', ['Meeting'])

        # Adding model 'User'
        db.create_table(u'coremodels_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('last_location', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'coremodels', ['User'])

        # Adding model 'Review'
        db.create_table(u'coremodels_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rating', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='review_author_set', to=orm['coremodels.User'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='review_for_set', to=orm['coremodels.User'])),
        ))
        db.send_create_signal(u'coremodels', ['Review'])


    def backwards(self, orm):
        # Deleting model 'Meeting'
        db.delete_table(u'coremodels_meeting')

        # Deleting model 'User'
        db.delete_table(u'coremodels_user')

        # Deleting model 'Review'
        db.delete_table(u'coremodels_review')


    models = {
        u'coremodels.meeting': {
            'Meta': {'object_name': 'Meeting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requestor_review'", 'to': u"orm['coremodels.Review']"}),
            'review_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deliverer_review'", 'to': u"orm['coremodels.Review']"}),
            'user_delivering': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deliverer_set'", 'to': u"orm['coremodels.User']"}),
            'user_in_need': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requestor_set'", 'to': u"orm['coremodels.User']"})
        },
        u'coremodels.review': {
            'Meta': {'object_name': 'Review'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'review_author'", 'to': u"orm['coremodels.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'review_for'", 'to': u"orm['coremodels.User']"}),
            'rating': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'coremodels.user': {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_location': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['coremodels']
