from django.http import Http404
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, Count

from website.apps.core.models import Family, Language, Source
from website.apps.pronouns.models import Paradigm, Pronoun, Relationship, Rule
from website.apps.pronouns.tables import ParadigmIndexTable, PronounTable, PronounRelationshipTable

from website.apps.pronouns.forms import ParadigmForm, RelationshipFormSet
from website.apps.pronouns.forms import create_pronoun_formset, RuleForm

from website.apps.pronouns.tools import add_pronoun_ordering, add_pronoun_table
from website.apps.pronouns.tools import find_identicals, extract_rule

from django_tables2 import SingleTableView


class Index(SingleTableView):
    """Index"""
    model = Paradigm
    template_name = 'pronouns/index.html'
    table_class = ParadigmIndexTable
    table_pagination = {"per_page": 50}

    def get_queryset(self):
        return Paradigm.objects.select_related().all()



def detail(request, paradigm_id):
    try:
        p = Paradigm.objects.select_related().get(pk=paradigm_id)
        out = {
            'paradigm': p,
            'language': p.language,
            'source': p.source,
            'pronoun_rows': add_pronoun_table(p.pronoun_set.prefetch_related("entries", "pronountype").all()),
            'relationship_table': PronounRelationshipTable(p.relationship_set.select_related().all())
        }
        return render(request, 'pronouns/detail.html', out)
    except Paradigm.DoesNotExist:
        raise Http404 # fail. Doesn't exist so pop out a 404
        

@login_required()
def add(request):
    paradigm_form = ParadigmForm(request.POST or None)
    if paradigm_form.is_valid():
        p = paradigm_form.save(commit=False)
        p.editor = request.user
        p.save()
        return redirect('pronouns:edit', p.id)
    
    return render_to_response('pronouns/add.html', {
        'paradigm_form': paradigm_form,
    }, context_instance=RequestContext(request))


@login_required()
def edit(request, paradigm_id):
    p = get_object_or_404(Paradigm, pk=paradigm_id)
    
    
    PronounFormSet = create_pronoun_formset(Paradigm)
    pronoun_form = PronounFormSet(request.POST or None, instance=p)
    
    if pronoun_form.is_valid():
        instances = pronoun_form.save(commit=False)
        for obj in instances:
            obj.editor = request.user
            obj.save()
        return redirect('pronouns:detail', p.id)
        
    pronoun_form = add_pronoun_ordering(pronoun_form)
    
    #import IPython; IPython.embed()
    
    # the initial view and the error view
    return render_to_response('pronouns/edit.html', {
        'paradigm': p,
        'pronouns': pronoun_form,
    }, context_instance=RequestContext(request))



@login_required()
def edit_relationships(request, paradigm_id):
    p = get_object_or_404(Paradigm, pk=paradigm_id)
    relationship_form = RelationshipFormSet(request.POST or None, instance=p)
    # Yuck - filter querysets -> must be a better way to do this!
    q = Pronoun.objects.all().filter(paradigm=p).annotate(entry_count=Count('entries')).exclude(entry_count=0)
    for f in relationship_form.forms:
        f.fields['pronoun1'].queryset = q
        f.fields['pronoun2'].queryset = q
    
    if relationship_form.is_valid():
        instances = relationship_form.save(commit=False)
        for obj in instances:
            obj.editor = request.user
            obj.save()
        return redirect('pronouns:detail', p.id)
    
    return render_to_response('pronouns/edit_relationships.html', {
        'paradigm': p,
        'language': p.language,
        'source': p.source,
        'pronoun_rows': add_pronoun_table(p.pronoun_set.all()),
        'relationships': relationship_form,
        'rule_form': RuleForm(),
        'applied_rules': p.rule_set.all(),
    }, context_instance=RequestContext(request))


@login_required()
def process_rule(request, paradigm_id):
    p = get_object_or_404(Paradigm, pk=paradigm_id)
    # do we have do_identicals? 
    if 'process_identicals' in request.POST:
        # 1. process form
        members = find_identicals(p)
        
        # 2. implement rule
        if len(members) > 0:
            # 3. save rule to rule table.
            rule = Rule.objects.create(
                paradigm = p,
                rule="Identical Entries set to Total Syncretism",
                editor=request.user
            )
            for m1, m2 in members:
                # Ignore anything we've already set
                if not Relationship.objects.has_relationship_between(m1[0], m1[1], m2[0], m2[1]):
                    rel = Relationship.objects.create(
                        paradigm = p, 
                        pronoun1_id=m1[0], pronoun2_id=m2[0], 
                        entry1_id=m1[1], entry2_id=m2[1],
                        relationship='TS',
                        editor=request.user
                    )
                    rule.relationships.add(rel)
        
        return redirect('pronouns:edit_relationships', p.id)
        
    elif 'process_rule' in request.POST:
        # 1. process form
        rule_form = RuleForm(request.POST or None)
        if rule_form.is_valid():
            # 2. implement rule
            try:
                rule = extract_rule(ruleform.clean())
            except ValueError:
                # form is broken - go away.
                return redirect('pronouns:edit_relationships', p.id)
                
            # members = process_rule(rule, p.pronoun_set.all())
            
            # 3. save rule to rule table.
            # rule = Rule.objects.create(
            #     paradigm = p,
            #     rule="Identical Entries set to Total Syncretism",
            #     editor=request.user
            # )
            # for p1, p2 in members:
            #     # Ignore anything we've already set
            #     if Relationship.objects.has_relationship_between(p1, p2) == False:
            #         rel = Relationship.objects.create(
            #             paradigm = p, pronoun1=p1, pronoun2=p2, relationship='TS',
            #             editor=request.user
            #         )
            #         rule.relationships.add(rel)
        
        # Note: Invalid forms are IGNORED
        return redirect('pronouns:edit_relationships', p.id)
    else:
        return redirect('pronouns:detail', p.id)
        
    