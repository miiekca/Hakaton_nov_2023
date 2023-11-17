import requests

url = "http://127.0.0.1:5000/hello"
data = {
    'name': 'John Doe',
    'age': 25
}

response = requests.post(url, json=data)

if response.status_code == 200:
    response_data = response.json()
    print(response_data)
else:
    print('Error:', response.status_code)

