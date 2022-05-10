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


def ping():
    global internet
    try:
        urlopen('http://google.com', timeout=1)
        internet = "online"
        return True
    except URLError as err:
        internet = "offline"
        return False

ping()
if len(sys.argv) > 1 and sys.argv[1] in ["--offline", "offline", "-O"]:
    internet = "offline"

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening: ")
        audio = r.listen(source)
    try:
        if internet == "online":
            print(r.recognize_google(audio))
            return  r.recognize_google(audio)
        else:
            print(r.recognize_sphinx(audio))
            return  r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        speak("I couldn't understand what you said! Would you like to repeat?")
        return(listen())
    except sr.RequestError as e:
        print("Could not request results from speech service; {0}".format(e))

def speak(text, mode=internet):
    if mode == "online":
        tts = gTTS(text=text, lang='en')
        tts.save("temp_soundtrack_tts.mp3")
        mixer.init()
        mixer.music.load("temp_soundtrack_tts.mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)
    else:
        engine = pyttsx3.init()
        engine.setProperty("voice", engine.getProperty("voices")[1].id)
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()


kernel = aiml.Kernel()
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
    #kernel.saveBrain("bot_brain.brn")

while True:
    que = listen()
    if que.strip().lower() in ['shutdown','exit','quit','gotosleep','goodbye','terminate']:
        break
    res = kernel.respond(que)
    if res != "":
        print("Answer: " + res)
        speak(res, internet)

