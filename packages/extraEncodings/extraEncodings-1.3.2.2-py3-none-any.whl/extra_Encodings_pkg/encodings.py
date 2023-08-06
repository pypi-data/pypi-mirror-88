#imports
import os
import time
from ciphers import *
#functions to encode and decode
def encodeto():
    entype = input("Which encoding?")
    if entype.upper() == "ichor".upper():
        obj = input("Encode:")
        for character in obj:
            encode = ichorEn[character]
            if character == obj[-1]:
                print(encode,end="\n")
            else:
                print(encode,end=" ")

def decodeto():
    detype = input("Which decoding?")
    if detype.upper() == "ichor".upper():
        obj = input("Decode:")
        objspce = obj.count(" ") + 1
        obj = obj.split(" ")
        for r in range(objspce):
            de = obj[r]
            decode = ichorDe[de]
            if de == obj[-1]:
                print(decode,end="\n")
            else:
                print(decode,end="")
            
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
        x = input("Encode, Decode, Clear, Credits, or exit?:")
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
if __name__ == "__main__":
    coder()
