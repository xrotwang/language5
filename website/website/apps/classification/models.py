from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from website.apps.core.models import Language

class Subgroup(MPTTModel):
    name = models.CharField(max_length=50, unique=False, db_index=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    language = models.ManyToManyField(Language, blank=True)
    
    class MPTTMeta:
        order_insertion_by = ['name']

