#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr
from time import ctime
import time
import os
import sys
from gtts import gTTS
import json
from collections import defaultdict
import webbrowser

 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
 
def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
 
def jarvis(data):
    if "how are you" in data:
        speak("I am fine")
 
    if "what time is it" in data:
        speak(ctime())
 
    if "where is" in data:
        data = data.split(" ")
        location = data[2]
        speak("Hold on Frank, I will show you where " + location + " is.")
        # os.system("chromium-browser https://www.google.nl/maps/place/" + location + "/&amp;")
        link = "https://www.google.nl/maps/place/" + location + "/&amp;"
        webbrowser.open(link)

def setup():
    settings = defaultdict(int)
    speak("What is your name")
    while settings['name']==0:
        settings['name'] = recordAudio()
    with open(os.path.join(path,'settings.json'), 'w') as f:
        json.dump(settings, f)

if __name__ == '__main__':
    # initialization
    path = os.path.dirname(os.path.realpath(sys.argv[0]))

    if not os.path.exists(os.path.join(path,'settings.json')):
        setup()
    with open(os.path.join(path,'settings.json'), 'r') as f:
        settings = json.load(f)

    time.sleep(2)
    speak("Hi "+settings['name']+", what can I do for you?")
    while 1:
        data = recordAudio()
        jarvis(data) 