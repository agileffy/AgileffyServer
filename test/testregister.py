import requests

url = 'https://agileffy.info/api/register'
d = '{"username":"rebel","password":"123456","email" : "cylnb@cylnb.com"}'.encode()

print(d)

r = requests.post(url, data=d)
print(r.text)
