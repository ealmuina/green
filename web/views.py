from django.shortcuts import render
from django.views.generic import ListView, DetailView

from web.models import Node


def index(request):
    return render(request, 'index.html')


class NodeListView(ListView):
    model = Node
    template_name = 'node_list.html'


class NodeDetailView(DetailView):
    model = Node
    template_name = 'node_detail.html'
    context_object_name = 'node'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add records
        context['records'] = list(map(
            lambda record: [record[0].timestamp() * 1000, record[1]],
            self.object.records.values_list('date', 'moisture')
        ))

        return context
