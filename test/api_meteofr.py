import requests
import csv
# unique application id : you can find this in the curl's command to generate jwt token 
APPLICATION_ID = 'eUFwQ0EwYmY4OG1nTW5GeXRyYUlkemN0ZW5FYTp0QUJodDNuNUtWdmFZUXZMMDZRNGxFZEhYRFVh'

# url to obtain acces token
TOKEN_URL = "https://portail-api.meteofrance.fr/token"


class Client(object):

    def __init__(self):
        self.session = requests.Session()

    def request(self, method, url, **kwargs):
        # First request will always need to obtain a token first
        if 'Authorization' not in self.session.headers:
            self.obtain_token()

        # Optimistically attempt to dispatch reqest
        response = self.session.request(method, url, **kwargs)
        if self.token_has_expired(response):
            # We got an 'Access token expired' response => refresh token
            self.obtain_token()
            # Re-dispatch the request that previously failed
            response = self.session.request(method, url, **kwargs)

        return response

    def token_has_expired(self, response):
        status = response.status_code
        content_type = response.headers['Content-Type']
        repJson = response.text
        if status == 401 and 'application/json' in content_type:
            repJson = response.text
            if 'Invalid JWT token' in repJson['description']:
                return True
        return False

    def obtain_token(self):
        # Obtain new token
        data = {'grant_type': 'client_credentials'}
        headers = {'Authorization': 'Basic ' + APPLICATION_ID}
        access_token_response = requests.post(TOKEN_URL, data=data, verify=False, allow_redirects=False, headers=headers)
        token = access_token_response.json()['access_token']
        # Update session with fresh token
        self.session.headers.update({'Authorization': 'Bearer %s' % token})


def main():
    client = Client()
    # Issue a series of API requests an example. For use this test, you must first subscribe to the arome api with your application
    client.session.headers.update({'Accept': 'application/json'})

    response = client.request('GET', 'https://public-api.meteofrance.fr/public/DPPaquetObs/v1/paquet/horaire?id-departement=974&format=json', verify=False)
    for a_json in response.json():
        print(a_json['geo_id_insee'] + ' - ' + a_json['reference_time'] + ' - ' + a_json['insert_time'] + " - " + a_json['validity_time'])


main()
