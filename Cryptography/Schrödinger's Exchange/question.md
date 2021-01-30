The future is here! Banks have begun the use of quantum computing technology. (at a basic level for now)
You are an I.T. guy at one such bank. Your job is to setup a secure communication channel between two mainframes located in different cities.

The use of BB84 protocol has been approved for this purpose. (Photons are sent on a quantum channel whereas sharing of basis and rest of the encrypted communication happens on a classical channel)

Once the key distribution is complete you will receive an encrypted flag. Get the original flag and hopefully you might even get a promotion!

## Server side:

```python
from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
import random

def verify_photons(photons):
    valid_len = 1024
    valid_photons = [[1, 0], [0, 1], [0.707, -0.707], [0.707, 0.707]]
    
    try:
        assert isinstance(photons, list)
        assert len(photons) == valid_len
        for i in range(valid_len):
            assert photons[i] in valid_photons
        return True
    except:
        return False

def verify_basis(basis):
    valid_len = 1024
    valid_base = ['+', 'x']

    try:
        assert isinstance(basis, list)
        assert len(basis) == valid_len
        for i in range(valid_len):
            assert basis[i] in valid_base
        return True
    except:
        return False

def verify_bits(bits):
    valid_len = 1024
    valid_bits = ['0', '1', '\x00']

    try:
        assert isinstance(bits, list)
        assert len(bits) == valid_len
        for i in range(valid_len):
            assert bits[i] in valid_bits
        return True
    except:
        return False

def verify_key_size(key_size):
    try:
        assert isinstance(key_size, int)
        assert key_size > 0
        return True
    except:
        return False

def polarize_photons(bits, basis):
    return []

def measure_photons(photons, basis):
    return ''

def calculate_key(bits, basis_1, basis_2):
    return b''

def BB84(photons, basis):
    my_basis = [random.choice('+x') for _ in len(basis)]
    calculated_bits = measure_photons(photons, my_basis)
    key = calculate_key(calculated_bits, basis, my_basis)
    key = key[:256]
    return my_basis, key

app = Flask(__name__)

@app.route('/flag', methods=['GET'])
def serve():
    try:
        if request.method == 'GET':
            params = request.get_json()
            
            try:
                photons = params['photons']
                basis = params['basis']
            except:
                return 'invalid parameters', 422

            if not verify_photons(photons) or not verify_basis(basis):
                return 'invalid parameters', 422
            
            my_basis, key = BB84(photons, basis)

            flag = open('flag.txt', 'rb').read()
            flag = AES.new(key, AES.MODE_ECB).encrypt(pad(flag, AES.block_size))
            flag = b64encode(flag).decode()

            response = jsonify({'basis': my_basis, 'flag': flag})
            return response, 200
        else:
            return 'method not implemented', 501
    except:
        return 'an unexpected error occured', 500

@app.route('/polarize', methods=['GET'])
def polarize():
    try:
        if request.method == 'GET':
            params = request.get_json()
            
            try:
                bits = params['bits']
                basis = params['basis']
            except:
                return 'invalid parameters', 422

            if not verify_bits(bits) or not verify_basis(basis):
                return 'invalid parameters', 422
            
            photons = polarize_photons(bits, basis)
            response = jsonify({'photons': photons})
            return response, 200
        else:
            return 'method not implemented', 501
    except:
        return 'an unexpected error occured', 500

@app.route('/measure', methods=['GET'])
def polarize():
    try:
        if request.method == 'GET':
            params = request.get_json()
            
            try:
                photons = params['photons']
                basis = params['basis']
            except:
                return 'invalid parameters', 422

            if not verify_photons(photons) or not verify_basis(basis):
                return 'invalid parameters', 422
            
            bits = measure_photons(photons, basis)
            response = jsonify({'bits': bits})
            return response, 200
        else:
            return 'method not implemented', 501
    except:
        return 'an unexpected error occured', 500

@app.route('/sharedkey', methods=['GET'])
def polarize():
    try:
        if request.method == 'GET':
            params = request.get_json()
            
            try:
                bits = params['bits']
                basis_1 = params['basis_1']
                basis_2 = params['basis_2']
            except:
                return 'invalid parameters', 422

            if not verify_bits(bits) or not verify_basis(basis_1) or not verify_basis(basis_2):
                return 'invalid parameters', 422
            
            key = calculate_key(bits, basis_1, basis_2)
            key = b64encode(key).decode()
            response = jsonify({'key': key})
            return response, 200
        else:
            return 'method not implemented', 501
    except:
        return 'an unexpected error occured', 500

if __name__ == '__main__':
    app.run()
```
