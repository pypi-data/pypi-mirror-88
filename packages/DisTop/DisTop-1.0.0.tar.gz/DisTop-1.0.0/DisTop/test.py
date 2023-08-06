import requests

r = requests.get("https://bumpboard.xyz/api/bumped")
r = r.json()
print(r)

