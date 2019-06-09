import requests

url = 'http://127.0.0.1:5000/api/login'
d = '{"username":"rebel1", "password":"123456"}'.encode()

r = requests.post(url, data=d)
print(r.text)
