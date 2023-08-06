#imports
import os
import time
import  extra_Encodings_pkg.ciphers
from  extra_Encodings_pkg.ciphers import *
import  extra_Encodings_pkg.encodingsGui
#functions to encode and decode
def encodeto():
    entype = input("Which encoding?")
    if entype.upper() == "ichor".upper():
        obj = input("Encode:")
        for character in obj:
            encode = ichor[character]
            if character == obj[-1]:
                print(encode,end="\n")
            else:
                print(encode,end=" ")
    if entype.upper() == "GEN2":
        Gen2Code(input('Encode:'))
    if entype.upper() == 'LTF64':
        LTF64Code(input('Encode:'))
    if entype.upper() == 'GTX2':
        GTX2Code(input('Decode '))

def decodeto():
    detype = input("Which decoding?")
    if detype.upper() == "ichor".upper():
        obj = input("Decode:")
        objspce = obj.count(" ") + 1
        obj = obj.split(" ")
        for r in range(objspce):
            de = int(obj[r])
            decode = ichor.rev_dict[de]
            if de == obj[-1]:
                print(decode,end="\n")
            else:
                print(decode,end="")
    if detype.upper() == "GEN2":
        Gen2Code(input('Decode:'))
    if detype.upper() == 'LTF64':
        LTF64Code(input('Decode:'))
    if detype.upper() == 'GTX2':
        GTX2Code(input('Decode '))
            
def clear():
    ostype = os.name
    if ostype.upper() == 'posix'.upper():
        os.system('clear')
    if ostype.upper() == 'nt'.upper():
        os.system('cls')




#while true loop for coder
def coder():
    x = ""
    clear()
    while x != "exit".upper():
        x = input("\nEncode, Decode, Clear, Credits,GUI, or exit?:")
        x = x.upper()
        if x == "encode".upper():
            encodeto()
        if x == "decode".upper():
            decodeto()
        if x  == "Credits".upper():
            print("Everything: Codecode")
            time.sleep(1)
        if x == "clear".upper():
            clear()
        if x == "GUI".upper():
            encodingsGui.startGUI()
if __name__ == "__main__":
    coder()
