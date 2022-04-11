import requests
import json

with open("post_data.json") as f:
    post_data = json.load(f)
res = requests.post('http://127.0.0.1:5000/data/json', json=post_data, params={"write": True})
print(res.ok)
