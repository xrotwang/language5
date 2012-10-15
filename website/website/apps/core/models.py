from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class TrackedModel(models.Model):
    """Abstract base class containing editorial information"""
    editor = models.ForeignKey(User)
    added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class Source(TrackedModel):
    """Source Details"""
    year = models.IntegerField(blank=True, null=True,
        help_text="Year published")
    author = models.CharField(max_length=255,
        help_text="Short Author list e.g. (Smith et al.)")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for author i.e. author-year (for use in URLS)")
    reference = models.TextField(blank=True, null=True,
        help_text="Reference for Source")
    bibtex = models.TextField(blank=True, null=True,
        help_text="BibTeX entry")
    comment = models.TextField(blank=True, null=True,
        help_text="Private comment on source")
    
    def __unicode__(self):
        if self.year is not None:
            return "%s (%d)" % (self.author, self.year)
        else:
            return self.author
        
    def get_absolute_url(self):
        return reverse('website.apps.core.views.source_detail', args=[self.slug])
    
    class Meta:
        db_table = 'sources'
    

    
class Note(TrackedModel):
    """Notes/Information about a language"""
    language = models.ForeignKey('Language')
    source = models.ForeignKey('Source')
    note = models.TextField(help_text="Note")
    location = models.CharField(max_length=50, blank=True, null=True,
        help_text="Location (e.g. p12)")
    
    def __unicode__(self):
        return u'#%d. %s on %s' % (self.id, self.source, self.language)
    
    class Meta:
        db_table = 'notes'


class Family(TrackedModel):
    """Language families/Subsets"""
    family = models.CharField(max_length=64, unique=True,
        help_text="Language Family")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for language family (for use in URLS)")
    
    def __unicode__(self):
        return self.family
    
    def get_absolute_url(self):
        return reverse('website.apps.core.views.family_detail', args=[self.slug])
    
    class Meta:
        db_table = 'families'
        verbose_name_plural = 'families'
    

class Language(TrackedModel):
    """Stores language information"""
    family = models.ManyToManyField(Family, blank=True)
    language = models.CharField(max_length=64, unique=True, db_index=True,
        help_text="Language Name")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for language (for use in URLS)")
    isocode = models.CharField(max_length=3, blank=True, null=True, db_index=True,
        help_text="3 character ISO-639-3 Code.")
    classification = models.TextField(blank=True, null=True,
        help_text="Classification String")
    information = models.TextField(blank=True, null=True,
        help_text="Information about language")
    
    def __unicode__(self):
        return self.language
    
    def get_absolute_url(self):
        return reverse('website.apps.core.views.language_detail', args=[self.slug])
        
    class Meta:
        unique_together = ("isocode", "language")
        db_table = 'languages'


class AlternateName(TrackedModel):
    """Handles languages with multiple names"""
    language = models.ForeignKey('Language')
    name = models.CharField(max_length=64, unique=True, db_index=True,
        help_text="Alternate Name for this language")
    slug = models.SlugField(max_length=64, unique=True,
        help_text="`Slug` for language (for use in URLS)")
    
    def __unicode__(self):
        return "%d AKA %s" % (self.language.id, self.slug)
        
    class Meta:
        verbose_name_plural = 'Alternate Language Names'
        db_table = 'altnames'


class Link(TrackedModel):
    """Stores links to language appropriate resources"""
    language = models.ForeignKey('Language')
    link = models.URLField(help_text="URL to link")
    description = models.TextField(help_text="Language Description")
    
    def __unicode__(self):
        return "%d %s" % (self.language.id, self.link)

    class Meta:
        verbose_name_plural = "Resource Links"
        db_table = 'links'


class Location(TrackedModel):
    language = models.ForeignKey('Language')
    longitude = models.FloatField(help_text="Longitude")
    latitude = models.FloatField(help_text="Latitiude")

    def __unicode__(self):
        return "%d %2.4f-%2.4f" % (self.language.id, self.longitude, self.latitude)

    class Meta:
        verbose_name_plural = "Geographical Locations"
        db_table = 'locations'

