from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from os.path import dirname, realpath
import compress_pickle
import random
import numpy
import base64
import json


class QKD:

    def __init__(self, params):
        self.bits = params['photons']
        self.basis = params['basis']
        self.key_size = params['key_size']
        self.eavesdrop = params['eavesdrop']

    def convert_basis(self):
        self.basis = ''.join('{:08b}'.format(n) for n in self.basis)

    def generate_basis(self):
        self.new_basis = ''.join(random.choice('01') for i in range(len(self.basis)))

    def convert_bits_dishonest(self):
        self.new_bits = ''.join(random.choice('01') for i in range(len(self.basis)))

    def convert_bits_honest(self):
        self.new_bits = ''
        for photon, basis in zip(self.bits, self.new_basis):
            if basis == '0':  # diagonal basis
                photon = photon * complex(-0.707, 0.707)
            probab_0 = round(photon.real**2, 1)
            probab_1 = round(photon.imag**2, 1)
            self.new_bits += str(numpy.random.choice(numpy.arange(0, 2), p=[probab_0, probab_1]))

    def shared_key(self):
        self.shared_key = ''
        for i in range(len(self.new_basis)):
            if self.new_basis[i] == self.basis[i]:
                self.shared_key += self.new_bits[i]
        self.shared_key = self.shared_key[:self.key_size]

    def params_to_base64(self):
        self.new_bits = base64.b64encode(bytes([int(self.new_bits[i:i+8], 2) for i in range(0, len(self.new_bits), 8)])).decode()
        self.new_basis = base64.b64encode(bytes([int(self.new_basis[i:i+8], 2) for i in range(0, len(self.new_basis), 8)])).decode()
        self.shared_key = base64.b64encode(bytes([int(self.shared_key[i:i+8], 2) for i in range(0, len(self.shared_key), 8)])).decode()

    def __call__(self):
        self.convert_basis()
        self.generate_basis()
        if self.eavesdrop:
            self.convert_bits_dishonest()
        else:
            self.convert_bits_honest()
        self.shared_key()
        self.params_to_base64()
        return {'basis': self.new_basis, 'key': self.shared_key}


class Challenge:

    def __init__(self, quantum_params, challenge_params):
        qkd = QKD(quantum_params)
        self.quantum = qkd()
        self.script = challenge_params['script']
        self.passwd = challenge_params['passwd']
        self.keyword = challenge_params['keyword']
        self.url = challenge_params['url']
        self.switch_cmd = challenge_params['switch_cmd']
        self.encryption_key = challenge_params['encryption_key']
        self.cipher = AES.new(base64.b64decode(self.quantum['key'].encode()), AES.MODE_ECB)

    def quantum_broadcast(self):
        print(f"\nMY BASIS: {self.quantum['basis']}")

    def passwd_prompt(self):
        msg = base64.b64encode(self.cipher.encrypt(pad(self.script['passwd_prompt'].encode(), AES.block_size))).decode()
        print(f"\n{msg}")

    def verify_passwd(self, recv_passwd):
        global switch_cmd_used
        if recv_passwd == self.switch_cmd:
            if not switch_cmd_used:
                switch_cmd_used = not switch_cmd_used
                return -1
            return -2
        try:
            recv_passwd = base64.b64decode(recv_passwd.encode())
            recv_passwd = AES.new(base64.b64decode(self.quantum['key'].encode()), AES.MODE_ECB).decrypt(recv_passwd)
            recv_passwd = unpad(recv_passwd, AES.block_size).decode()
            assert recv_passwd == self.passwd
            return 1
        except:
            return 2

    def classical_channel(self):
        print(f"\n{self.script['classical_channel']['switch']}")
        print(f"\n{self.script['classical_channel']['reason']}")

        if not input("\n").lower().find(self.keyword) == -1:
            print(f"\n{self.script['keyword_resp']['correct']}")
            print(f"\n{self.encryption_key}")
            return True
        else:
            print(f"\n{self.script['keyword_resp']['incorrect']}")
            return False

    def __call__(self):
        self.quantum_broadcast()
        self.passwd_prompt()

        response = self.verify_passwd(input("\n"))
        if response == -2:
            print(f"\n{self.script['switch_cmd_overuse']}")
            return False
        if not response == -1:
            if response == 1:
                msg = f"{self.script['password_resp']['correct']}: {self.url}"
            elif response == 2:
                msg = self.script['password_resp']['incorrect']
            msg = base64.b64encode(self.cipher.encrypt(pad(msg.encode(), AES.block_size))).decode()
            print(f"\n{msg}")
        else:
            return self.classical_channel()
        return False


eavesdrop = True
switch_cmd_used = False


def main():
    file = dirname(realpath(__file__)) + '/config.json'
    with open(file) as config:
        params = json.load(config)

    global switch_cmd_used
    if switch_cmd_used:
        print(f"\n{params['script']['quantum_channel']['switch']}")
    else:
        print(f"\n{params['script']['quantum_channel']['start']}")

    photons = input("\nYOUR PHOTONS: ")
    basis = input("\nYOUR BASIS: ")
    # photons = 'QlpoOTFBWSZTWTTlawcAGor/7d7AAAQAQQAggIAQAlpnz0BBBA4AhAGAQAEAQABQBD4YOCArYAMaNGgGTIaMRpoGmAkyqqBkDAgAwDRNBKfqVVQGgYCGmIwmBBjRo0AyZDRiNNA0wClSpkA00NNAGjEaDJwiV2YRDPSqskFUtNVVWKVVr2t3jux+JAcykJmRDNErCKnHhEaVIYiVnRDiqlZAAy6NGjK9cBK04VIbduz32Y6uvs9/Z5GMAB9ero6XdNoqJxIis2WKRZJ0RTRYUqEoklUcMU5YRSZRptZIakpRcTpKiJKQUJXNCLRJISYgZXVSRSNWVGCVJgqiTOMttYYhbZsCGWNbotrZmDlHY2bJpnGXMasLITWbnOImba1hqVlxGIzdliO2sotCKJInLQwzcbWmlDFiqKBcNMrSIkkJKwjayMwrViSFIQtoZqnMTomgQWpy5rErCMDREJTUlEiI5yUUuqhpkhImGmaG1E4hLaLKTiktDMUJETphkURosTFLYSmkUWKgaYnVA6gohTRRmVmQm1uy1u024jqQxRILLhBm5eZ7eHAAAA7wAADw4buCQHBIDekBrqlb0hV9e7qqv+5xOVHRRQdzonOOclOOUBIUcEJySjhQKAEjiiBBJTkiTgckUQ5OcJKcHDoA6XBwUEJxIQRInSCRB3CjikpSOhHLkIRBERwHB0ATnEcpOjhJIdE5HRCHdd3d3/i7kinChIGnK1g4'
    # basis = 'CORTO/W7ot9L+5pTDpuV3yU9T30aWs12oi4pl/LivVeQ1GtaoAjKvzAq494Y7HVGnj5GxB5QVfrMCZzii1p4FYxUAkqJ6nkha0NJQj0D8S3V4+EIJxe6Bo3vC4uaIOfAYCFWPomaFFeY5clLNOJxlvryTj2MWY+UVEq2Ddwa94s='

    try:
        photons = base64.b64decode(photons.encode())
        photons = compress_pickle.loads(photons, compression='bz2')
        assert isinstance(photons, list)
        assert len(photons) == 1024
        valid_photons = [complex(0, 1), complex(1, 0), complex(0.707, -0.707), complex(0.707, 0.707)]
        for photon in photons:
            assert isinstance(photon, complex)
            assert photon in valid_photons
        basis = base64.b64decode(basis.encode())
        assert len(basis) == 128
    except:
        print(f"\n{params['script']['parse_error']}")
        return

    global eavesdrop
    key_size = params['key_size']
    quantum_params = {'photons': photons, 'basis': basis, 'key_size': key_size, 'eavesdrop': eavesdrop}

    script = params['script']
    passwd = params['passwd']
    keyword = params['keyword']
    encryption_key = params['encryption_key']
    switch_cmd = params['switch_cmd']
    url = params['url']
    challenge_params = {'script': script, 'keyword': keyword, 'passwd': passwd, 'switch_cmd': switch_cmd, 'url': url, 'encryption_key': encryption_key}

    challenge = Challenge(quantum_params, challenge_params)
    if challenge():
        eavesdrop = not eavesdrop
        return main()
    return


if __name__ == '__main__':
    main()
