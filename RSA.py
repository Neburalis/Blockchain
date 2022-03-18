from rsa import *

pubkey, privkey = newkeys(1024)

print(privkey)
print(pubkey)

pubkey_pem = pubkey.save_pkcs1(format='PEM')
privkey_pem = privkey.save_pkcs1(format='PEM')

print(pubkey_pem, privkey_pem)

with open('PublicKey.pem', 'w+') as f:
    f.write(pubkey_pem.decode('utf8'))
with open('PrivateKey.pem', 'w+') as f:
    f.write(privkey_pem.decode('utf8'))
