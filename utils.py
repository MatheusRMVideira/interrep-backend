import hashlib
import re
import requests
import jwt

from config import ALLOWED_EXTENSIONS, JWT_KEY


def encrypt(password):
	hash_object = hashlib.sha1(str.encode(password))
	hex_dig = hash_object.hexdigest()
	hash_object2 = hashlib.sha1(str.encode(hex_dig)+str.encode(password))
	hex_dig2 = hash_object2.hexdigest()
	return hex_dig2

def isValidEmail(email):
	match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
	if match:
		return True
	return False

class HttpRequest:
    def get(url):
        result = requests.get(url)
        if result.status_code >= 400:
            return False
        return result.json()
    def post(url, data):
        result = requests.post(url, data)
        if result.status_code >= 400:
            return False
        return result.json()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def CreateToken(payload):
    token = jwt.encode(payload, JWT_KEY, algorithm='HS256')
    #str_token = token.decode("utf-8")
    return token

def DecodeToken(auth):
    token = auth.split(" ", 2)[1]
    return jwt.decode(token, JWT_KEY, algorithms=['HS256'])

