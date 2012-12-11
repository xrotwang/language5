from django.conf.urls import *
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from website.apps.core.views import LanguageIndex
from website.apps.core.views import SourceIndex, SourceDetail
from website.apps.core.views import FamilyIndex, FamilyDetail

from website.apps.lexicon.views import WordIndex, WordDetail

from sitemap import FamilySitemap, LanguageSitemap, SourceSitemap, WordSitemap

urlpatterns = patterns('',
    # Main Page / Home
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    
    # About
    url(r'^about', TemplateView.as_view(template_name="about.html"), name="about"),
    
    # ------------------------------------------------------------------------ #
    # Core
    # ------------------------------------------------------------------------ #
    
    # Language-Index: Show all languages
    url(r'^language/$', LanguageIndex.as_view(), name="language-index"),
    
    # Source-Index: Show all sources
    url(r'^source/$', SourceIndex.as_view(), name="source-index"),
    
    # Family-Index: Show all families
    url(r'^family/$', FamilyIndex.as_view(), name="family-index"),
    
    # Language-Detail: Show the given language
    url(r'^language/(?P<language>.+)$', 
        'website.apps.core.views.language_detail', 
        name="language-detail"
    ),
    
    # Source-Detail: Show the given source
    url(r'^source/(?P<slug>.+)$', SourceDetail.as_view(), name="source-detail"),

    # Family-Detail: Show the given family
    url(r'^family/(?P<slug>.+)$', FamilyDetail.as_view(), name="family-detail"),

    # ISO Lookup: redirects to the language page
    url(r'^iso/(?P<iso>\w{3})$', 
        'website.apps.core.views.iso_lookup', 
        name="iso-lookup"
    ),
    
    # ------------------------------------------------------------------------ #
    # Lexicon
    # ------------------------------------------------------------------------ #
    
    # Word-Index: Show all words
    url(r'^word/$', WordIndex.as_view(), name="word-index"),
    
    # Word-Detail: Show the given word
    url(r'^word/(?P<slug>.+)$', WordDetail.as_view(), name="word-detail"),
    
    # Subset-Detail: Show the given word subset
    url(r'^word/\?subset=(?P<slug>.+)$', WordDetail.as_view(), name="subset-detail"),


    # ------------------------------------------------------------------------ #
    # Classification 
    # ------------------------------------------------------------------------ #    
    url(r'^classification/$', 'website.apps.classification.views.show', name="classification"),
    url(r'^classification/(?P<group_id>.+)$', 'website.apps.classification.views.show', name="classification"),

    # ------------------------------------------------------------------------ #
    # Data entry
    # ------------------------------------------------------------------------ #    
    #url(r'^entry/language$', GenericEntry.as_view(), name="entry-generic"),
    
    
    
    # ------------------------------------------------------------------------ #
    # Misc
    # ------------------------------------------------------------------------ #
    # search page
    url(r"^search/", include('watson.urls', namespace='watson')),
    
    # Sitemap
    (r'^sitemap\.xml$', 
           'django.contrib.sitemaps.views.sitemap', 
           {'sitemaps': {
                'families': FamilySitemap, 
                'languages': LanguageSitemap,
                'sources': SourceSitemap,
                'words': WordSitemap,
           }}
       ),
    # Robots.txt
    (r'^robots\.txt$', include('robots.urls')),
    
    # OAI:
    (r'^oai/', include('website.apps.olac.urls')),
    
    # ADMIN
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
