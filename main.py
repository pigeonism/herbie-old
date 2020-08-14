# Herbie tk
# wayne w 2018

import tkinter as tk
from chatter import *
from subprocess import Popen

class Herbie(tk.Frame):

    def __init__(self, master=None):
        
        # chatter setup
        self.chat = Chatter()
        self.chat.get_testwords_file_lengths()
        self.chat.buld_wordTypes_rand()
        self.herbie_audio = False
        
        # the rest is tk
        tk.Frame.__init__(self, master)
        self.config(bd=1, relief="ridge", width="5i")
        self.config(background="blue")
        #print (tk.Frame.keys(self))
        #self.test_k(tk.Frame.keys(self))
        self.pack()
        
        # herbie label
        self.label_frame = tk.LabelFrame()
        self.label_herbie = tk.Label()
        self.herbie_txt = tk.StringVar()
        self.herbie_txt.set("Hello") # or previous greetings from db
        self.label_herbie["textvariable"] = self.herbie_txt
        #self.label_herbie.pack(pady="0.2i")
        self.label_frame.pack(pady="0.2i", ipadx="0.2i", ipady="0.2i")
        self.label_herbie.pack(in_=self.label_frame)
        
        #entry
        self.entryfield = tk.Entry()
        self.entryfield.pack(padx="0.2i",pady="0.2i", fill='x')

        #app variable
        self.contents = tk.StringVar()
        self.contents.set("type reply here")
        
        #keep an eye on the variable
        self.entryfield["textvariable"] = self.contents

        #get pass btn
        self.buttonpass = tk.Button()
        self.buttonpass["text"] = "Reply"
        self.buttonpass["command"] = self.reply
        self.buttonpass["relief"] = "ridge"
        self.buttonpass.pack(pady="0.2i")

        # quitttt
        #self.quit = tk.Button(self, text="Quit", command=self.quit)
        #self.quit.pack(pady="0.2i")

        # check for enter key press.
        self.bind_all('<KeyPress-Return>', self.enter_pressed)


    def feed_replies(self, fileName):
        """fill herbie db with more sentences"""
        sentenceFile = open(fileName, "r")
        sentenceList = sentenceFile.readlines()
        for s in sentenceList:
            self.contents.set(s)
            self.reply()
        
    
    def enter_pressed(self, someVal=None):
        # respond if enter pressed as well
        self.reply()

    # skip or disable 'say' if using feed_replies
    def say(self, text):
        if self.herbie_audio:
            Popen(["spd-say", "-r", "-100","-t", "female3", text])
        
    def reply(self):
        # on reply clicked, send to herbieee
        entry_text = self.contents.get()
        if len(entry_text) > 0:
            herbie_say = self.chat.lets_chat_gui(entry_text)
            self.herbie_txt.set(herbie_say)
            # testing speech, disable this if using feed_replies
            self.say(herbie_say)
        else:
            herbie_say = "What was that?"
            self.say(herbie_say)
            self.herbie_txt.set(herbie_say)

        self.contents.set("")
        
            
root = tk.Tk()
root.title("Herbie")
app = Herbie(master=root)
app.mainloop()
