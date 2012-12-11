from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Subgroup

def show(request, group_id=None):
    if group_id:
        root = Subgroup.objects.get(pk=group_id)
        nodes = root.get_children()
    else:
        root = Subgroup
        nodes = Subgroup.objects.all()
    return render_to_response("classification/index.html",
                          {'nodes': nodes, 'root': root, 'subgroup': root},
                          context_instance=RequestContext(request))
