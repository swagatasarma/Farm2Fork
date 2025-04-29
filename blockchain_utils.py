
def append_block(data, filename='blockchain.json'):
    import hashlib, json, os, time
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            chain = json.load(f)
    else:
        chain = []

    prev_hash = chain[-1]['hash'] if chain else '0'
    block = {
        'index': len(chain) + 1,
        'timestamp': time.time(),
        'data': data,
        'previous_hash': prev_hash
    }
    block_string = json.dumps(block, sort_keys=True).encode()
    block['hash'] = hashlib.sha256(block_string).hexdigest()
    chain.append(block)
    with open(filename, 'w') as f:
        json.dump(chain, f, indent=4)
