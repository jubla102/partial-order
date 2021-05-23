from django.http import HttpResponse
from django.template import loader


def test(request):
    template = loader.get_template('test.html')
    data = "partial order visualization"
    return HttpResponse(template.render({'data': data}, request))
