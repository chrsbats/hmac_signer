=====
HMAC Signer
=====

Sign your HTTIP requests with requests and validate it in your flask server.

This code is presently functional but needs more tests.

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

Getting HMAC signing to work with both flask and requests was a bit more painful than expected.  Leaving this code here for others. 

Authors
=======

Created by [Christopher Bates](https://github.com/chrsbats)

