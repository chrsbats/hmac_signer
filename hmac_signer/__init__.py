
import base64
import datetime
import hmac
from hashlib import sha1, md5
from requests.auth import AuthBase
from urlparse import parse_qs, urlsplit, urlunsplit
from urllib import urlencode
from email.Utils import formatdate
import dateutil.parser
from dateutil.tz import tzutc

import os


class HmacAuth(AuthBase):
    #API_KEY_QUERY_PARAM = 'apiKey'
    #API_HTTP_HEADER = ''
    SIGNATURE_HTTP_HEADER = 'Authorization'
    TIMESTAMP_HTTP_HEADER = 'Date'
    CONTENT_MD5_HEADER = "Content-MD5"
    VERSION_HTTP_HEADER = 'X-Auth-Version'
    SIGNATURE_DELIM = ','
    VERSION_1 = '1'

    def __init__(self,api_key=None,secret_key=None,timestamp_expiry=15):
        if not secret_key:
            raise TypeError("HMAC signing requires secret key")
        if api_key:
            self.api_key = str(api_key)
        else:
            self.api_key = None

        self.secret_key = str(secret_key)
        self.timestamp_expiry = timestamp_expiry

    def __call__(self, request):
        self._encode(request)
        
        return request

    def validate_flask_request(self,request):
        #TODO - Find flask equivalents
        body = request.get_data()
        if body:
            h = md5()
            h.update(str(body))
            h = h.digest()
            content_md5 = base64.b64encode(h).strip()
        content_type = str(request.headers.get('Content-Type',''))
        path = str(request.path)
        
        timestamp = str(request.headers[HmacAuth.TIMESTAMP_HTTP_HEADER])
        request_date = dateutil.parser.parse(timestamp)
        if datetime.datetime.now(tzutc()) - request_date < datetime.timedelta(minutes=self.timestamp_expiry):
            signature = self._sign(content_type, content_md5, path, timestamp)
            
            if request.headers[HmacAuth.SIGNATURE_HTTP_HEADER] == signature:
                return True
        return False

    def _encode(self, request):
        timestamp = self._get_current_timestamp()
        #self._add_version(request, HmacAuth.VERSION_1)
        self._add_timestamp(request, timestamp)
        self._add_content_md5(request, timestamp)
        
        #Must be done last - relies on the above
        self._add_signature(request, timestamp)
        

    def _get_current_timestamp(self):
        # Return current UTC time in ISO8601 format
        return formatdate()[:-5] + "GMT"

    
    def _add_timestamp(self, request, timestamp):
        request.headers[HmacAuth.TIMESTAMP_HTTP_HEADER] = timestamp

    def _add_content_md5(self, request, timestamp):
        if request.body:
            h = md5()
            h.update(request.body)
            h = h.digest()
            content_md5 = base64.b64encode(h).strip()
            request.headers[HmacAuth.CONTENT_MD5_HEADER] = content_md5
    
    def _add_version(self, request, version):
        request.headers[HmacAuth.VERSION_HTTP_HEADER] = version

    def _add_signature(self, request, timestamp):
        content_type = request.headers.get('Content-Type','')
        if request.body:
            content_md5 = request.headers[HmacAuth.CONTENT_MD5_HEADER]
        else:
            content_md5 = ''
        
        path = request.path_url
        
        signature = self._sign(content_type, content_md5, path, timestamp)
        request.headers[HmacAuth.SIGNATURE_HTTP_HEADER] = signature
        

    def _sign(self, content_type, content_md5, path, timestamp):
        # Build the message to sign

        message = bytearray(content_type) +                 \
                  bytearray(HmacAuth.SIGNATURE_DELIM) +     \
                  bytearray(content_md5) +                  \
                  bytearray(HmacAuth.SIGNATURE_DELIM) +     \
                  bytearray(path) +                         \
                  bytearray(HmacAuth.SIGNATURE_DELIM) +     \
                  bytearray(timestamp) 
                  
        # Create the signature
        digest = hmac.new(self.secret_key, message, sha1).digest()
        hmac_key = base64.b64encode(digest).strip()
        
        if self.api_key:
            return 'APIAuth ' + self.api_key + ':' + hmac_key
        else:
            return 'HMACAuth ' + hmac_key

def extract_api_key_from_flask_request(request):
    signature = request.headers[HmacAuth.SIGNATURE_HTTP_HEADER]
    if signature[:len('APIAuth ')] == 'APIAuth ':
        api_key = signature[len('APIAuth '):].split(':')[0]
        return api_key
    else:
        return None

def validate_flask_request(request,api_key=None,secret_key=None):
    #TODO - Fix this
    #Resign the request and check md5 matches content and the time of request is reasonable
    hmac = HmacAuth(api_key,secret_key)
    if hmac.validate_flask_request(request):
        return True
    return False
    