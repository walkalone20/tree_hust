from sympy import *
from numpy import *
import hashlib
from random import *

# P = 955648524556446329387195293279494785773433536025987992578106057041523464431
# G = 29

# 传入消息，输出签名包（域，生成元，公钥，密文哈希）


def Signature(Text):
   HashText = hashlib.sha224(Text.encode('utf-8')).hexdigest()
   P = randprime(1, pow(2, 100))
   G = primitive_root(P)
   Data = int(HashText, base = 16) % P
   X = randint(1, P - 1)
   Y = pow(G, X, P)
   K = randprime(1, P - 1)
   S1 = pow(G, K, P)
   S2 = pow(K, totient(P - 1) - 1, P - 1) * (Data - X * S1) % (P - 1)
   return P, G, Y, Data, S1, S2

# 校验，输入签名包即可


def Check(Sig):
   P = Sig[0]
   G = Sig[1]
   Y = Sig[2]
   HashData = Sig[3]
   S1 = Sig[4]
   S2 = Sig[5]
   V1 = pow(G, HashData, P)
   V2 = pow(Y, S1, P) * pow(S1, S2, P) % P
   print(V1, V2)
   return V1 == V2
