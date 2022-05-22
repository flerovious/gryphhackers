import json
import html
from urllib import response
import requests

response = requests.get('https://would-you-rather-api.abaanshanid.repl.co')
json_data = json.loads(response.text)
question = json_data['data']
print(question)