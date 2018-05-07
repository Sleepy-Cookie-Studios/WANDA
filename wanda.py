#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr
from time import strftime, localtime
import time
import os
import sys
from gtts import gTTS
import json
from collections import defaultdict
import webbrowser
import urllib

 
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
        data = [None]
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
 
def jarvis(data):
    if "how are you" in data:
        speak("I am fine.")
 
    elif "what time is it" in data:
        speak("It's " + strftime("%H:%M", localtime()))

    elif "what is the date" in data:
        speak("Today is "+ strftime("%A, %d %B %Y", localtime()))
 
    elif "where is" in data:
        data = data.split("is")
        location = data[1]
        speak("Hold on " + settings['name'] + ", I will show you where " + location + " is.")
        link = "https://www.google.com/maps/place/" + location + "/&amp;"
        webbrowser.open(link)

    elif "who is" in data:
        data = data.split("is")
        person = data[1]
        speak(knowledgegraph(person))
    
    elif "thank you" in data:
        speak("You are welcome! I'm just doing my job.")

    elif data != [None]:
        speak("Hmm, let me search that for you.")
        link = "https://www.google.com/search?q=" + data
        webbrowser.open(link)

def knowledgegraph(query):
    API_KEY = "AIzaSyDxBZk1LpvBZ0as-ddQHvbQN6rwlT7AygY"
    # api_key = open('.api_key').read()
    api_key = API_KEY
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 5,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    # print(json.dumps(response, indent=2))

    try:
        text = response['itemListElement'][0]['result']['detailedDescription']['articleBody']
        if text != "goog:detailedDescription" or text != None:
            return text
        else:
            text = "I couldn't find any information."
            return text
    except:
        text = "I couldn't find any information."
        return text

def setup():
    settings = defaultdict(int)
    speak("What is your name?")
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