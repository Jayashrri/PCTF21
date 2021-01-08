import random
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD


def GetPrimePair(bits=512):
    assert bits % 4 == 0

    p = getPrime(bits)
    q = getPrime(p+1, 2*p)

    return p, q


def generateKeys(nbits=1024):
    # nbits >= 1024 is recommended
    assert nbits % 4 == 0

    p = getPrime(512)
    q = getPrime(512)
    print("p = ")
    print(p)
    print("q = ")
    print(q)
    n = p*q
    phi = (p-1)*(q-1)

    good_d = False
    while not good_d:
        d = random.getrandbits(nbits//4)
        if (GCD(d, phi) == 1 and 36*pow(d, 4) < n):
            good_d = True

    e = inverse(d, phi)
    return e, n, d


e, n, d = generateKeys()
print("Public Key:")
print("e =")
print(e)
print("n =")
print(n)
print("Private Key:")
print("d =")
print(d)

p = 8126710856977669175419803458963817583963497266002177971426858750160093358788927258748062323833496645235650818765821007695076380044949680444889928784242587
q = 7304404432383575683608074874266776909119066547276589789780177002818876924194875374511238034737544812430861594244780679937796921259588981073493227258326641
e = 42763678068180324405985997857607497539263825207033675501965144853459364969587631157436606656082580650751101436817434900913679067314399520863421704013436729351034913742760716705282563374206639055605158668559469880540281064505601591110019881820615738843482236923178043129161609880033052395105391662297159608321
n = 59360782804407413522416571298493084219826254310575168671477307019289337183670261656559575071599338323054099125705237395481583063086234984501812872504880145760206916712867995019899595257616472196133917100862216739339368067344798908301525968760957408691426720338431793399138239903765505639822387020850228860267
d = 25121366845647976495852084403409456983078186427266033862693622774546436434721
t = (p-1)*(q-1)
# hex_encrypt = 202b8536cf2f7c7d36744bec3b492f428c2a0e0c3c0bc01dfd8cdff3122b1d8c2d5cb64368c6e878b4d7fa08149992ff94c2907be991c702b4dfbea2fb2d1d3ca6f66c3765a0fc679fcc6d5cdc4c71271286d2270bbb0f76582865d13e042e0b51cbc773720bf3a2f05314d6f539da1ac627526c6def249d64455c79c246eb49

print("---------------------------------------")
flag = b"pctf{0nly_1f_y0u_kn0w_1t_4ll}"
encrypt_hex = long_to_bytes((pow(bytes_to_long(flag), e, n))).hex()
print("HEX ENCRYPT= ")
print(encrypt_hex)
print("---------------------------------------")
encrypt_long = pow(bytes_to_long(flag), e, n)
print("LONG ENCRYPT= ")
print(encrypt_long)
print("---------------------------------------")
decrypt_hex = pow(bytes_to_long(bytes.fromhex(encrypt_hex)), d, n)
decrypt_long = long_to_bytes(pow(encrypt_long, d, n))
print("LONG DECRYPT= ")
print(decrypt_long)
print("---------------------------------------")
print("HEX DECRYPT= ")
print(long_to_bytes(decrypt_hex))
