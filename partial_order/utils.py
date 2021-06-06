import json


def get_form_data(request, key):
    return json.loads(request.POST.dict()[key])
