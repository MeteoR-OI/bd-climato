import requests
import csv

userName='meteo.oi'
password='meteo.oi'

#

def get_station_data(token):
    # url = 'https://public-api.meteofrance.fr/public/DPPaquetObs/v1/liste-stations'
    url = "https://public-api.meteofrance.fr/public/DPPaquetObs/v1/paquet/horaire?id-departement=974&format=json"
    # url = 'https://public-api.meteofrance.fr/public/DPPaquetObs/v1/paquet/infrahoraire-6m?id_station=97418110&format=json'
    headers = {
        'accept': '*/*',
        'apiKey': token
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return the CSV data as a string
    else:
        return ""


def get_token():
    return 'eyJ4NXQiOiJZV0kxTTJZNE1qWTNOemsyTkRZeU5XTTRPV014TXpjek1UVmhNbU14T1RSa09ETXlOVEE0Tnc9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJtZXRlb3Iub2lAY2FyYm9uLnN1cGVyIiwiYXBwbGljYXRpb24iOnsib3duZXIiOiJtZXRlb3Iub2kiLCJ0aWVyUXVvdGFUeXBlIjpudWxsLCJ0aWVyIjoiVW5saW1pdGVkIiwibmFtZSI6IkRlZmF1bHRBcHBsaWNhdGlvbiIsImlkIjo2NzMzLCJ1dWlkIjoiNWZlZjg3MzctZGQ1My00Njk2LWFiZjItODg3Zjc5ODE3OTE2In0sImlzcyI6Imh0dHBzOlwvXC9wb3J0YWlsLWFwaS5tZXRlb2ZyYW5jZS5mcjo0NDNcL29hdXRoMlwvdG9rZW4iLCJ0aWVySW5mbyI6eyI1MFBlck1pbiI6eyJ0aWVyUXVvdGFUeXBlIjoicmVxdWVzdENvdW50IiwiZ3JhcGhRTE1heENvbXBsZXhpdHkiOjAsImdyYXBoUUxNYXhEZXB0aCI6MCwic3RvcE9uUXVvdGFSZWFjaCI6dHJ1ZSwic3Bpa2VBcnJlc3RMaW1pdCI6MCwic3Bpa2VBcnJlc3RVbml0Ijoic2VjIn19LCJrZXl0eXBlIjoiUFJPRFVDVElPTiIsInN1YnNjcmliZWRBUElzIjpbeyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6IkRvbm5lZXNQdWJsaXF1ZXNQYXF1ZXRPYnNlcnZhdGlvbiIsImNvbnRleHQiOiJcL3B1YmxpY1wvRFBQYXF1ZXRPYnNcL3YxIiwicHVibGlzaGVyIjoiYmFzdGllbmciLCJ2ZXJzaW9uIjoidjEiLCJzdWJzY3JpcHRpb25UaWVyIjoiNTBQZXJNaW4ifSx7InN1YnNjcmliZXJUZW5hbnREb21haW4iOiJjYXJib24uc3VwZXIiLCJuYW1lIjoiRG9ubmVlc1B1YmxpcXVlc09ic2VydmF0aW9uIiwiY29udGV4dCI6IlwvcHVibGljXC9EUE9ic1wvdjEiLCJwdWJsaXNoZXIiOiJiYXN0aWVuZyIsInZlcnNpb24iOiJ2MSIsInN1YnNjcmlwdGlvblRpZXIiOiI1MFBlck1pbiJ9LHsic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJEb25uZWVzUHVibGlxdWVzQ2xpbWF0b2xvZ2llIiwiY29udGV4dCI6IlwvcHVibGljXC9EUENsaW1cL3YxIiwicHVibGlzaGVyIjoiYWRtaW5fbWYiLCJ2ZXJzaW9uIjoidjEiLCJzdWJzY3JpcHRpb25UaWVyIjoiNTBQZXJNaW4ifSx7InN1YnNjcmliZXJUZW5hbnREb21haW4iOiJjYXJib24uc3VwZXIiLCJuYW1lIjoiRG9ubmVlc1B1YmxpcXVlc1BhcXVldFJhZGFyIiwiY29udGV4dCI6IlwvcHVibGljXC9EUFBhcXVldFJhZGFyXC92MSIsInB1Ymxpc2hlciI6ImxvaWMubWFydGluIiwidmVyc2lvbiI6InYxIiwic3Vic2NyaXB0aW9uVGllciI6IjUwUGVyTWluIn0seyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6IkRvbm5lZXNQdWJsaXF1ZXNSYWRhciIsImNvbnRleHQiOiJcL3B1YmxpY1wvRFBSYWRhclwvdjEiLCJwdWJsaXNoZXIiOiJNRVRFTy5GUlwvbWFydGlubCIsInZlcnNpb24iOiJ2MSIsInN1YnNjcmlwdGlvblRpZXIiOiI1MFBlck1pbiJ9XSwiZXhwIjoxNzM2OTU2ODQzLCJ0b2tlbl90eXBlIjoiYXBpS2V5IiwiaWF0IjoxNzA1NDIwODQzLCJqdGkiOiI0NWJlYjM0OC1jNzcyLTRiM2QtYTU2Yy1jYjJhZWExMzE0YjYifQ==.fUCIZm_f2Zu-F3Gp9zNkETdVVcncaGSQlrDEILXiBEOp8EcuYrzG0WyQy8rMEoEqpCFaipbcKWu4LlbnlS7CY8VpXtZpHTufLWQxwQaQZSx87YLFs2mT6MhkbzKYcXqvzvHgqgFcIhya-K2cDbLd6eDGHJ3QKjQf8oWqlbrTWDlsrwq3ejLlbOYf8VPO7kqdJ1Y3H-dFwMiAyvd3rBhQ-Am8iCIkLdHOeUi1euosRBk1bDlT9mOzFFfTHjT2M4g4oW6j7MKwAgaCykssYnKVmXUzbFxupPCwC_uc5ByJj3IggM2bGdKspB-sM4n1iIDp4ZY_gSik3ArWS0TLPX-PCQ=='
    # headers = {
    #     'accept': 'application/json, text/plain, */*',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    #     'Authorization': 'Bearer eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJtZXRlb3Iub2kiLCJhdXQiOiJBUFBMSUNBVElPTl9VU0VSIiwicm9sZSI6WyJJbnRlcm5hbFwvc3Vic2NyaWJlciIsIkludGVybmFsXC9ldmVyeW9uZSIsIkludGVybmFsXC9zZWxmc2lnbnVwIl0sImNpdmlsaXR5IjoibXIiLCJhZGRyZXNzIjp7ImNvdW50cnkiOiJGcmFuY2UiLCJhZGRyZXNzIjoiMjcgYmlzIFJ1ZSBQb3VsZGVuaXMiLCJwb3N0YWxfY29kZSI6IjU2MzcwIn0sImNpdHkiOiJMZSBUb3VyIER1IFBhcmMiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJwcm9BY2NvdW50Ijoib24iLCJnaXZlbl9uYW1lIjoiTmljb2xhcyIsImNsaWVudF9pZCI6InE4NkVmeGczQVdKUTJLSlEyNUVac0p3MWNmQWEiLCJhdWQiOiJxODZFZnhnM0FXSlEyS0pRMjVFWnNKdzFjZkFhIiwibmJmIjoxNzA1MDc2NzgzLCJhenAiOiJxODZFZnhnM0FXSlEyS0pRMjVFWnNKdzFjZkFhIiwic2NvcGUiOiJhcGltOnN1YnNjcmliZSBvcGVuaWQgcHJvZmlsZSIsImV4cCI6MTcwNTA4MDM4MywiaWF0IjoxNzA1MDc2NzgzLCJmYW1pbHlfbmFtZSI6IkN1dmlsbGllciIsImp0aSI6ImM5YWQ1YzUyLTAwZmUtNDJiNy04ZGJmLTM4MTQ4YmI1NTQ2MyIsImVtYWlsIjoibmljb2xhc0BjdXZpbGxpZXIubmV0IiwidXNlcm5hbWUiOiJtZXRlb3Iub2kifQ.VCZuAXd3Vr1kkin2LvlWghZf5KgwTD362Xdth4ImzvzMW6uWCP8y_LCE3Wniqj7R3j7TRv0lC6pBznDvFvOXZB8LhluBqjGk185IFnMqlgAUUSeIb7un6rYI6pnNNR4iDVumvGIqvl8ypIpxjSJaz4KMuNLGUAo-aZpz7ca3GTQ0tJ3P3g4VOLacBjxXCBAl3GHTpLfxErV6VsQLfBlAkSNgNpn9vbgIsmCEEvBqm7CRvi-1GJJz5osMiUq3wUonQkVrLzrjTQe5h5qXTOSxFAa6ZatTYFG3JguIyyPfbXJ7ZBKIM78oHeDqv1I0xLse-k4gog9sOB9tlfQ_dk7JsQ',
    #     'Content-Type': 'application/json',
    #     'Sec-Fetch-Mode': 'cors',
    #     'Sec-Fetch-Site': 'same-origin'
    # }
    # data = {
    #     "scopes": [],
    #     "validityTime": 3600
    # }
    # response = requests.post(url, params=data, headers=headers)

    # if response.status_code == 200:
    #     return response.json()['accessToken']  # Return the CSV data as a string
    # else:
    #     return None


token = get_token()
if token is None:
    print("Token is None")
    exit(1)
big_j = get_station_data(token)
print(str(big_j))

print('-------------------')
for j in big_j:
    print(j['geo_id_insee'] + ' - ' + j['reference_time'] + ' - ' + j['insert_time'] + " - " + j['validity_time'])
print('-------------------')
print(big_j[0])
# 

# stations = get_station_data(token).splitlines(token)  # Split the CSV data into lines
# reader = csv.reader(stations)  # Create a CSV reader

# hdr = True

# for row in reader:
#     if str(row).split(';')[0].startswith("['974") or hdr:
#         print(str(row).split(';'))  # Print each row of the CSV data
#     hdr = False
