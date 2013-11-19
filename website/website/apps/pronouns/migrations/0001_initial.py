# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PronounType'
        db.create_table(u'pronouns_pronountype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('alignment', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('person', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lexicon.Word'])),
        ))
        db.send_create_signal(u'pronouns', ['PronounType'])

        # Adding model 'Paradigm'
        db.create_table('paradigms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Language'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Source'])),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pronouns', ['Paradigm'])

        # Adding model 'Pronoun'
        db.create_table('pronouns', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('paradigm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pronouns.Paradigm'])),
            ('pronountype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pronouns.PronounType'])),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pronouns', ['Pronoun'])

        # Adding M2M table for field entries on 'Pronoun'
        m2m_table_name = db.shorten_name('pronouns_entries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pronoun', models.ForeignKey(orm[u'pronouns.pronoun'], null=False)),
            ('lexicon', models.ForeignKey(orm[u'lexicon.lexicon'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pronoun_id', 'lexicon_id'])

        # Adding model 'Relationship'
        db.create_table('pronoun_relationships', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('paradigm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pronouns.Paradigm'])),
            ('pronoun1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pronoun1', to=orm['pronouns.Pronoun'])),
            ('pronoun2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pronoun2', to=orm['pronouns.Pronoun'])),
            ('entry1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entry1', to=orm['lexicon.Lexicon'])),
            ('entry2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entry2', to=orm['lexicon.Lexicon'])),
            ('relationship', self.gf('django.db.models.fields.CharField')(default=None, max_length=2, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pronouns', ['Relationship'])

        # Adding model 'Rule'
        db.create_table('pronoun_rules', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('paradigm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pronouns.Paradigm'])),
            ('rule', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'pronouns', ['Rule'])

        # Adding M2M table for field relationships on 'Rule'
        m2m_table_name = db.shorten_name('pronoun_rules_relationships')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rule', models.ForeignKey(orm[u'pronouns.rule'], null=False)),
            ('relationship', models.ForeignKey(orm[u'pronouns.relationship'], null=False))
        ))
        db.create_unique(m2m_table_name, ['rule_id', 'relationship_id'])


    def backwards(self, orm):
        # Deleting model 'PronounType'
        db.delete_table(u'pronouns_pronountype')

        # Deleting model 'Paradigm'
        db.delete_table('paradigms')

        # Deleting model 'Pronoun'
        db.delete_table('pronouns')

        # Removing M2M table for field entries on 'Pronoun'
        db.delete_table(db.shorten_name('pronouns_entries'))

        # Deleting model 'Relationship'
        db.delete_table('pronoun_relationships')

        # Deleting model 'Rule'
        db.delete_table('pronoun_rules')

        # Removing M2M table for field relationships on 'Rule'
        db.delete_table(db.shorten_name('pronoun_rules_relationships'))


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
        u'core.family': {
            'Meta': {'ordering': "['family']", 'object_name': 'Family', 'db_table': "'families'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'family': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'core.language': {
            'Meta': {'ordering': "['language', 'dialect']", 'unique_together': "(('isocode', 'language', 'dialect'),)", 'object_name': 'Language', 'db_table': "'languages'", 'index_together': "[['language', 'dialect']]"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'classification': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dialect': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'family': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Family']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'isocode': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'core.source': {
            'Meta': {'ordering': "['author', 'year']", 'object_name': 'Source', 'db_table': "'sources'", 'index_together': "[['author', 'year']]"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'bibtex': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'year': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'lexicon.lexicon': {
            'Meta': {'ordering': "['entry']", 'object_name': 'Lexicon', 'db_table': "'lexicon'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'annotation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'entry': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'loan': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'loan_source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'loan_source_set'", 'null': 'True', 'to': u"orm['core.Language']"}),
            'phon_entry': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']"}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lexicon.Word']"})
        },
        u'lexicon.word': {
            'Meta': {'ordering': "['word']", 'object_name': 'Word', 'db_table': "'words'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'full': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'word': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        },
        u'pronouns.paradigm': {
            'Meta': {'object_name': 'Paradigm', 'db_table': "'paradigms'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']"})
        },
        u'pronouns.pronoun': {
            'Meta': {'object_name': 'Pronoun', 'db_table': "'pronouns'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'entries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['lexicon.Lexicon']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paradigm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pronouns.Paradigm']"}),
            'pronountype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pronouns.PronounType']"})
        },
        u'pronouns.pronountype': {
            'Meta': {'object_name': 'PronounType'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'alignment': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'person': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lexicon.Word']"})
        },
        u'pronouns.relationship': {
            'Meta': {'object_name': 'Relationship', 'db_table': "'pronoun_relationships'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'entry1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entry1'", 'to': u"orm['lexicon.Lexicon']"}),
            'entry2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entry2'", 'to': u"orm['lexicon.Lexicon']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paradigm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pronouns.Paradigm']"}),
            'pronoun1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pronoun1'", 'to': u"orm['pronouns.Pronoun']"}),
            'pronoun2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pronoun2'", 'to': u"orm['pronouns.Pronoun']"}),
            'relationship': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        u'pronouns.rule': {
            'Meta': {'object_name': 'Rule', 'db_table': "'pronoun_rules'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paradigm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pronouns.Paradigm']"}),
            'relationships': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pronouns.Relationship']", 'null': 'True', 'blank': 'True'}),
            'rule': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['pronouns']