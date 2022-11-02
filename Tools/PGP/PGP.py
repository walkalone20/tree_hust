import AES
import RSA
import ElGamal
import random
import hashlib
import string

# 传入明文，按照(RSA(Key), AES(Key, Text), Signature(Hash)) 进行传输
def Encode(Text):
    Key = random.sample(string.ascii_letters + string.digits, 16)
    RSAKey = RSA.Encode(Key)
    Cipher = AES.Encoder(Text, Key)
    Signature = ElGamal.Signature(Text)
    return RSAKey, Cipher, Signature
    
def Decode(Pkt):
    RSAKey = Pkt[0]
    CipherText, oldlen = Pkt[1]
    Signature = Pkt[2]
    Key = RSA.Decode(RSAKey)
    Text = AES.Decoder(CipherText, Key, oldlen)
    # 哈希完整性检验
    NoDamage = int(hashlib.sha224(Text.encode('utf-8')).hexdigest(), base = 16) % Signature[0] == Signature[3]
    Verification = ElGamal.Check(Signature)
    return NoDamage, Verification, Text

# 示例
# Text = "qefdlkm24ltml24kmghl lkjhkasjeghfqaijfnli sfgvi vlaiejf"
# Pkt = Encode(Text)
# Text = Decode(Pkt)
