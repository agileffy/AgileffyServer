import requests

url = 'https://agileffy.info/api/login'
d = '{"username":"rebel1", "password":"123456"}'.encode()

r = requests.post(url, data=d)
print(r.text)
