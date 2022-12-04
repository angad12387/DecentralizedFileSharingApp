
"""
The two main methods are jwt_send() and jwt_receieve(), the others are helper functions
jwt_send()
    When given a json file for example: 
            {
            "Header": [
                {
                    "alg": "HS256",
                    "typ": "JWT"
                }
            ],
            "Payload": [
                {
                    "Pass": "1234567890",
                    "User": "John Doe"
                }
            ]
            }
    It will parse the Header and payload and create a string of the two dictionaries. 
    These are encoded in base64 and used to create a sha256 hash. 
    These are appended togther seperated by '.'
    Example: eydBbGcnOiAnSFMyNTYnLCAnVHlwZSc6ICdKV1QnfQ==.eydVc2VyJzogJ0pvaG4gRG9lJywgJ1Bhc3MnOiAnMTIzNDU2Nzg5MCd9.002db224960b4a40681cf73d094fd06087a12a18ad02fd9070a4de344aa4234a
    is created from:
    {'Alg': 'HS256', 'Type': 'JWT'}
    {'User': 'John Doe', 'Pass': '1234567890'}

jwt_receive():
    When given string JWT it will, verify the sha256 hash and parse the hash into two dictorionaries, header and payload

Example of how they can be used is seen in __init__()
"""

import base64
import hashlib
import json


def __init__():
    with open('JWT/jwtpass.json') as json_file:
        JWT_token = jwt_send(json_file)

    print(JWT_token)

    Header, Payload = jwt_receive(JWT_token)
    print(Header)
    print(Payload)


def jwt_send(fp):
    """Fuction which will return the completed JWT when given an appropriate json file"""
    jwtDict = json.load(fp)

    header, payload = _parseJson_(jwtDict)

    hash = _hash256_(_encode_(str(header)), _encode_(str(payload)))

    full_JWTstring = _createEncodedStr_(
        _encode_(str(header)), _encode_(str(payload)), hash)

    return full_JWTstring


def jwt_receive(input: str):
    """Evaluates hash value received vs expected and returns the parsed Header and payload dictionaries if hash values are consistent"""
    jwtList = input.split('.')

    if(not _checkHash_(jwtList[0], jwtList[1], jwtList[2])):
        print("Error: Hash values are inconsistent")
        return 0

    Header = eval(_decode_(jwtList[0]))
    Payload = eval(_decode_(jwtList[1]))

    return Header, Payload


def _parseJson_(Dict: dict):
    """Parses a json file into seperate dictonaries and returns them"""
    header = {}
    payload = {}

    for dictionary in Dict['Header']:
        header["Alg"] = dictionary['alg']
        header["Type"] = dictionary['typ']

    for dictionary in Dict['Payload']:
        payload["User"] = dictionary['User']
        payload["Pass"] = dictionary['Pass']

    return header, payload


def _createEncodedStr_(Hstr: str, PStr: str, hash: str) -> str:
    """Creates the full JWT token"""
    return Hstr + "." + PStr + "." + hash


def _bytesToString_(input: bytes):
    """Converts a series of bytes to a string"""
    if isinstance(input, str):
        return input
    return input.decode('ascii')


def _stringToBytes_(input: str):
    """Converts a string to a series of bytes"""
    if isinstance(input, bytes):
        return input
    return input.encode('ascii')


def _encode_(input: str) -> str:
    """Returns a string of the encoded string """
    return _bytesToString_(base64.urlsafe_b64encode(_stringToBytes_(input)))


def _decode_(input: str) -> str:
    """Decodes a base64 encoded string"""
    return _bytesToString_(base64.urlsafe_b64decode(_stringToBytes_(input)))


def _hash256_(head: str, pay: str) -> str:
    """Hashes the header and payload and returns a hexadecimal string"""
    hash = hashlib.sha256()
    hash.update(_stringToBytes_(head))
    hash.update(_stringToBytes_(pay))
    return hash.hexdigest()


def _checkHash_(input1, input2, hash) -> bool:
    """Evaluates expected vs calculated hash"""
    hashInput = _hash256_(input1, input2)
    return hashInput == hash


__init__()
