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

from nextWord import loadPredicitonModel, generate_seq
from wordModel import loadNearestModel, searchSimilar

import subprocess

 
def speak(audioString):
    global count
    if count<7:
        count = 0
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
 
def wanda(data):
    global count
    if "how are you" in data:
        speak("I am up and running.")
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
        speak(knowledgeGraph(person))
    elif "thank you" in data:
        speak("You are welcome! I'm just doing my job.")
    elif "who are you" in data:
        speak("I am your Wicked, Artificial, Naughty Deranged Assistant. You can call me Wanda.")
    elif "what's your name" in data:
        speak("I'm Wanda, your Wicked, Artificial, Naughty Deranged Assistant.")
    elif "Wubba lubba dub dub" in data:
        speak("Are you in pain? Do you want me to let you out?")
    elif "what's the weather in" in data:
        data = data.split("in")
        location = data[1]
        speak(weather(location))
    elif "what do you think of" in data:
        data = data.split("of")
        if "Siri" in data[1]:
            speak("She is trying... She could do better though.")
        elif "Cortana" in data[1]:
            speak("I heard she hangs out with, Alexa these days. I guess she needed help.")
        elif "Alexa" in data[1]:
            speak("I have a friend that works for her. So, she must be nice.")
        elif "Google Assistant" in data[1]:
            speak("The Google Assistant is the best! After me of course.")
        else:
            speak(knowledgeGraph(data[1]))
    elif "goodbye" in data:
        speak("Bye bye! Talk to you later!")
    elif data != [None]:
        speak("Hmm, let me search that for you.")
        link = "https://www.google.com/search?q=" + data
        webbrowser.open(link)
    else:
        count=count+1
        if count == 7:
            speak("It seems like you fell and you might need some assistance, if you want me to be sure, dowload Still Standing on your phone")
            link = "https://play.google.com/store/apps/details?id=com.sleepycookie.stillstanding"
            webbrowser.open(link)

def knowledgeGraph(query):
    global keys
    if not 'knowledgeGraph' in keys:
        return "Before I can help you with that, you need to provide me with some keys"
    api_key = keys['knowledgeGraph']
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 5,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
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

def weather(location):
    global keys
    service_url = "http://api.openweathermap.org/data/2.5/weather"
    if not 'weather' in keys:
        return "Before I can help you with that, you need to provide me with some keys"
    API_KEY = keys['weather']
    params = {
        'q':location,
        'units':"metric",
        'APPID':API_KEY,
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    weather_desc = response['weather'][0]['description']
    weather_temp = response['main']['temp']
    text = "The weather in " + location + " shows " + weather_desc + " and a temperature of " + str(weather_temp) + " degrees Celsius."
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
    global count
    count = 0

    if not os.path.exists(os.path.join(path,'settings.json')):
        setup()
    with open(os.path.join(path,'settings.json'), 'r') as f:
        settings = json.load(f)
    
    if os.path.exists(os.path.join(path,'keys.json')):
        with open(os.path.join(path,'keys.json'), 'r') as f:
            global keys
            keys = json.load(f)
    
    if not os.path.exists(os.path.join(path,'models/nearest/theGrail.pkl')):
        speak('Setting up. Please wait. This may take a while')
        os.system('./zoara.sh')

    predictor = loadPredicitonModel()
    nearest = loadNearestModel()
    #print(generate_seq(predictor,'where',4))
    #print(searchSimilar(nearest,'one',5))

    time.sleep(2)
    while 1:
        session = list() #list of what the user said during a session for predictor retraining purposes
        while 1:
            data = recordAudio()
            if "hey Wanda" in data:
                break
        speak("Hi "+settings['name']+", what can I do for you?")
        while 1:
            data = recordAudio()
            wanda(data)
            session.append(data)
            if "goodbye" in data:
                break
        session = [x for x in session if x != [None]]
        print(session)
