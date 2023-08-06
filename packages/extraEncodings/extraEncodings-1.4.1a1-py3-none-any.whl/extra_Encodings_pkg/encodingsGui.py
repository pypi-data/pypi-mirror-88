'''VERY UNCLEAN AND MESSY CODE WHICH MAKES  A DARKMODE GUI VERSION OF AN ENCODER WITHOUT ICHOR '''
import ciphers
from ciphers import *
from tkinter import *
import os
def startGUI():
    root = Tk()
    root.title("Encoding GUI")
    root.configure(bg='black')
    root.maxsize()
    Mainframe = Frame(root)   
    Mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
    Mainframe.configure(bg='black')
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0, weight=1)
    encodablevar = StringVar()
    encoded_string = StringVar()
    wew = IntVar()
    entry = Entry(Mainframe,width=12,textvariable=encodablevar,bg='black',fg='dark cyan')
    entry.grid(column=3,row=1,sticky=(N,W))
    entry.focus()
    def GEN2codeGUI():
     ''' Only use with r-strings due to % and \. Don't mind strange coloration as that is just your text   editor rendering it incorrectly'''
     encoded_string.set('')
     entryvalue = entry.get()
     Character_to_decode = str(entryvalue)
     for character in Character_to_decode:
         charpos = Gen2.index(character)
         ResultStr = str(Gen2[-charpos])
         encoded_string.set(str(encoded_string.get()) + ResultStr)
    def GTX2CodeGUI():
        entryvalue = entry.get()
        '''Only use with r-strings due to % and \. Don't mind strange coloration as that is just your text editor rendering it incorrectly'''
        #make sure this is always a string
        encoded_string.set('')
        Character_to_decode = str(entryvalue)
        for character in Character_to_decode:
            charpos = GTX2.index(character)
            ResultStr = str(GTX2[-charpos - 1])
            encoded_string.set(str(encoded_string.get()) + ResultStr)
    def LTF64CodeGUI(): 
        '''Only use with r-strings due to % and \. Don't mind strange coloration as that is just your text editor rendering it incorrectly'''
        #make sure this is always a string
        encoded_string.set('')
        entryvalue = entry.get()
        Character_to_decode = str(entryvalue)
        for character in Character_to_decode:
            charpos = LTF64.index(character)
            ResultStr = str(LTF64[-charpos -2])
            encoded_string.set(str(encoded_string.get()) + ResultStr)
    def encoderGUI():
        if wew.get() ==0:
            LTF64CodeGUI()
        if wew.get() == 1:
            GTX2CodeGUI()
        if wew.get() == 2:
            GEN2codeGUI()
    def kill():
        os.sys.exit()
    Button(Mainframe,text='Encode',command=encoderGUI,bg='black',fg='dark cyan').grid(column=3,row=4)
    Button(Mainframe,text='Quit',command=kill,bg='black',fg='dark cyan') .grid(column=3,row=5)
    Radiobutton(Mainframe,text='LTF64',variable=wew,value=0,bg='black',fg='dark cyan').grid(column=1,row=1,sticky=(N))
    Radiobutton(Mainframe,text='GTX2',variable=wew,value=1,bg='black',fg='dark cyan').grid(column=1,row=2,sticky=(N))
    Radiobutton(Mainframe,text='Gen2',variable=wew,value=2,bg='black',fg='dark cyan').grid(column=1,row=3,sticky=(N))
    Label(Mainframe,text='Encoder',bg='black',fg='dark cyan').grid(column=3,row=0,sticky=(N))
    Label(Mainframe,text='Encoded text:',bg='black',fg='dark cyan').grid(column=3,row=2,sticky=(N))
    Entry(Mainframe,textvariable=encoded_string,bg='black',fg='dark cyan').grid(column=4,row=2)
    for child in Mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    root.bind("<Return>", encoderGUI)
    Mainframe.mainloop()
