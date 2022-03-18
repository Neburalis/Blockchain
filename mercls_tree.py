import hashlib as hl
import json
import rsa
from glob import glob


def mercles_tree(hashs: list[str]) -> str:
    def balancing(hashs: list[str])  -> list[str]:
        if len(hashs) % 2 == 0:
            return hashs

        hashs.append(hashs[-1])
        return hashs

    tmp_hashs = []
    if len(hashs) > 1:
        balance_hashs = balancing(hashs)
        for i in range(0, len(balance_hashs), 2):
            j = (i + 1)
            el1, el2 = hashs[i], hashs[j]
            sum = el1 + el2
            tmp_hashs.append(hl.sha256(sum.encode()).hexdigest())
        return mercles_tree(tmp_hashs)
    return hashs[0]


def verify(transaction, signature):
    key = transaction['user']['public_key']
    return rsa.verify(message=str(transaction).encode(), signature=signature, pub_key=key)


def read_transactions(fp):  # Считываем цепочку уже созданных транзакций
    fp_transaction = fp + 'transaction' + '*' + '.json'
    fp_signature = fp + 'signatue' + '*' + '.dat'
    files_transactions = glob(fp_transaction)
    files_signatures = glob(fp_signature)
    if len(files_signatures) == len(files_transactions):
        pass
    else:
        raise Exception('Not all transactions were signed')

    transactions = []
    for i, file_name_transction in enumerate(files_transactions):
        file_name_signatures = files_signatures[i]
        with open(file_name_transction, 'r', encoding='UTF8') as file:
            transactions.append([json.load(file)])
            transactions[-1][0]['user']['public_key'] = rsa.PublicKey(
                transactions[-1][0]['user']['public_key'][0],
                transactions[-1][0]['user']['public_key'][1]
            )
        with open(file_name_signatures, 'rb') as bytes_code:
            transactions[-1].append(bytes_code.read())
    return transactions


# transactions = read_transactions('transactions//')
# for i, transaction in enumerate(transactions):
#     number = transaction[0]['additional']['number']
#     print(f"--------------------------\nChecking {number}th transaction's signature")
#     print(f'transaction = {transaction[0]}')
#     print(f'signature = {transaction[1]}')
#     verify(transaction=transaction[0], signature=transaction[1])
#     transaction[0]['signature'] = transaction[1]
#     transactions[i] = transaction[0]
# del transaction
#
# hashs = []
# for i, transaction in enumerate(transactions):
#     # print(type(transaction))
#     hashs.append(hl.sha256(str(transaction).encode()).hexdigest())
#
# print(hashs)
# print(mercles_tree(hashs))
