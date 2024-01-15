created by marijn franco klappe

bits is used to save encrypted data by key and can only be decrypted widt the richt key
but you dont have to add a key to your data if you dont want to.

--------------------------------------------------------------
example: widt key

from bits import storeData,readData

data = ["my data",{'a':1,'b':1.1},False]

storeData(data,"save.bm","key")

storedData = readData(data,"save.bm","key")
print(storedData)

--------------------------------------------------------------
example: without key

from bits import storeData,readData

data = ["my data",{'a':1,'b':1.1},False]

storeData(data,"save.bm")

storedData = readData(data,"save.bm")
print(storedData)
