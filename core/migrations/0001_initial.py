# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hugger'
        db.create_table(u'core_hugger', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('about_me', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('facebook_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True, null=True, blank=True)),
            ('access_token', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('facebook_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('facebook_profile_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('website_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('blog_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('raw_data', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('facebook_open_graph', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('new_token_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('last_location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('last_hug_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'core', ['Hugger'])

        # Adding M2M table for field groups on 'Hugger'
        m2m_table_name = db.shorten_name(u'core_hugger_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hugger', models.ForeignKey(orm[u'core.hugger'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['hugger_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Hugger'
        m2m_table_name = db.shorten_name(u'core_hugger_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hugger', models.ForeignKey(orm[u'core.hugger'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['hugger_id', 'permission_id'])

        # Adding M2M table for field friend_objects on 'Hugger'
        m2m_table_name = db.shorten_name(u'core_hugger_friend_objects')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_hugger', models.ForeignKey(orm[u'core.hugger'], null=False)),
            ('to_hugger', models.ForeignKey(orm[u'core.hugger'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_hugger_id', 'to_hugger_id'])

        # Adding model 'Meeting'
        db.create_table(u'core_meeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_in_need', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requestor_set', to=orm['core.Hugger'])),
            ('user_delivering', self.gf('django.db.models.fields.related.ForeignKey')(related_name='deliverer_set', null=True, to=orm['core.Hugger'])),
            ('review_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requestor_review_set', null=True, to=orm['core.Review'])),
            ('review_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='deliverer_review_set', null=True, to=orm['core.Review'])),
        ))
        db.send_create_signal(u'core', ['Meeting'])

        # Adding model 'Review'
        db.create_table(u'core_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rating', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='review_author_set', to=orm['core.Hugger'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='review_for_set', to=orm['core.Hugger'])),
        ))
        db.send_create_signal(u'core', ['Review'])

        # Adding model 'Message'
        db.create_table(u'core_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Hugger'])),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Meeting'])),
        ))
        db.send_create_signal(u'core', ['Message'])


    def backwards(self, orm):
        # Deleting model 'Hugger'
        db.delete_table(u'core_hugger')

        # Removing M2M table for field groups on 'Hugger'
        db.delete_table(db.shorten_name(u'core_hugger_groups'))

        # Removing M2M table for field user_permissions on 'Hugger'
        db.delete_table(db.shorten_name(u'core_hugger_user_permissions'))

        # Removing M2M table for field friend_objects on 'Hugger'
        db.delete_table(db.shorten_name(u'core_hugger_friend_objects'))

        # Deleting model 'Meeting'
        db.delete_table(u'core_meeting')

        # Deleting model 'Review'
        db.delete_table(u'core_review')

        # Deleting model 'Message'
        db.delete_table(u'core_message')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.hugger': {
            'Meta': {'object_name': 'Hugger'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'blog_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facebook_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_open_graph': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_profile_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'friend_objects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Hugger']", 'symmetrical': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_hug_date': ('django.db.models.fields.DateTimeField', [], {}),
            'last_location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'new_token_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'raw_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'website_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'core.meeting': {
            'Meta': {'object_name': 'Meeting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requestor_review_set'", 'null': 'True', 'to': u"orm['core.Review']"}),
            'review_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deliverer_review_set'", 'null': 'True', 'to': u"orm['core.Review']"}),
            'user_delivering': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deliverer_set'", 'null': 'True', 'to': u"orm['core.Hugger']"}),
            'user_in_need': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requestor_set'", 'to': u"orm['core.Hugger']"})
        },
        u'core.message': {
            'Meta': {'object_name': 'Message'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Meeting']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Hugger']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'core.review': {
            'Meta': {'object_name': 'Review'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'review_author_set'", 'to': u"orm['core.Hugger']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'review_for_set'", 'to': u"orm['core.Hugger']"}),
            'rating': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['core']