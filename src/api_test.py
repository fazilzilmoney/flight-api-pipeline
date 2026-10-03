import requests

url = 'https://opensky-network.org/api/states/all'

response = requests.get(url)

print(response.status_code)

data = response.json()

print(data.keys())
