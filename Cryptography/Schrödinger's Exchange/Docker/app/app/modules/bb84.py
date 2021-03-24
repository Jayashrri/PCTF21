from random import choice
from numpy import random, arange

class BB84:

    def initialize(self, params):
        self.photons = params['photons']
        self.basis = params['basis']
        self.key_size = params['key_size']

    def generate_basis(self) -> list:
        return [choice('+x') for i in range(len(self.basis))]

    def measure_photons(self, photons, basis) -> list:
        bits = ''
        for photon, base in zip(photons, basis):
            if base == 'x':
                photon = photon * complex(-0.707, 0.707)
            probab_0 = round(photon.real**2, 1)
            probab_1 = round(photon.imag**2, 1)
            if not probab_0 == probab_1:
                bits += str(random.choice(arange(0, 2), p=[probab_0, probab_1]))
            else:
                bits += '\x00'
        return list(bits)

    def shared_key(self, bits, basis_1, basis_2, key_size) -> bytes:
        key = ''
        for i in range(len(basis_1)):
            if basis_1[i] == basis_2[i]:
                if not bits[i] == '\x00':
                    key += bits[i]
        key = key[:key_size]
        key += '1'*(key_size - len(key))
        key = bytes([int(key[i:i+8], 2) for i in range(0, len(key), 8)])
        return key

    def polarize_photons(self, bits, basis) -> list:
        photons = []
        for pair in zip(bits, basis):
            if pair == ('1', '+'):
                photons.append(complex(0, 1))
            elif pair == ('1', 'x'):
                photons.append(complex(0.707, -0.707))
            elif pair == ('0', '+'):
                photons.append(complex(1, 0))
            else:
                photons.append(complex(0.707, 0.707))
        return photons

    def simulate_eavesdropper(self) -> list:
        basis = self.generate_basis()
        bits = self.measure_photons(self.photons, basis)
        self.photons = self.polarize_photons(bits, basis)
        return basis

    def distribute(self, simulate=False) -> (list, list, bytes):
        basis = self.generate_basis()
        if simulate:
            e_basis = self.simulate_eavesdropper()
        bits = self.measure_photons(self.photons, basis)
        key = self.shared_key(bits, self.basis, basis, self.key_size)
        if simulate:
            return basis, e_basis, key
        return basis, [], key
