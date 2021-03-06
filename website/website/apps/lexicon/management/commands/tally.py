# -*- coding: utf-8 -*-
import reversion
from django.db.models import Count
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.core.models import Language

def condense_classification(classif):
    condensers = {
        'Austronesian': "An",
        "Malayo-Polynesian": "MP",
        "Central-Eastern": "CE",
        "Eastern": "E",
        "South Halmahera-West New Guinea": "SHWNG",
        "Western Oceanic": "WOc",
        "Oceanic": "Oc",
        "West New Guinea": "WNG",
        
    }
    for old, new in condensers.items():
        classif = classif.replace(old, new)
    return classif


class Command(BaseCommand):
    args = 'tally'
    help = 'Tallys the counts of language data'
    output_transaction = True
        
    def handle(self, *args, **options):
        tally = {}
        families = {}
        languages = Language.objects.annotate(count=Count('lexicon')).all()
        #languages = languages.filter(count__gt=0)
        languages = languages.order_by("classification")
        
        prev_classif = None
        total = 0
        for count, lang in enumerate(languages, 1):
            if lang.classification != prev_classif:
                print condense_classification(lang.classification)
            
            if lang.count < 50:
                strength = '   '
            elif lang.count < 100:
                strength = '*  '
            elif lang.count < 200:
                strength = '** '
            else:
                strength = '***'
                
            print " ".join([
                "\t", 
                '%3d' % count,
                "%3s" % lang.isocode, 
                unicode(lang).ljust(50), 
                '%5d' % lang.count, 
                strength
            ])
            tally[strength] = tally.get(strength, 0) + 1
            
            for family in lang.family.all():
                families[family] = families.get(family, 0) + 1
                
            prev_classif = lang.classification
            total += lang.count
            
        print '-' * 76
        print '%d languages' % count
        print '%d lexical items' % total
        print '-' * 76
        families = sorted(families.items(), key=lambda x: x[1], reverse=True)
        for f, n in families:
            print ' %20s = %3d' % (f, n)
        print '-' * 76
        print '   0-50 = %3d' % tally['   ']
        print ' 50-100 = %3d' % tally['*  ']
        print '100-200 = %3d' % tally['** ']
        print '200-+   = %3d' % tally['***']
        print '-' * 76
        
