#!/usr/bin/python3
from urllib.request import urlopen
from urllib.error import URLError
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import time
import aiml
import pyttsx3
import threading
from gtts.tts import gTTS
from pygame import mixer
import speech_recognition as sr
from PyQt5 import QtCore
from PyQt5.QtGui import QMovie , QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QSystemTrayIcon, QMenu , QMessageBox


internet = "online"
mode = "voice"
def ping():
    try:
        urlopen('http://google.com', timeout=1)
        internet = "online"
        return True
    except URLError as err:
        internet = "offline"
        return False

if any(item in sys.argv for item in ["--chat", "chat", "-c"]):
    mode = "chat"
if any(item in sys.argv for item in ["--offline", "offline", "-O"]):
    internet = "offline"
else:
    ping()


class QMainWindow(QLabel):
    def __init__(self, fileName):
        QLabel.__init__(self)
        thread = Thread(self)
        m = QMovie(fileName)
        m.start()
        self.setMovie(m)
        app.aboutToQuit.connect(thread.stop)
        thread.start()

    def setMovie(self, movie):
        QLabel.setMovie(self, movie)
        s=movie.currentImage().size()
        self._movieWidth = s.width()
        self._movieHeight = s.height()


class Thread(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self.window = parent
        self._lock = threading.Lock()
        self.running = True

    def run(self):
        self.running = True

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
            if mode == "chat":
                que = input("Talk to Me: ")
            else:
                que = listen()
            if que.strip().lower() in ['shutdown','exit','quit','gotosleep','goodbye','terminate']:
                app.quit()
                break
            res = kernel.respond(que)
            if res != "":
                print("Answer: " + res)
                speak(res, internet)


    def stop(self):
        engine = pyttsx3.init()
        engine.setProperty("voice", engine.getProperty("voices")[1].id)
        engine.setProperty("rate", 175)
        engine.say("goodbye sir")
        engine.runAndWait()
        self.running = False


if __name__ == '__main__':
    print(sys.argv)
    print(mode)
    print(internet)

    app = QApplication(sys.argv)

    win = QMainWindow('icons/main.gif')
    win.setWindowTitle("SOLDIER")
    win.show()

    trayIcon = QSystemTrayIcon(QIcon('icons/icon.png'), parent=app)
    trayIcon.setToolTip('SOLDIER 1.0.0')
    trayIcon.show()

    msg = QMessageBox()
    msg.setWindowTitle("Info")
    msg.setText("\nSOLDIER v1.0.0\n\nA voice assistant robot that can do a series of pre-set tasks for you and maybe talk to you a little.\n\nhttps://github.com/ali-moments/No-Name\n")

    menu = QMenu()
    moreAction = menu.addAction('More info')
    moreAction.triggered.connect(msg.show)
    exitAction = menu.addAction('Exit')
    exitAction.triggered.connect(app.quit)

    trayIcon.setContextMenu(menu)
    sys.exit(app.exec_())
