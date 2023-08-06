#ichor
ichorEn = {
    "a":"1",
    "A":"2",
    "b":"3",
    "B":"4",
    "c":"5",
    "C":"6",
    "d":"7",
    "D":"8",
    "e":"9",
    "E":"10",
    "f":"11",
    "F":"12",
    "g":"13",
    "G":"14",
    "h":"15",
    "H":"16",
    "i":"17",
    "I":"18",
    "j":"19",
    "J":"20",
    "k":"21",
    "K":"22",
    "l":"23",
    "L":"24",
    "m":"25",
    "M":"26",
    "n":"27",
    "N":"28",
    "o":"29",
    "O":"30",
    "p":"31",
    "P":"32",
    "q":"33",
    "Q":"34",
    "r":"35",
    "R":"36",
    "s":"37",
    "S":"38",
    "t":"39",
    "T":"40",
    "u":"41",
    "U":"42",
    "v":"43",
    "V":"44",
    "w":"45",
    "W":"46",
    "x":"47",
    "X":"48",
    "y":"49",
    "Y":"50",
    "z":"51",
    "Z":"52",
    " ":"53",
    ".":"54",
    "?":"55",
    "!":"56",
    ",":"57",
    ";":"58",
    ":":"59",
    "'":"60",
    '"':"61",
    "@":"62",
}

ichorDe = {
    "1":"a",
    "2":"A",
    "3":"b",
    "4":"B",
    "5":"c",
    "6":"C",
    "7":"d",
    "8":"D",
    "9":"e",
    "10":"E",
    "11":"f",
    "12":"F",
    "13":"g",
    "14":"G",
    "15":"h",
    "16":"H",
    "17":"i",
    "18":"I",
    "19":"j",
    "20":"J",
    "21":"k",
    "22":"K",
    "23":"l",
    "24":"L",
    "25":"m",
    "26":"M",
    "27":"n",
    "28":"N",
    "29":"o",
    "30":"O",
    "31":"p",
    "32":"P",
    "33":"q",
    "34":"Q",
    "35":"r",
    "36":"R",
    "37":"s",
    "38":"S",
    "39":"t",
    "40":"T",
    "41":"u",
    "42":"U",
    "43":"v",
    "44":"V",
    "45":"w",
    "46":"W",
    "47":"x",
    "48":"X",
    "49":"y",
    "50":"Y",
    "51":"z",
    "52":"Z",
    "53":" ",
    "54":".",
    "55":"?",
    "56":"!",
    "57":",",
    "58":";",
    "59":":",
    "60":"'",
    "61":'"',
    "62":"@",
}
#Gen2
Encodeable_letters = r'''aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ1234567890!@\#$%^&*()`~-=_+[]}{'\";:| ,.<>/?'''
Gen2=[]
#Sorry for making this capital
LTF64 = []
GTX2 = []
for letter in Encodeable_letters:
    Gen2.append(letter)
    LTF64.append(letter)
    GTX2.append(letter)

def Gen2Code(Character_to_decode):
    ''' Only use with r-strings due to % and \. Don't mind strange coloration as that is just your text   editor rendering it incorrectly'''
    #make sure this is always a string
    Character_to_decode = str(Character_to_decode)
    for character in Character_to_decode:
        charpos = Gen2.index(character)
        ResultStr = str(Gen2[-charpos])
        print(ResultStr,end='')

def LTF64Code(Character_to_decode):
    '''Only use with r-strings due to % and \. Don't mind strange coloration as that is just your text editor rendering it incorrectly'''
    #make sure this is always a string
    Character_to_decode = str(Character_to_decode)
    for character in Character_to_decode:
        charpos = LTF64.index(character)
        ResultStr = str(LTF64[-charpos - (1 * -2)])
        print(ResultStr,end='')
def GTX2Code(Character_to_decode):
    '''Only use with r-strings due to % and \. Don't mind strange coloration as that is just your text editor rendering it incorrectly'''
    #make sure this is always a string
    Character_to_decode = str(Character_to_decode)
    for character in Character_to_decode:
        charpos = LTF64.index(character)
        ResultStr = str(LTF64[-charpos - (1 * -3)])
        print(ResultStr,end='')
#Example \/ Make sure to reset the file once you are finshed or make a copy of this file
#LTF64Code(r'Fire balls')

