from bitstring import BitArray

def save_bits_to_file(filePath, bits):
    with open(filePath, 'wb') as file:
        bit_array = BitArray(uint=bits[0], length=8)
        for i in range(1, len(bits)):
            bit_array.append(BitArray(uint=bits[i], length=8))
        bit_array.tofile(file)

def read_bits_from_file(filePath):
    with open(filePath, 'rb') as file:
        bit_array = BitArray(bytes=file.read())
    result = [bit_array[i:i+8].uint for i in range(0, len(bit_array), 8)]

    return result

def convertInt(number):
    bitLenght = 0
    found = False
    while found == False:
        Min = 2**bitLenght-1
        bitLenght+=8
        Max = 2**bitLenght
        if number >= Min and number < Max:
            found = True

    binary_string = bin(number)[2:]
    binary_string=binary_string.zfill(bitLenght)
    arr = []
    for i in range(0,round(bitLenght/8)):
        Min = i*8
        Max = (i+1)*8
        arr.append(int(binary_string[Min:Max], 2))
    return arr

def convertChar(char):
    return int(bin(ord(char))[2:], 2)

def checkType(data,bits,has=True):
    if type(data) is int:
        if data < 0:
            if(has):
                bits.append(12)
            data = abs(data)
            sData = convertInt(data)
            bits.append(len(sData))
            bits+=sData
        else:
            if(has):
                bits.append(1)
            sData = convertInt(data)
            bits.append(len(sData))
            bits+=sData

    elif type(data) is float:
        if int(data) == data:
            checkType(int(data),bits)
        else:
            if data < 0:
                bits.append(13)
                data = abs(data)
            else:
                bits.append(2)
            float_str = str(data)
            integer_part, decimal_part = map(int, float_str.split('.'))
            sData = convertInt(integer_part)
            bits.append(len(sData))
            bits+=sData
            sData = convertInt(decimal_part)
            bits.append(len(sData))
            bits+=sData
    elif type(data) is str:
        if len(data) == 1:
            if(has):
                bits.append(3)
            bits.append(convertChar(data))
        else:
            bits.append(4)
            checkType(len(data),bits,False)
            for i in range(len(data)):
                checkType(data[i],bits,False)
    elif type(data) is bool:
        if data:
            bits.append(0)
        else:
            bits.append(11)
    else:
        convertData(data,bits)

def convertData(data,bits=[]):
    if type(data) is list:
        bits.append(7)
        for i in data:
            checkType(i,bits)
        bits.append(8)
    elif type(data) is dict:
        bits.append(5)
        for k,v in data.items():
            checkType(k,bits)
            checkType(v,bits)
        bits.append(6)
    else:
        checkType(data,bits)
    return bits

def convertBitInt(bits):
    bits.reverse()
    num = 0
    for i in range(len(bits)):
        num+=bits[i]*(256**i)

    return num

def findEnd(bits,endType):
    ignore = 0
    total = 1
    for i in range(len(bits)):
        if i < ignore: continue
        if bits[i] == 1:
            ignore = bits[i+1]+i+2
        elif bits[i] == 12:
            ignore = bits[i+1]+i+2
        elif bits[i] == 2:
            n = bits[i+1]+i+2
            ignore = bits[n]+1+n
        elif bits[i] == 13:
            n = bits[i+1]+i+2
            ignore = bits[n]+1+n
        elif bits[i] == 3:
            ignore = i+2
        elif bits[i] == endType[0]:
            total+=1
        elif bits[i] == endType[1]:
            total-=1
        if total == 0:
            return bits[:i]

def isEven(n):
    return n % 2 == 0

def convertbits(bits,data = [],deep = 0):
    ignore = 0
    key = None
    count = 0
    for i in range(len(bits)):
        if i < ignore: continue
        if type(data) == list:
            if bits[i] == 7:
                data.append([])
                newBits = findEnd(bits[i+1:],[7,8])
                ignore = i+len(newBits)+2
                convertbits(newBits,data[-1],deep=deep+1)
            elif bits[i] == 5:
                data.append({})
                newBits = findEnd(bits[i+1:],[5,6])
                ignore = i+len(newBits)+2
                convertbits(newBits,data[-1],deep=deep+1)
            elif bits[i] == 0:
                data.append(True)
            elif bits[i] == 11:
                data.append(False)
            elif bits[i] == 1:
                ignore = bits[i+1]+i+2
                newBits = bits[i+2:ignore]
                data.append(convertBitInt(newBits))
            elif bits[i] == 12:
                ignore = bits[i+1]+i+2
                newBits = bits[i+2:ignore]
                data.append(-convertBitInt(newBits))
            elif bits[i] == 3:
                ignore = i+2
                data.append(chr(bits[i+1]))
            elif bits[i] == 4:
                Intrange = bits[i+1]+i+2
                newBits = bits[i+2:Intrange]
                StringLenght = convertBitInt(newBits)
                ignore = Intrange+StringLenght
                s = ''
                for j in range(StringLenght):
                    s+=chr(bits[j+Intrange])
                data.append(s)
            elif bits[i] == 2:
                n = bits[i+1]+i+2
                ignore = bits[n]+1+n
                newBits = bits[i+2:n]
                intbit = convertBitInt(newBits)
                newBits = bits[n+1:ignore]
                dec = convertBitInt(newBits)
                data.append(float(f"{intbit}.{dec}"))
            elif bits[i] == 13:
                n = bits[i+1]+i+2
                ignore = bits[n]+1+n
                newBits = bits[i+2:n]
                intbit = convertBitInt(newBits)
                newBits = bits[n+1:ignore]
                dec = convertBitInt(newBits)
                data.append(float(f"{-intbit}.{dec}"))
        else:
            if bits[i] == 7:
                data[key] = []
                newBits = findEnd(bits[i+1:],[7,8])
                ignore = i+len(newBits)+2
                convertbits(newBits,data[key],deep=deep+1)
            elif bits[i] == 5:
                data[key] = {}
                newBits = findEnd(bits[i+1:],[5,6])
                ignore = i+len(newBits)+2
                convertbits(newBits,data[key],deep=deep+1)
            elif bits[i] == 0:
                count+=1
                if isEven(count):
                    data[key] = True
                else:
                    key = True
            elif bits[i] == 11:
                count+=1
                if isEven(count):
                    data[key] = False
                else:
                    key = False
            elif bits[i] == 1:
                count+=1
                ignore = bits[i+1]+i+2
                newBits = bits[i+2:ignore]
                if isEven(count):
                    data[key] = convertBitInt(newBits)
                else:
                    key = convertBitInt(newBits)
            elif bits[i] == 12:
                count+=1
                ignore = bits[i+1]+i+2
                newBits = bits[i+2:ignore]
                if isEven(count):
                    data[key] = -convertBitInt(newBits)
                else:
                    key = -convertBitInt(newBits)
            elif bits[i] == 3:
                count+=1
                ignore = i+2
                if isEven(count):
                    data[key] = chr(bits[i+1])
                else:
                    key = chr(bits[i+1])
            elif bits[i] == 4:
                count+=1
                Intrange = bits[i+1]+i+2
                newBits = bits[i+2:Intrange]
                StringLenght = convertBitInt(newBits)
                ignore = Intrange+StringLenght
                s = ''
                for j in range(StringLenght):
                    s+=chr(bits[j+Intrange])
                if isEven(count):
                    data[key] = s
                else:
                    key = s
            elif bits[i] == 2:
                count+=1
                n = bits[i+1]+i+2
                ignore = bits[n]+1+n
                newBits = bits[i+2:n]
                intbit = convertBitInt(newBits)
                newBits = bits[n+1:ignore]
                dec = convertBitInt(newBits)
                if isEven(count):
                    data[key] = float(f"{intbit}.{dec}")
                else:
                    key = float(f"{intbit}.{dec}")
            elif bits[i] == 13:
                count+=1
                n = bits[i+1]+i+2
                ignore = bits[n]+1+n
                newBits = bits[i+2:n]
                intbit = convertBitInt(newBits)
                newBits = bits[n+1:ignore]
                dec = convertBitInt(newBits)
                if isEven(count):
                    data[key] = float(f"{-intbit}.{dec}")
                else:
                    key = float(f"{-intbit}.{dec}")
    if deep == 0:
        return data[0]


print(convertbits(read_bits_from_file('save')))