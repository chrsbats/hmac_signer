import os, sys
from flask import Flask, request
from hmac_signer import extract_api_key_from_flask_request, validate_flask_request



app = Flask(__name__)

app.secret_key = 'mysecretflaskkey'

keys = {'apikey':'secretkey', 'orgkey':'secretorgkey'}


@app.route("/", methods=['POST'])
def receive():
    apikey = extract_api_key_from_flask_request(request)
    if apikey:
        result = validate_flask_request(request,apikey,keys[apikey])
    else:
        result = validate_flask_request(request,secret_key=keys['orgkey'])

    if result:
        return '',200
    else:
        return '',401
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,use_reloader=False,debug=True)
