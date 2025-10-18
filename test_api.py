import requests

url = "http://localhost/v1/video"
data = {
    "url": "CYlon2tvywA"
}
response = requests.get(url, json=data)
print("Status code:", response.status_code)
print("Response body:", response.text)

url = "http://localhost/v2/video"
data = {
    "url": "CYlon2tvywA"
}
response = requests.get(url, json=data)
print("Status code:", response.status_code)
print("Response body:", response.text)
