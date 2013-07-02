# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Hugger.user'
        db.delete_column(u'core_hugger', 'user_id')

        # Adding field 'Hugger.password'
        db.add_column(u'core_hugger', 'password',
                      self.gf('django.db.models.fields.CharField')(default='changeme', max_length=128),
                      keep_default=False)

        # Adding field 'Hugger.last_login'
        db.add_column(u'core_hugger', 'last_login',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Hugger.is_superuser'
        db.add_column(u'core_hugger', 'is_superuser',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Hugger.username'
        db.add_column(u'core_hugger', 'username',
                      self.gf('django.db.models.fields.CharField')(default='changeme', unique=True, max_length=30),
                      keep_default=False)

        # Adding field 'Hugger.first_name'
        db.add_column(u'core_hugger', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.last_name'
        db.add_column(u'core_hugger', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.is_staff'
        db.add_column(u'core_hugger', 'is_staff',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Hugger.is_active'
        db.add_column(u'core_hugger', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Hugger.date_joined'
        db.add_column(u'core_hugger', 'date_joined',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Hugger.about_me'
        db.add_column(u'core_hugger', 'about_me',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.facebook_id'
        db.add_column(u'core_hugger', 'facebook_id',
                      self.gf('django.db.models.fields.BigIntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.access_token'
        db.add_column(u'core_hugger', 'access_token',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.facebook_name'
        db.add_column(u'core_hugger', 'facebook_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.facebook_profile_url'
        db.add_column(u'core_hugger', 'facebook_profile_url',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.website_url'
        db.add_column(u'core_hugger', 'website_url',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.blog_url'
        db.add_column(u'core_hugger', 'blog_url',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.date_of_birth'
        db.add_column(u'core_hugger', 'date_of_birth',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.gender'
        db.add_column(u'core_hugger', 'gender',
                      self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.raw_data'
        db.add_column(u'core_hugger', 'raw_data',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.facebook_open_graph'
        db.add_column(u'core_hugger', 'facebook_open_graph',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Hugger.new_token_required'
        db.add_column(u'core_hugger', 'new_token_required',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Hugger.image'
        db.add_column(u'core_hugger', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True),
                      keep_default=False)

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


        # Changing field 'Hugger.email'
        db.alter_column(u'core_hugger', 'email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Hugger.user'
        raise RuntimeError("Cannot reverse this migration. 'Hugger.user' and its values cannot be restored.")
        # Deleting field 'Hugger.password'
        db.delete_column(u'core_hugger', 'password')

        # Deleting field 'Hugger.last_login'
        db.delete_column(u'core_hugger', 'last_login')

        # Deleting field 'Hugger.is_superuser'
        db.delete_column(u'core_hugger', 'is_superuser')

        # Deleting field 'Hugger.username'
        db.delete_column(u'core_hugger', 'username')

        # Deleting field 'Hugger.first_name'
        db.delete_column(u'core_hugger', 'first_name')

        # Deleting field 'Hugger.last_name'
        db.delete_column(u'core_hugger', 'last_name')

        # Deleting field 'Hugger.is_staff'
        db.delete_column(u'core_hugger', 'is_staff')

        # Deleting field 'Hugger.is_active'
        db.delete_column(u'core_hugger', 'is_active')

        # Deleting field 'Hugger.date_joined'
        db.delete_column(u'core_hugger', 'date_joined')

        # Deleting field 'Hugger.about_me'
        db.delete_column(u'core_hugger', 'about_me')

        # Deleting field 'Hugger.facebook_id'
        db.delete_column(u'core_hugger', 'facebook_id')

        # Deleting field 'Hugger.access_token'
        db.delete_column(u'core_hugger', 'access_token')

        # Deleting field 'Hugger.facebook_name'
        db.delete_column(u'core_hugger', 'facebook_name')

        # Deleting field 'Hugger.facebook_profile_url'
        db.delete_column(u'core_hugger', 'facebook_profile_url')

        # Deleting field 'Hugger.website_url'
        db.delete_column(u'core_hugger', 'website_url')

        # Deleting field 'Hugger.blog_url'
        db.delete_column(u'core_hugger', 'blog_url')

        # Deleting field 'Hugger.date_of_birth'
        db.delete_column(u'core_hugger', 'date_of_birth')

        # Deleting field 'Hugger.gender'
        db.delete_column(u'core_hugger', 'gender')

        # Deleting field 'Hugger.raw_data'
        db.delete_column(u'core_hugger', 'raw_data')

        # Deleting field 'Hugger.facebook_open_graph'
        db.delete_column(u'core_hugger', 'facebook_open_graph')

        # Deleting field 'Hugger.new_token_required'
        db.delete_column(u'core_hugger', 'new_token_required')

        # Deleting field 'Hugger.image'
        db.delete_column(u'core_hugger', 'image')

        # Removing M2M table for field groups on 'Hugger'
        db.delete_table(db.shorten_name(u'core_hugger_groups'))

        # Removing M2M table for field user_permissions on 'Hugger'
        db.delete_table(db.shorten_name(u'core_hugger_user_permissions'))


        # Changing field 'Hugger.email'
        db.alter_column(u'core_hugger', 'email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))

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
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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