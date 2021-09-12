#
# This file is only a routing to the view implementation
#
from django.http import HttpResponse
from app.classes.metier import posteMetier
# from app.tools.jsonPlus import JsonPlus
from django.template import loader


# views to update
def view_my_poste(request, poste_id):
    p = posteMetier.PosteMeteor(poste_id)
    print("in view poste")

    # poste_data = {'function': 'last_obs', 'poste_id': p.id, 'meteor': p.meteor, 'owner': p.owner}
    template = loader.get_template('app/poste.html')
    context = {
        'poste_data': p,
    }
    return HttpResponse(template.render(context, request))
