import requests

url = "http://localhost:3000/v1/video"
data = {
    "url": "CYlon2tvywA"
}
response = requests.get(url, json=data)
print("Status code:", response.status_code)
print("Response body:", response.text)
