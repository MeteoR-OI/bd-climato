from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.urls import path
from app.classes.repository.posteMeteor import PosteMeteor
from app.tools.myTools import getDirNameInSettings
import uuid
import os
import app.tools.myTools as t
import app.tools.dbTools as dbt

# restServer.py
# pg_pool is required...


@csrf_exempt
@require_POST
def upload_file(request):
    try:
        pg_cxion = pg_cur = None

        json_dir = getDirNameInSettings("JSON_AUTOLOAD")
        pg_cxion = dbt.getPGConnexion()
         
        meteor_requested = request.POST.get('meteor', None)
        file_name = request.POST.get('filename', None)
        if meteor_requested is None or file_name is None:
            return JsonResponse({'error': 'Missing parameters'}, status=400)
        
        if str(meteor_requested).__contains__("'") or str(meteor_requested).__contains__(";"):
            return JsonResponse({'error': 'Invalid meteor'}, status=400)

        my_select = "select meteor, api_key from postes where meteor = '" + meteor_requested + "'"
        print ("my_select: ", my_select)

        try:
            pg_cur = pg_cxion.cursor()

        except Exception as e:
            t.logError("upload_file", "Invalid PG connexion, trying to reconnect")
            pg_cxion = dbt.getPGConnexion()
            pg_cur = pg_cxion.cursor()

        cur_row = pg_cur.execute(my_select).fetchone()

        if cur_row is None:
            return JsonResponse({'error': 'Invalid meteor'}, status=400)

        meteor = cur_row[0]
        api_key = cur_row[1]

        while cur_row is not None:
            cur_row.fetchone()

        print ("meteor: ", meteor, ", api_key: ", api_key)

        if meteor is None or api_key is None:
            return JsonResponse({'error': 'Invalid meteor'}, status=400)

        if meteor not in file_name:
            return JsonResponse({'error': 'Invalid file name'}, status=400)

        # Check if the API key is provided in the request headers
        if 'X-API-Key' not in request.headers or request.headers['X-API-Key'] != api_key:
            return JsonResponse({'error': 'Invalid Credentials'}, status=401)

        # Check if the file parameter exists in the request
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        file = request.FILES['file']

        dir_name = os.path.join(json_dir, meteor)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

        # Generate a random unique file name
        file_name = os.path.join(json_dir, meteor, file_name)
        if os.path.isfile(file_name):
            return JsonResponse({'error': 'File already exists'}, status=400)
        file_name = file_name.replace('.json', '.tmp_json')

        # Save the file locally with the generated file name
        with open(file_name, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        os.rename(file_name, file_name.replace('.tmp_json', '.json'))

        return JsonResponse({'message': 'File uploaded successfully'}, status=200)

    except Exception as e:
        t.logException(e, {'meteor': meteor, 'file_name': file_name})
        return JsonResponse({'error': '{0}'.format(e)}, status=500)

    finally:
        if pg_cur is not None:
            pg_cur.close()
        if pg_cxion is not None:
            pg_cxion.close()
