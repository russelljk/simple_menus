# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Menu'
        db.create_table(u'simple_menus_menu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('schema', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'simple_menus', ['Menu'])


    def backwards(self, orm):
        # Deleting model 'Menu'
        db.delete_table(u'simple_menus_menu')


    models = {
        u'simple_menus.menu': {
            'Meta': {'object_name': 'Menu'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schema': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['simple_menus']