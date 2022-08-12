import hashlib
import re
import requests

JWT_KEY = "14834c55af7e2ca2adda98495f6e64a2cc032cb7"
while(True):
    password = input()

    print("\n")
    hash_object = hashlib.sha1(str.encode(password))
    hex_dig = hash_object.hexdigest()
    hash_object2 = hashlib.sha1(str.encode(hex_dig)+str.encode(password))
    hex_dig2 = hash_object2.hexdigest()
    print(hex_dig2)
    print("\n")
