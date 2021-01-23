from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import compress_pickle
import random
import numpy
import base64


def generate_basis():
    my_basis = [random.choice('01') for i in range(1024)]
    return my_basis


def photons_to_bits(photons, my_basis):
    my_bits = ''
    for photon, basis in zip(photons, my_basis):
        if basis == '0':
            photon *= complex(0.707, -0.707)
        probab_0 = round(photon.real**2, 1)
        probab_1 = round(photon.imag**2, 1)
        my_bits += str(numpy.random.choice(numpy.arange(0, 2), p=[probab_0, probab_1]))
    return my_bits


def shared_key(basis, my_basis, my_bits, key_size):
    shared_key = ''
    for i in range(len(my_basis)):
        if basis[i] == my_basis[i]:
            shared_key += my_bits[i]
    shared_key = shared_key[:key_size]
    shared_key = bytes([int(shared_key[i:i+8], 2) for i in range(0, len(shared_key), 8)])
    return shared_key


def encrypt(message, key):
    message = pad(message.encode(), AES.block_size)
    ciphertext = AES.new(key, AES.MODE_ECB).encrypt(message)
    ciphertext = base64.b64encode(ciphertext).decode()
    return ciphertext


def decrypt(message, key):
    message = base64.b64decode(message.encode())
    message = AES.new(key, AES.MODE_ECB).decrypt(message)
    message = unpad(message, AES.block_size).decode()
    return message


def main():
    print("\n--- START OF QUANTUM CHANNEL (QUANTUM KEY DISTRIBUTION INITIATED) ---")
    photons = input("\nYOUR PHOTONS: ")
    basis = input("\nYOUR BASIS: ")  # 1: rectilinear, 0: diagonal

    try:
        photons = base64.b64decode(photons.encode())
        photons = compress_pickle.loads(photons, compression='bz2')
        assert isinstance(photons, list)
        assert len(bits) == 1024
        valid_photons = [complex(0, 1), complex(1, 0), complex(-0.707, 0.707), complex(0.707, 0.707)]
        for photon in photons:
            assert isinstance(photon, complex)
            assert photon in valid_photons
        basis = base64.b64decode(basis.encode())
        assert len(basis) == 128
    except:
        print("\nIncorrect PHOTONS/BASIS format.")
        return

    my_basis = generate_basis()
    my_bits = photons_to_bits(photons, my_basis)
    key = shared_key(basis, my_basis, my_bits, 256)

    my_basis = bytes([int(my_basis[i:i+8], 2) for i in range(0, len(my_basis), 8)])
    my_basis = base64.b64encode(my_basis).decode()

    print(f"\nMY BASIS: {my_basis}")
    print(f"\n{encrypt('<message>', key)}")

    response = input("\n")
    if response == "SWITCH":
        print("\n--- SWITCHED TO CLASSICAL CHANNEL (QUANTUM KEY DISTRIBUTION TERMINATED) ---")
        print("\nWhy did you ditch the quantum channel? What happened?")
        if input("\n") == "<valid>":
            pass  # proceed further
        else:
            print("\nI do not understand what you are saying.")
    else:
        try:
            response = decrypt(response, key)
            assert response == "<valid>"
            print(f"\n{encrypt('<message>', key)}")
        except:
            print(f"\n{encrypt('<message>', key)}")
    return


if __name__ == '__main__':
    main()
