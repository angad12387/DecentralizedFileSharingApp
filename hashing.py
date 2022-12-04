import hashlib

testing=("peer1").encode()
print(hashlib.sha384(testing).hexdigest())
testing=("peer2").encode()
print(hashlib.sha384(testing).hexdigest())
testing=("peer3").encode()
print(hashlib.sha384(testing).hexdigest())