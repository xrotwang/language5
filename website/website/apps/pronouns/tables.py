import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from website.apps.core.tables import DataTable

from website.apps.pronouns.models import Paradigm, Pronoun, Relationship


class ParadigmIndexTable(DataTable):
    """Paradigm Listing"""
    def render_language(self, record):
        col = tables.LinkColumn('pronouns:detail', args=[record.id])
        return col.render(value=unicode(record), record=unicode(record), bound_column=None)
    
    class Meta(DataTable.Meta):
        model = Paradigm
        order_by = 'language' # default sorting
        sequence = ('id', 'language', 'source')
        exclude = ('editor', 'added', 'comment', 'label')
    Meta.attrs['summary'] = 'Table of Paradigms'


class PronounTable(DataTable):
    """Pronoun Listing"""
    class Meta(DataTable.Meta):
        model = Pronoun
        order_by = 'id' # default sorting
        sequence = ('pronountype', 'comment')
        exclude = ('id', 'editor', 'added', 'paradigm')
    Meta.attrs['summary'] = 'Table of Pronouns'


class PronounRelationshipTable(DataTable):
    """Pronoun Listing"""
    pronoun1 = tables.Column(accessor='pronoun1.pronountype', verbose_name="Pronoun 1")
    pronoun2 = tables.Column(accessor='pronoun2.pronountype', verbose_name="Pronoun 2")
    
    class Meta(DataTable.Meta):
        model = Relationship
        order_by = 'id' # default sorting
        sequence = ('pronoun1', 'relationship', 'pronoun2', 'comment')
        exclude = ('id', 'editor', 'added', 'paradigm')
    Meta.attrs['summary'] = 'Table of Pronoun Paradigm Relationship'