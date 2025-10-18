import requests

url = "http://localhost:3000/v1/video"
data = {
    "url": " https://example.com/video"
}
response = requests.post(url, json=data)
print("Status code:", response.status_code)
print("Response body:", response.text)
