from django.http import HttpResponse
import json

from main_web.models import Sub_Information_classification
from main_web.models import Information_classification

def get_sub_class(request, obj_id):
    print (obj_id)
    in_class = Information_classification.objects.get(id = obj_id)
    print (in_class)
    sub_class = Sub_Information_classification.objects.filter(information_classification = in_class.id)
    print (sub_class)
    result = []
    for i in sub_class:
        result.append({'id': i.id,
                        'name': i.name})
        print(i.id, i.name)
    json_result = json.dumps(result)

    return HttpResponse(json_result, content_type="application/json")