import time
import json
import rsa

key = []


def get_key(fp):
    global key
    puk = fp + 'PublicKey'
    prk = fp + 'PrivateKey'
    with open(puk, 'r') as file:
        key.append(rsa.PublicKey.load_pkcs1(file.read().encode(), 'PEM'))
    with open(prk, 'r') as file:
        key.append(rsa.PrivateKey.load_pkcs1(file.read().encode(), 'PEM'))


def generate_transaction(user, weight, group, sender, recipient, number):
    global key
    transaction = {"additional": {"number": number, "time": time.time(), "weight": weight, "group": group},
                   "user": {"public_key": key[0], "address": user["address"], "post_code": user["post_code"]},
                   "content": {'sender': sender, "recipient": recipient}}
    return transaction


def sign_transaction(transaction):
    global key
    signature = rsa.sign(message=str(transaction).encode(), priv_key=key[1], hash_method='SHA-256')
    return signature


def verify(transaction, signature):
    global key
    return rsa.verify(message=str(transaction).encode(), signature=signature, pub_key=key[0])


def write_transaction(transaction, signature, fp):
    number = transaction["additional"]["number"]
    fp_transaction = fp + 'transaction' + str(number) + '.json'
    fp_signature = fp + 'signatue' + str(number) + '.dat'
    transaction['user']['public_key'] = [transaction['user']['public_key']['n'], transaction['user']['public_key']['e']]
    with open(fp_transaction, 'w', encoding='UTF8') as file:
        json.dump(transaction, file, indent=4)
    with open(fp_signature, 'wb') as file:
        file.write(signature)


# get_key('')
# for i in range(1, 6):
#     print(f'-----------------------\nGenerate transaction {i}')
#     tmp = (generate_transaction({"address": 'address', "post_code": 123456}, 5, 5, {'1': 1}, {'2': 2}, i))
#     print(f'transaction = {tmp}')
#     signature = sing_transaction(tmp)
#     print(f'signature = {signature}')
#     print(verify(tmp, signature))
#     write_transaction(tmp, signature, 'transactions//')
