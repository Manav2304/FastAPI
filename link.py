import requests

url = "https://sandbox.cashfree.com/pg/links"

headers = {
    "accept": "application/json",
    "x-api-version": "2022-09-01",
    "content-type": "application/json"
}

response = requests.post(url, headers=headers)

print(response.text)