=====
HMAC Signer
=====

Sign your HTTP requests with requests and validate it in your flask server.

This code is presently functional but needs more tests.

Requirements
============

python 2.7
Flask 0.10.1
python-dateutil 2.4.2
requests 2.7.0


Examples
========

First have some kind of datastore containing your apikey and secret key pairs

    secret_keys = {'apikey':'secretkey'}

Then set up your flask endpoint as follows

    from hmac_signer import extract_api_key_from_flask_request, validate_flask_request

    @app.route("/", methods=['POST'])
    def receive():
        apikey = extract_api_key_from_flask_request(request)
        result = validate_flask_request(request,apikey,secret_keys[apikey])
        
Result will be True if auth passes.

On the client side use requests like follows to interact with your REST based microservice

    from hmac_signer import HmacAuth

    data = 'some data'
    url = "http://localhost:5000"

    response = requests.post(url, data=data, auth=HmacAuth('apikey','secretkey'))


Motivation
==========

Getting HMAC signing to work with both flask and requests was a bit more painful than expected.  Leaving this code here for others.  This code is based on the one provided by python-hmac-auth but follows the same HMAC scheme as used by the ruby api-auth gem.

Authors
=======

Created by [Christopher Bates](https://github.com/chrsbats)

Forked from [bazaarvoice/python-hmac-auth](https://github.com/bazaarvoice/python-hmac-auth)
