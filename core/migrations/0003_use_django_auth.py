# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'core_user')

        # Adding model 'Hugger'
        db.create_table(u'core_hugger', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('last_location', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'core', ['Hugger'])


        # Changing field 'Meeting.user_in_need'
        db.alter_column(u'core_meeting', 'user_in_need_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Hugger']))

        # Changing field 'Meeting.user_delivering'
        db.alter_column(u'core_meeting', 'user_delivering_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Hugger']))

        # Changing field 'Review.owner'
        db.alter_column(u'core_review', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Hugger']))

        # Changing field 'Review.author'
        db.alter_column(u'core_review', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Hugger']))

    def backwards(self, orm):
        # Adding model 'User'
        db.create_table(u'core_user', (
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('last_location', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'core', ['User'])

        # Deleting model 'Hugger'
        db.delete_table(u'core_hugger')


        # Changing field 'Meeting.user_in_need'
        db.alter_column(u'core_meeting', 'user_in_need_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User']))

        # Changing field 'Meeting.user_delivering'
        db.alter_column(u'core_meeting', 'user_delivering_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User']))

        # Changing field 'Review.owner'
        db.alter_column(u'core_review', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User']))

        # Changing field 'Review.author'
        db.alter_column(u'core_review', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.hugger': {
            'Meta': {'object_name': 'Hugger'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_location': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'core.meeting': {
            'Meta': {'object_name': 'Meeting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requestor_review'", 'to': u"orm['core.Review']"}),
            'review_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deliverer_review'", 'to': u"orm['core.Review']"}),
            'user_delivering': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deliverer_set'", 'to': u"orm['core.Hugger']"}),
            'user_in_need': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requestor_set'", 'to': u"orm['core.Hugger']"})
        },
        u'core.review': {
            'Meta': {'object_name': 'Review'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'review_author'", 'to': u"orm['core.Hugger']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'review_for'", 'to': u"orm['core.Hugger']"}),
            'rating': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['core']
