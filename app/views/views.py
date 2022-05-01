#
# This file is only a routing to the view implementation
#
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# views well routed
@csrf_exempt
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
