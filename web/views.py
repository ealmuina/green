from basicauth.decorators import basic_auth_required
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from web.models import Node, Firmware


def index(request):
    return render(request, 'index.html')


@basic_auth_required
def firmware(request, node_type):
    current_version = request.META.get('HTTP_X_ESP8266_VERSION')
    try:
        new_firmware = Firmware.objects.filter(
            node_type=node_type,
            version__gt=current_version
        ).order_by('version').last()
        if new_firmware:
            return FileResponse(
                open(new_firmware.file.path, 'rb')
            )
        return HttpResponse(status=304)
    except:
        return HttpResponseBadRequest()


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
