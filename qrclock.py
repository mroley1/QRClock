# pototyping

#target: QR Model 2, v.1 alphanumeric, ECC level H


import time

def main():
    alphanumeric_key = "0123456789ABCDEFGHIJKLMONPQRSTUVWXYZ $%*+-./:"
    generator_polynomials = {17: [43, 139, 206, 78, 43, 239, 123, 206, 214, 147, 24, 99, 150, 39, 243, 163, 136]}
    t = time.localtime()
    t_string = "{0:0>2}:{1:0>2}:{2:0>2}".format(int(t.tm_hour%12), t.tm_min, t.tm_sec)
    t_string = "12:34:56"
    print(t_string)

    CODEWORD_QUANTITY = 26

    bits = ""
    #mode
    bits += "0010"
    #charector count
    bits += " "
    tmp = f"{len(t_string):b}"
    bits += f"{tmp:0>9}"
    #paired charectors
    for i in range(0,len(t_string)-1,2):
        bits += " "
        a = alphanumeric_key.index(t_string[i])
        b = alphanumeric_key.index(t_string[i+1])
        a = a*10
        c = a+b
        tmp = f"{c:b}"
        bits += f"{tmp:0>11}"
    #unpaired charectors
    if len(t_string)%2:
        bits += " "
        tmp = f"{alphanumeric_key.index(t_string[-1]):b}"
        bits += f"{tmp:0>6}"
    #terminator
    bits += " "
    bits += "0000"
    print(bits)

    #codeword generation
    codewords = []
    codeword = ""
    for bit in bits:
        if bit == " ": continue
        codeword += bit
        if len(codeword) >= 8:
            codewords.append(codeword)
            codeword = ""
    if len(codeword):
        codewords.append(f"{codeword:0<8}")
    
    #pad codewords
    DATA_CODEWORD_QUANTITY = 9
    it = len(codewords)
    first = True
    for _ in range(it, DATA_CODEWORD_QUANTITY):
        if first:
            codewords.append("11101100")
            first = False
        else:
            codewords.append("11101100")
            first = True
    
    #error correction codewords
    ERROR_COORECTION_QUANTITY = 17
    ERROR_COORECTION_BLOCKS_QUANTITY = 1
    LOG = [_ for _ in range(256)]
    EXP = [_ for _ in range(255)]
    val = 1
    for e in range(1, 256):
        if val > 127:
            val = (val << 1) ^ 285
        else:
            val = (val << 1)
        LOG[val] = e % 255
        EXP[e % 255] = val

    def multiply(a, b):
        if a & b:
            return EXP[(LOG[a] + LOG[b]) % 255]
        else: return 0

    def divide(a, b):
        return EXP[(LOG[a] + LOG[b] * 254) % 255]

    def polynimial_multiply(poly1, poly2):
        print(poly1, poly2)
        coefficients = [_ for _ in range(len(poly1) + len(poly2) - 1)]
        for i in range(len(coefficients)):
            coefficient = 0
            for poly1Index in range(i+1):
                poly2Index = i - poly1Index
                print(poly1Index, poly1)
                coefficient = coefficient ^ multiply(poly1[poly1Index], poly2[poly2Index])
            coefficients[i] = coefficient
        return coefficients

    def polynomial_remainder(dividend, divisor):
        remainder = list(dividend)
        for count in range(len(dividend) - len(divisor) + 1):
            if remainder[0]:
                factor = divide(remainder[0], divisor[0])
                subtract = [_ for _ in range(len(remainder))]
                subtract.insert(polynimial_multiply(divisor, [factor]), 0)
                for i,val in enumerate(remainder):
                    remainder[i] = val ^ subtract[i]
                remainder = remainder[1:]
            else:
                remainder = remainder[1:]
    
    def get_generator_poly(e_codewords_num):
        lastPoly = [1]
        for i in range(e_codewords_num):
            lastPoly = polynimial_multiply(lastPoly, [1, EXP[i]])
        return lastPoly
    print(get_generator_poly(16))

    #(26, 9, 8)
    print(LOG)
    print(EXP)
    print(codewords)
#main()
import re
string = "x^17 + a^43 x^16 + a^139 x^15 + a^206 x^14 + a^78 x^13 + a^43 x^12 + a^239 x^11 + a^123 x^10 + a^206 x^9 + a^214 x^8 + a^147 x^7 + a^24 x^6 + a^99 x^5 + a^150 x^4 + a^39 x^3 + a^243 x^2 + a^163 x + a^136"

print(re.findall("(?<=a\^)\d+", string))