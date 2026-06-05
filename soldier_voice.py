from urllib.error import URLError
from urllib.request import urlopen
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
from pygame import mixer
import random
import aiml
import os
import time
import sys
import subprocess

class bot : 
    def __init__(self):
        self.internet = None 
  

    def ping(self):
        
        try:
            urlopen('http://google.com', timeout=1)
            self.internet = "online"
            return True
        except URLError as err:
            self.internet = "offline"
            return False


    def listen(self):
        
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("I am listening: ")
            audio = r.listen(source)
        try:
            if self.internet == "online":
                data = r.recognize_google(audio) 
                print(data)
                return  data
            else:
                data = r.recognize_sphinx(audio)
                print(data)
                return  data
        except sr.UnknownValueError:
            self.speak("I couldn't understand what you said! Would you like to repeat?")
            return(self.listen())
        except sr.RequestError as e:
            print("Could not request results from speech service; {0}".format(e))

    def speak(self , text ,):
        if self.internet == "online":
            try :
                tts = gTTS(text=text, lang='en')
                tts.save("temp_soundtrack_tts.mp3")
            except : 
                raise Exception("Fetch Error")
            subprocess.run(["ffmpeg" , "-i" , "temp_soundtrack_tts.mp3" , "temp_soundtrack_tts.wav" , "-y"])
            
            subprocess.run(["paplay" , "temp_soundtrack_tts.wav"])
            
        


    def mainloop(self):
        self.ping()
        kernel = aiml.Kernel()
        if os.path.isfile("bot_brain.brn"):
            kernel.bootstrap(brainFile = "bot_brain.brn")
        else:
            kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
            #kernel.saveBrain("bot_brain.brn")

        while True:
            que = self.listen()
            if que.strip().lower() in ['shutdown','exit','quit','gotosleep','goodbye','terminate']:
                break
            res = kernel.respond(que)
            if res != "":
                print("Answer: " + res)
                self.speak(res)
                



if __name__ == "__main__" : 
    b = bot() 
    b.mainloop()