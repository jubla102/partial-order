from django.conf import settings
from django.http import HttpResponse
from django.template import loader


def groups(request):
    template = loader.get_template('partial_order/groups.html')
    return HttpResponse(template.render({'log_name': settings.EVENT_LOG_NAME}, request))


def combinations(request):
    template = loader.get_template('partial_order/combinations.html')
    return HttpResponse(template.render({'log_name': settings.EVENT_LOG_NAME}, request))


def delays(request):
    template = loader.get_template('partial_order/delays.html')
    return HttpResponse(template.render({'log_name': settings.EVENT_LOG_NAME}, request))
