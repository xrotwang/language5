#!/usr/bin/env python
#coding=utf-8
import os
import re

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Lexicon, Word, CognateSet, Cognate

from openpyxl import load_workbook

filename = os.path.join(os.environ['IMPORTER_DATAROOT'], '0012_scott1978.xlsx')
is_cognate = re.compile(r"""^(\d+?)""")
languages = {
    'Gende': 'gende',
    'Siane': 'siane',
    'Yabiyufa': 'yaweyuha',
    'Asaro': 'dano-asaro',
    'Gahuku': 'alekano',
    'Benabena': 'benabena',
    'Kamano': 'kamano',
    'Yate': 'inoke-yate',
    'Yagaria': 'yagaria',
    'Fore': 'fore',
    'Gimi': 'gimi',
    'ECF Reconstn': 'proto-eastern-central',
    'Awa': 'awa',
    'Auyana': 'awiyaana',
    'Gadsup': 'gadsup',
    'Tairora': 'tairora-north',
    'EF Reconstn': 'proto-eastern',
}

def process_item(item):
    # ignore completely empty
    if item is None: 
        return None
    assert unicode(item)
    assert item.encode('utf8')
    item = item.strip()
    
    # ignore entries marked as empty
    if item == '/' or item == '\\' or item == '-':
        return None
    
    if item.startswith("''"):
        raise ValueError("ERROR 1: %s" % item)
    
    # start processing properly.
    items = []
    item = item.replace(",", ";").replace(u" ' ", " ; ")
    for i in item.split(";"):
        i = i.strip()
        # get cognate
        cog = is_cognate.findall(i)
        if len(cog):
            assert len(cog) == 1
            try:
                cog = int(cog[0])
            except TypeError:
                raise TypeError("Expecting an int for {}: {}".format(cog, item))
            i = is_cognate.sub('', i)
            i = i.strip()
        else:
            cog = None
        
        if len(i) == 0:
            raise ValueError(u'%r :: %s :: %r' % (item, cog, i))
        
        items.append((i, cog))
    return items

# ------------------------------- #


# get editor
ed = User.objects.get(pk=1)
# create source
SObj = Source.objects.create(
        year=1979, 
        author="Scott", slug="scott1978",
        reference="Scott. 1978. The Fore language of Papua New Guinea. Canberra: Pacific Linguistics",
        bibtex="", comment="",
        editor=ed)

wb = load_workbook(filename=filename)
w = wb.worksheets[0]

header = [_.value for _ in w.columns[0]]

counter = 0
for i in range(1, w.get_highest_column()):
    values = [_.value for _ in w.columns[i]]
    values = dict(zip(header, values))
    
    # ----------------------------------------------------------------
    # WORD
    # get word, yes really.
    word = values.pop(u'Word')
    print i, word
    
    # note get_or_create does not work when transaction management is on...
    try:
        WObj = Word.objects.get(slug=slugify(word))
    except Word.DoesNotExist:
        WObj = Word.objects.create(word=word, slug=slugify(word), editor=ed)
        WObj.save()
    # ----------------------------------------------------------------
    cognate_sets = {}
    
    for language in sorted(values):
        if language is None:
            continue
            
        lslug = languages[language]
        try:
            LObj = Language.objects.get(slug=lslug)
        except Language.DoesNotExist:
            LObj = Language.objects.create(language=language, slug=lslug, editor=ed)
            LObj.save()
            # FOR DEBUGGING ONLY ON LOCAL SITE. PRODUCTION SHOULD 
            # HAVE THIS LANGUAGE ALREADY CREATED!
            print 'ERROR: I should not have needed to create %s' % language
        
        item = process_item(values[language])
        
        if item is not None:
            for entry, cognate in item:
                counter += 1
                print "\t", counter, 'Lexicon', language.ljust(20), entry.ljust(30), cognate
                lex = Lexicon.objects.create(
                    language=LObj, 
                    source=SObj,
                    word=WObj, 
                    entry=entry, 
                    annotation='', 
                    editor=ed
                )
                lex.save()        
                if cognate is not None:
                    cognate_sets[cognate] = cognate_sets.get(cognate, [])
                    cognate_sets[cognate].append(lex)
                
    # Add things with more than one entry to a cognate set
    for cogid, members in cognate_sets.items():
        if len(members) > 1:
            # Add protoform --> <?>
            CogSet = CognateSet.objects.create(
                protoform='?',
                gloss=word,
                source=SObj,
                comment="",
                quality='1', # published
                editor=ed
            )
            CogSet.save()
            counter += 1
            print "\t", counter, 'CognateSet', CogSet
            for m in members:
                counter += 1
                cog = Cognate.objects.create(lexicon=m, cognateset=CogSet, source=SObj, editor=ed)
                cog.save()
                print "\t", counter, 'Cognate', cog, m


print '%d objects created!' % counter