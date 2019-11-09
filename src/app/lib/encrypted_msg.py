import os
import sys
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import json
import base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "lib"))
import msg

def send(sock, text, timeout=60):
    # Send request for public key.
    ret = msg.send(sock, json.dumps({
        "TYPE": "REQUEST_PUB_KEY"
    }), timeout=timeout)
    if not ret:
        return False
    
    # Get the target's public key.
    ret = msg.recv(sock, timeout=timeout)
    if not ret:
        return False
    json_msg = ''
    try:
        json_msg = json.loads(ret)
    except json.decoder.JSONDecodeError:
        return False
    try:
        if json_msg["TYPE"] != "RESPONSE_PUB_KEY":
            return False
    except KeyError:
        return False
    pubkey = None
    try:
        pubkey = RSA.importKey(base64.b64decode(json_msg["BODY"].encode()))
    except (ValueError, KeyError):
        return False

    # Encrypt the message using the target's public key.
    cipher = pubkey.encrypt(text.encode(), 32)

    # Send the cipher to the target.
    ret = msg.send(sock, json.dumps({
        "TYPE": "CIPHER",
        "BODY": base64.b64encode(cipher[0]).decode('UTF8')
    }), timeout=timeout)
    if not ret:
        return False
    return True


def recv(sock, key, timeout=60):
    # Get a public key request.
    ret = msg.recv(sock, timeout=timeout)
    if not ret:
        return None
    json_msg = ''
    try:
        json_msg = json.loads(ret)
    except json.decoder.JSONDecodeError:
        return None
    try:
        if json_msg["TYPE"] != "REQUEST_PUB_KEY":
            return None
    except KeyError:
        return None

    # Send own public key to the requester.
    ret = msg.send(sock, json.dumps({
        "TYPE": "RESPONSE_PUB_KEY",
        "BODY": base64.b64encode(key.publickey().exportKey()).decode('UTF8')
    }), timeout=timeout)
    if not ret:
        return None

    # Get the requester's cipher.
    ret = msg.recv(sock, timeout=timeout)
    if not ret:
        return None
    json_msg = ''
    try:
        json_msg = json.loads(ret)
    except json.decoder.JSONDecodeError:
        return None
    try:
        if json_msg["TYPE"] != "CIPHER":
            return None
    except KeyError:
        return None

    # Decipher using own private key that matches own public key, and return the decrypted text.
    try:
        return key.decrypt(base64.b64decode(json_msg["BODY"].encode())).decode()
    except KeyError:
        return None
    

def generate_key():
    random_generator = Random.new().read
    return RSA.generate(1024, random_generator)
