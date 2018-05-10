#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
from time import strftime, localtime
import time
import os
import sys
import json
from collections import defaultdict
import webbrowser
from stemming.porter2 import stem

from nextWord import loadPredicitonModel, generateSeq
from wordModel import loadNearestModel, searchSimilar

import utils

def wanda(data):
    if "how are you" in data:
        utils.speak("I am up and running.")
    elif "what time is it" in data:
        utils.speak("It's " + strftime("%H:%M", localtime()))
    elif "what is the date" in data:
        utils.speak("Today is "+ strftime("%A, %d %B %Y", localtime()))
    elif "where is" in data:
        data = data.split("is")
        location = data[1]
        utils.speak("Hold on " + settings['name'] + ", I will show you where " + location + " is.")
        link = "https://www.google.com/maps/place/" + location + "/&amp;"
        webbrowser.open(link)
    elif "who is" in data:
        data = data.split("is")
        person = data[1]
        utils.speak(utils.knowledgeGraph(person,keys['knowledgeGraph']))
    elif "thank you" in data:
        utils.speak("You are welcome! I'm just doing my job.")
    elif "who are you" in data:
        utils.speak("I am your Wicked, Artificial, Naughty Deranged Assistant. You can call me Wanda.")
    elif "what is your name" in data:
        utils.speak("I'm Wanda, your Wicked, Artificial, Naughty Deranged Assistant.")
    elif "wubba lubba dub dub" in data:
        utils.speak("Are you in pain? Do you want me to let you out?")
    elif "what is the weather in" in data:
        data = data.split("in")
        location = data[1]
        if location == '':
            location=generateSeq(predictor,"what is the weather in",1)
        utils.speak(utils.weather(location,keys['weather']))
    elif "what do you think of" in data:
        data = data.split("of")
        if "siri" in data[1]:
            utils.speak("She is trying... She could do better though.")
        elif "cortana" in data[1]:
            utils.speak("I heard she hangs out with, Alexa these days. I guess she needed help.")
        elif "alexa" in data[1]:
            utils.speak("I have a friend that works for her. So, she must be nice.")
        elif "google assistant" in data[1]:
            utils.speak("The Google Assistant is the best! After me of course.")
        else:
            utils.speak(utils.knowledgeGraph(data[1]),keys['knowledgeGraph'])
    elif "goodbye" in data:
        utils.speak("Bye bye! Talk to you later!")
    elif data != [None]:
        utils.speak("Hmm, let me search that for you.")
        link = "https://www.google.com/search?q=" + data
        webbrowser.open(link)
    else:
        utils.count=utils.count+1
        if utils.count == 7:
            utils.speak("It seems like you fell and you might need some assistance, if you want me to be sure, download Still Standing on your phone.")
            link = "https://play.google.com/store/apps/details?id=com.sleepycookie.stillstanding"
            webbrowser.open(link)

<<<<<<< HEAD
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
    text = "The weather in" + location.title() + " shows " + weather_desc + " and a temperature of " + str(weather_temp) + " degrees Celsius."
    return text

def stringProcess(data):
    synDict = {
        "what's": "what is",
        "who's": "who is",
        "where's": "where is",
        "thanks": "thank you",
        "think about": "think of"
    }

    for s in synDict.keys():
        data = data.replace(s, synDict[s])
    
    return data

=======
>>>>>>> e5fe2749c3f4fb9c0dbfa299641cc7a556cc9303
def setup():
    settings = defaultdict(int)
    utils.speak("What is your name?")
    while settings['name']==0:
        settings['name'] = utils.recordAudio()
    with open(os.path.join(path,'settings.json'), 'w') as f:
        json.dump(settings, f)

if __name__ == '__main__':
    # initialization
    path = os.path.dirname(os.path.realpath(sys.argv[0]))

    global keys
    keys = defaultdict(int)

    if not os.path.exists(os.path.join(path,'settings.json')):
        setup()
    with open(os.path.join(path,'settings.json'), 'r') as f:
        settings = json.load(f)
    
    if os.path.exists(os.path.join(path,'keys.json')):
        with open(os.path.join(path,'keys.json'), 'r') as f:
            keys = json.load(f)
            keys = defaultdict(int, keys)
    
    if not os.path.exists(os.path.join(path,'models/nearest/theGrail.pkl')):
        utils.speak('Setting up. Please wait. This may take a while')
        os.system('./zoara.sh')

    global predictor

    predictor = loadPredicitonModel()
    nearest = loadNearestModel()
    # print(generateSeq(predictor,'where',4))
    # print(searchSimilar(nearest,'one',5))

    time.sleep(2)
    while 1:
        session = list() #list of what the user said during a session for predictor retraining purposes
        while 1:
            data = utils.recordAudio()
            if "hey wanda" in data:
                break
        utils.speak("Hi "+settings['name']+", what can I do for you?")
        while 1:
            data = utils.recordAudio()
            wanda(data)
            session.append(data)
            if "goodbye" in data:
                break
        session = [x for x in session if x != [None]]
        print(session)
