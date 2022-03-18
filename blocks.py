import hashlib as hl
import json
complexity = 2

block = {
    'nonce ': 0
}
hash_block = hl.sha256(str(block).encode()).hexdigest()
# print(hash)
while hash_block[-1:-3:-1] != '0'*complexity:
    block['nonce '] += 1
    hash_block = hl.sha256(str(block).encode()).hexdigest()

print(block['nonce '])
print(hash_block)

print(json.dumps(block, sort_keys=True, indent=4))
