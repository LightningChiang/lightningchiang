import sys
import pandas as pd
import json
import re
import os
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256


raw = input("please set the password of data:\n")

path = os.path.abspath('.')
#sheetPath = path + '/CONTRUCT DATABASE.xlsm'
#print(sheetPath)
sheetPath = sys.argv[1]
# Load data
df = pd.read_excel(open(sheetPath, 'rb'), sheet_name="Database")
# Data Per processing
df = df.drop(columns=['Relevant Primers'])  # Drop this column for now
df = df.fillna('__')

def plainTextCleaner(text):
    text = re.sub(r'\s|\d', '', text)
    return text.upper()

df['DNA Sequence'] = df['DNA Sequence'].map(lambda x : plainTextCleaner(x))
df['Protein Seqeuence'] = df['Protein Seqeuence'].map(lambda x : plainTextCleaner(x))

dataSheet = df.to_json(orient="records")



hash_object = SHA256.new(raw.encode())

data = dataSheet.encode()
key = hash_object.digest().hex()[0:16].encode()
iv = 'a8d9672272f606b9'.encode()

cipher1 = AES.new(key, AES.MODE_CBC, iv)
ct = cipher1.encrypt(pad(data, 16))

'''cipher2 = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher2.decrypt(ct), 16)
assert(data == pt)'''
with open('../js/data/data.js', 'w') as fp:
    fp.writelines(["var values_FSLAB = '"])
    fp.writelines(ct.hex())
    fp.writelines(["'"])