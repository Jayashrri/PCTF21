from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os.path import dirname, realpath
import random

class Challenge :

    def __init__(self, key, iv, trolls) :
        self.key = bytes.fromhex(key)
        self.iv = bytes.fromhex(iv)
        self.trolls = trolls
        self.N = AES.block_size
        self.flag_file = dirname(realpath(__file__)) + '/flag.txt'
        self.engine = AES.new(self.key, AES.MODE_CBC, self.iv)

    def create_cipher(self) :
        with open(self.flag_file, 'rb') as f :
            flag = pad(f.read().strip(), self.N) #pctf{cut_743_BS_@nd_g1mm3_743_f1@g}
        self.ct = AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(flag)
        print(self.ct.hex())

    def decrypt(self, encrypted) :
        return self.engine.decrypt(encrypted).hex()

    def troll_player(self) :
        print(f"\n  This might help you : {random.choice(self.trolls)}")

    def interact(self) :
        blocks = [self.ct[i:i+self.N] for i in range(self.N, len(self.ct), self.N)]
        while True :
            cipher = input("\n  Ciphertext (hex) : ")
            try :
                cipher = bytes.fromhex(cipher)
            except :
                break
            if cipher == self.ct[:self.N] :
                IV = input("\n  IV (hex) : ")
                try :
                    IV = bytes.fromhex(IV)
                except :
                    break
                if IV == self.iv :
                    print(f"\n  Decrypted : {self.decrypt(cipher)}")
                else :
                    break
            elif not self.ct.find(cipher) == -1 :
                self.troll_player()
            else :
                print(f"\n  Decrypted : {self.decrypt(cipher)}")

    def __call__(self) :
        self.create_cipher()
        self.interact()
        return
        
def main() :
    key = "daeae618228c1b6e4be24c795dbf9b473dad4e89ee9711be7cb9b4993bce239d"
    iv = "a7e3c780cebe32f7c7e20eb615a6fcdc"
    trolls = ["https://youtu.be/Sagg08DrO5U",
            "https://youtu.be/oDvD9rOGUSs",
            "https://youtu.be/6iFbuIpe68k",
            "https://youtu.be/hIputTTexwA",
            "https://youtu.be/Qcp2W1-SFt4?t=14"]
    challenge = Challenge(key, iv, trolls)
    return challenge()

if __name__ == '__main__' :
    main()
