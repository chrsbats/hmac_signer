from __future__ import absolute_import
import requests
from hmac_signer import HmacAuth
import json

data = 'some data'
url = "http://localhost:5000"

response = requests.post(url, data=data, auth=HmacAuth('apikey','secretkey'))
print "200",response.status_code
assert response.status_code == 200


response = requests.post(url, data=data, auth=HmacAuth('apikey','anotherkey'))
print "401",response.status_code
assert response.status_code == 401

