from django.http import HttpResponse
from django.template import loader


def test(request):
    template = loader.get_template('partial_order/partial_order_groups.html')
    return HttpResponse(template.render({}, request))
