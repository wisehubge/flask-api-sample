import requests
BASE_URL = "http://127.0.0.1:5000/services"

resp = requests.get(BASE_URL)
print(resp.json())
