from django.core.cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.utils import timezone

from website.apps.lexicon.models import Word, WordSubset, Lexicon, CognateSet
from website.apps.lexicon.forms import LexiconForm

from django_tables2 import SingleTableView, RequestConfig
from website.apps.lexicon.tables import WordIndexTable, WordLexiconTable
from website.apps.lexicon.tables import WordLexiconEditTable
from website.apps.lexicon.tables import CognateSetIndexTable, CognateSetDetailTable

# for WordEdit
from django.forms.models import modelformset_factory
from website.apps.lexicon.forms import WordForm


class WordIndex(SingleTableView):
    """Word Index"""
    model = Word
    template_name = 'lexicon/word_index.html'
    table_class = WordIndexTable
    table_pagination = {"per_page": 50}
    
    def get_queryset(self):
        # filter on subset if necessary
        if 'subset' in self.request.GET:
            self.subset = get_object_or_404(WordSubset, slug=self.request.GET['subset'])
            return self.subset.words.all().annotate(count=Count("lexicon"))
        else:
            self.subset = None
            return Word.objects.annotate(count=Count('lexicon'))
    
    def get_context_data(self, **kwargs):
        context = super(WordIndex, self).get_context_data(**kwargs)
        context['subset'] = self.subset
        context['subsets'] = WordSubset.objects.all()
        return context
    

class WordDetail(DetailView):
    """Word Detail"""
    model = Word
    template_name = 'lexicon/word_detail.html'
    table_class = WordLexiconTable
    table_pagination = {"per_page": 50}
    
    def get_context_data(self, **kwargs):
        context = super(WordDetail, self).get_context_data(**kwargs)
        
        qset = kwargs['object'].lexicon_set.select_related().all()
        if self.request.user.is_authenticated():
            context['lexicon'] = WordLexiconEditTable(qset)
        else:
            context['lexicon'] = WordLexiconTable(qset)
        RequestConfig(self.request).configure(context['lexicon'])
            
        try:
            context['lexicon'].paginate(page=self.request.GET.get('page', 1), per_page=50)
        except EmptyPage: # 404 on a empty page
            raise Http404
        except PageNotAnInteger: # 404 on invalid page number
            raise Http404
        return context


class LexiconDetail(DetailView):
    """Lexicon Detail"""
    model = Lexicon
    template_name = 'lexicon/lexicon_detail.html'


class CognateSetIndex(DetailView):
    """Cognate Set Index"""
    model = CognateSet
    template_name = 'lexicon/cognate_index.html'

    @method_decorator(login_required) # ensure logged in
    def dispatch(self, *args, **kwargs):
        return super(LexiconEdit, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CognateSetIndex, self).get_context_data(**kwargs)
        
        qset = kwargs['object'].lexicon_set.select_related().all()
        if self.request.user.is_authenticated():
            context['lexicon'] = WordLexiconEditTable(qset)
        else:
            context['lexicon'] = WordLexiconTable(qset)
        RequestConfig(self.request).configure(context['lexicon'])
        
        try:
            context['lexicon'].paginate(page=self.request.GET.get('page', 1), per_page=50)
        except EmptyPage: # 404 on a empty page
            raise Http404
        except PageNotAnInteger: # 404 on invalid page number
            raise Http404
        return context


class CognateSetIndex(SingleTableView):
    """Cognate Set Index"""
    model = CognateSet
    template_name = 'lexicon/cognateset_index.html'
    table_class = CognateSetIndexTable
    table_pagination = {"per_page": 100}
    
    def get_queryset(self):
        return CognateSet.objects.all().annotate(count=Count('lexicon'))
    
    @method_decorator(login_required) # ensure logged in
    def dispatch(self, *args, **kwargs):
        return super(CognateSetIndex, self).dispatch(*args, **kwargs)


class CognateSetDetail(DetailView):
    """Cognate Set Detail"""
    model = CognateSet
    template_name = 'lexicon/cognateset_detail.html'
    table_pagination = {"per_page": 100}
    
    def get_context_data(self, **kwargs):
        context = super(CognateSetDetail, self).get_context_data(**kwargs)
        qset = kwargs['object'].lexicon.select_related().all()
        context['lexicon'] = CognateSetDetailTable(qset)
        RequestConfig(self.request).configure(context['lexicon'])

        try:
            context['lexicon'].paginate(page=self.request.GET.get('page', 1), per_page=50)
        except EmptyPage: # 404 on a empty page
            raise Http404
        except PageNotAnInteger: # 404 on invalid page number
            raise Http404
        return context

    @method_decorator(login_required) # ensure logged in
    def dispatch(self, *args, **kwargs):
        return super(CognateSetDetail, self).dispatch(*args, **kwargs)


class LexiconEdit(UpdateView):
    """Lexicon Editor"""
    model = Lexicon
    form_class = LexiconForm
    template_name_suffix = '_edit'
    
    def form_valid(self, form):
        from django.utils import timezone
        import reversion
        form.instance.editor = self.request.user
        form.instance.added = timezone.now()
        with reversion.create_revision():
            form.save()
        return super(LexiconEdit, self).form_valid(form)
    
    @method_decorator(login_required) # ensure logged in
    def dispatch(self, *args, **kwargs):
        return super(LexiconEdit, self).dispatch(*args, **kwargs)




@login_required()
def word_edit(request, slug):
    w = get_object_or_404(Word, slug=slug)
    GenericFormSet = modelformset_factory(Lexicon, form=WordForm, extra=0)
    formset = GenericFormSet(request.POST or None, queryset=w.lexicon_set.all())
    
    if request.POST and formset.is_valid():
        import reversion
        for form in formset:
            if form.is_valid() and len(form.changed_data):
                # if form is valid and some fields have changed
                # two stages here to set default fields
                with reversion.create_revision():
                    obj = form.save(commit=False)
                    obj.editor = request.user
                    obj.added = timezone.now()
                    obj.save()
        return redirect(w)
    else:
        return render_to_response('lexicon/word_edit.html', 
                                  {'word': w, 'formset': formset},
                                  context_instance=RequestContext(request))


@login_required()
def word_alignment(request, slug):
    from lingpy import Multiple
    from website.apps.lexicon.tables import AlignmentTable
    w = get_object_or_404(Word, slug=slug)
    entries = w.lexicon_set.select_related().all()
    
    # as MSA is seriously computationally expensive, we check if we can re-use a cached MSA.
    # first -- we set a cache value to be the raw string of all the entries. If one
    # entry is changed, then this cache_value will be different.
    cache_value = "".join(sorted([e.entry for e in entries]))
    
    if cache.get("msa-check-%s" % slug) == cache_value:
        # have not changed. Get cache value
        records = cache.get("msa-%s" % slug)
    else:
        # ... regenerate..
        # align....
        msa = Multiple([e.entry for e in entries])
        msa.prog_align()
    
        # tabulate....
        records = []
        for i, e in enumerate(entries):
            e.alignment = "".join(msa.alm_matrix[i])
            records.append(e)
        
        # update cache...
        cache.set('msa-check-%s' % slug, cache_value, None)  # None = never expire
        cache.set('msa-%s' % slug, records, None)  # None = never expire
    
    table = AlignmentTable(records)
    
    return render_to_response('lexicon/word_alignment.html', 
                              {'object': w, 'lexicon': table},
                              context_instance=RequestContext(request))
