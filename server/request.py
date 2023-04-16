import requests
import hashlib
url="http://localhost:5000/login"


rsp=requests.post(url, json={"email":"Chakib@gmail.com", "password":"chakib1234"})

print(rsp.text)