import aiml
import os

kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")

while True:
    que = input("Talk to me: ")
    if que.strip().lower() in ['shutdown','exit','quit','gotosleep','goodbye','terminate']:
        break
    res = kernel.respond(que)
    print("Answer: " + res)

