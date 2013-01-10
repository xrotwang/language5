from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import DetailView, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from website.apps.entry.models import Task

from django_tables2 import SingleTableView

from website.apps.entry.tables import TaskIndexTable

class TaskIndex(SingleTableView):
    """Task Index"""
    model = Task
    template_name = 'entry/index.html'
    table_class = TaskIndexTable
    table_pagination = {"per_page": 50}
    order_by_field = 'name'
    
    queryset = Task.objects.all().filter(content__done=False).annotate(task_count=Count('content'))
    
    # ensure logged in
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskIndex, self).dispatch(*args, **kwargs)

    
# Data Entry View
class TaskDetail(DetailView):
    """Data Entry"""
    model = Task
    template_name = 'entry/detail.html'
    #form_class = 
    
    # ensure logged in
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DataEntry, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(DataEntry, self).get_context_data(**kwargs)
        context['task'] = Task.objects.get(pk=kwargs['object'].task_id)
        # get form...
        _temp = __import__("website.apps.entry.forms", globals(), locals(), [str(context['task'].form)])
        #context['form'] = getattr(_temp, context['task'].form)(initial={'editor': self.request.user})
        context['form'] = getattr(_temp, context['task'].form)()
        # load data...?
        return context
    