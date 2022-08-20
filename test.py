import json
import requests
import random

import string
letters = string.ascii_lowercase

url = "http://35.196.111.228:8080/api/v1/dags/product_search/dagRuns"

payload = json.dumps({
                        "dag_run_id": ''.join(random.choice(letters) for i in range(10))
                })

headers = {
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive',
'Authorization': 'Basic YWlyZmxvdzphaXJmbG93',
'Content-Type': 'application/json',
'Cookie': 'session=fa4019dc-3e32-4785-babe-f1881bcdcbd2.0MZlc2KPl0AqtG4de855trFvA9w'
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)