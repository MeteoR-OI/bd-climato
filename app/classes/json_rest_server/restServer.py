from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.urls import path
from app.classes.repository.posteMeteor import PosteMeteor
from app.tools.myTools import getDirNameInSettings
import uuid
import os

# restServer.py


API_KEY = 'your_api_key'

@csrf_exempt
@require_POST
def upload_file(request):
    try:
        json_dir = getDirNameInSettings("JSON_AUTOLOAD")
        
        meteor = request.POST.get('meteor', None)
        file_name = request.POST.get('file_name', None)
        if meteor is None or file_name is None:
            return JsonResponse({'error': 'Missing parameters'}, status=400)
        
        cur_poste = PosteMeteor(meteor)
        if cur_poste is None:
            return JsonResponse({'error': 'Invalid meteor'}, status=400)

        if meteor not in file_name:
            return JsonResponse({'error': 'Invalid file name'}, status=400)   

        # Check if the API key is provided in the request headers
        if 'X-API-Key' not in request.headers or request.headers['X-API-Key'] != cur_poste.data.api_key:
            return JsonResponse({'error': 'Invalid Credentials'}, status=401)

        # Check if the file parameter exists in the request
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        file = request.FILES['file']

        # Generate a random unique file name
        file_name = os.path.join(json_dir, str(uuid.uuid4()) + '.tmp_json')

        # Save the file locally with the generated file name
        with open(file_name, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        os.rename(file_name, file_name.replace('.tmp_json', '.json'))

        return JsonResponse({'message': 'File uploaded successfully'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
