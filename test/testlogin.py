import requests

url = 'http://127.0.0.1:5000/login'
d = {'username':'rebel1', 'password':'123456'}

r = requests.post(url, data=d)
print(r.text)
