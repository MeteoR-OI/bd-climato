import requests

def send_file():

    url = 'http://localhost:8000/app/sendjson?meteor=MTG320&filename=obs.MTG320.2023-11-01T01-00.json'
    file_path = './data/json_not_in_git/obs.MTG320.2023-11-01T01-00.json'
    api_key = 'mon api key 007'

    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': file}, headers={'X-API-Key': api_key})

    if response.status_code == 200:
        print('File sent successfully.')
    else:
        print('Failed to send file.')

send_file()
