import requests

url = 'http://108.61.183.99/api/register'
d = '{"username":"rebel","password":"123456","email" : "cylnb@cylnb.com"}'.encode()

print(d)

r = requests.post(url, data=d)
print(r.text)
