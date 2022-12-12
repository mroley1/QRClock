# pototyping

#target: QR Model 2, v.1 alphanumeric, ECC level H


import time

def main():
    alphanumeric_key = "0123456789ABCDEFGHIJKLMONPQRSTUVWXYZ $%*+-./:"
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
    #(26, 9, 8)
    print(codewords)
main()

# x^17 + a^43 x^16 + a^139 x^15 + a^206 x^14 + a^78 x^13 + a^43 x^12 + a^239 x^11 + a^123 x^10 + a^206 x^9 + a^214 x^8 + a^147 x^7 + a^24 x^6 + a^99 x^5 + a^150 x^4 + a^39 x^3 + a^243 x^2 + a^163 x + a^136