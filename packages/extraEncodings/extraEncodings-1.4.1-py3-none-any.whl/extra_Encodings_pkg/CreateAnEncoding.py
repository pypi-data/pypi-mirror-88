#import the items
import  extra_Encodings_pkg.ciphers
from  extra_Encodings_pkg.ciphers import *
#make the encoding.
#The rate argument shows changes the dict. For example is it's 3 then a:3 A:6 b:9 B:12 and so on and forth. 
encoding = Encoding(3)
#this prints the encoding dict
print(encoding.encoding)
#this prints the decodsing dict
print(encoding.encoding.rev_dict)
# this prints the value  that is contained in key A in the encoding dictionary
print(encoding.encoding['A'])
#this prints the value that is contained in key 6   in the decoding dictionary
print(encoding.encoding.rev_dict[6])
#Notes
# Decode with instance.encoding.rev_dict
#encode with instance.encoding
