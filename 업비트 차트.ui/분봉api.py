import requests

url = "https://api.upbit.com/v1/candles/minutes/1"

querystring = {"market":"KRW-BTC","count":"1"}

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)