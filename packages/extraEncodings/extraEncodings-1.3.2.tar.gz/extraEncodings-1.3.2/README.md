# Extra encodings for Python 

##  1.3.2 | Latest Update News
_____  
Gen2 and LTF64 released for beta and ichor has progressed for US keyboard.
Updated import process for beta for technical reasons
Added support for people up till  Python 3.6 

## Plans for future updates:
______
Add more Encodings and Decodings\
Work on a version for python 3.4 and older (For whoever still uses that)\
Make a Gui (tkinter) for the encoder\
Add Binary encodings

## Notes
____
Currently we only support all characters on a US keyboard for all encoding types and a computer that runs a standard os like Win32/64 , macOS (Not tested), Linux Debian,Ubuntu and distros based on them.

## Decodings and encodings:
_____
Ichor (Not fully finshed)\
Gen2\
LTF-64
GTX2 (Not in any of the encoders but encoding is available in ciphers.py)

## How to import
_____
`from extra_Encodings.extra_Encodings_pkg.encodings import *` \
To import beta versions\
`from extra_Encodings.extra_Encodings_pkg.encodingsbeta import *`\
To import raw encoder for Gen2, GTX2 and LTF64 and dicts for ichor\
`from extra_Encodings.extra_Encodings_pkg.ciphers import *`