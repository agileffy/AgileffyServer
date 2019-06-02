import requests

url = 'http://127.0.0.1:5000/register'
d = {'username': 'rebel',
     'password': '123456',
     'email': 'cylnb@cylnb.com'}

r = requests.post(url, data=d)
print(r.text)
