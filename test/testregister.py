import requests

url = 'http://127.0.0.1:5000/api/register'
d = '{"username":"rebel","password":"123456","email" : "cylnb@cylnb.com"}'.encode()

print(d)

r = requests.post(url, data=d)
print(r.text)
