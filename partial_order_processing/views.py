from django.conf import settings
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def partial_order_processing(request):
    template = loader.get_template('partial_order/partial_order_groups.html')
    return HttpResponse(template.render({'log_name': settings.EVENT_LOG_NAME}, request))
