import speech_recognition as sr
from time import strftime, localtime
from gtts import gTTS
import os
import urllib
import json
import webbrowser

from nextWord import generateSeq

def knowledgeGraph(args):
    #args 0 -> data, 1 -> key, 2 -> predictor
    if args[1] == 0:
        return "Before I can help you with that, you need to provide me with some keys"

    query = args[0].split("is")[1]

    if query == '':
        speak("I couldn't hear who you are talking about. Please repeat the name")
        query=[None]
        while query == [None]:
            query=recordAudio()

    api_key = args[1]
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

def weather(args):
    #args 0 -> data, 1 -> key, 2 -> predictor

    if args[1] == 0:
        return "Before I can help you with that, you need to provide me with some keys"
    data = args[0].split("in")
    location = data[1]

    if location == '':
        speak("Sure! What's the location, again?")
        location=[None]
        while location == [None]:
            location=recordAudio()

    service_url = "http://api.openweathermap.org/data/2.5/weather"
    API_KEY = args[1]
    params = {
        'q':location,
        'units':"metric",
        'APPID':API_KEY,
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    weather_desc = response['weather'][0]['description']
    weather_temp = response['main']['temp']
    text = "The weather in " + location.title() + " shows " + weather_desc + " and a temperature of " + str(weather_temp) + " degrees Celsius."
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

def getTime(args):
    return "It's " + strftime("%H:%M", localtime())
def getDate(args):
    return "Today is "+ strftime("%A, %d %B %Y", localtime())
def getPlace(args):
    #args 0 -> data, 1 -> settings
    data = args[0].split("is")
    location = data[1]
    link = "https://www.google.com/maps/place/" + location + "/&amp;"
    webbrowser.open(link)
    return("Hold on " + args[1]['name'] + ", I will show you where " + location + " is.")
def opinion(args):
    #args 0 -> data, 1 -> key
    data = args[0].split("of")
    if "siri" in data[1]:
        return "She is trying... She could do better though."
    elif "cortana" in data[1]:
        return "I heard she hangs out with, Alexa these days. I guess she needed help."
    elif "alexa" in data[1]:
        return "I have a friend that works for her. So, she must be nice."
    elif "google assistant" in data[1]:
        return "The Google Assistant is the best! After me of course."
    else:
        return knowledgeGraph(["is "+data[1],args[1]])
def stillStanding():
    global count
    count+=1
    if count == 7:
        link = "https://play.google.com/store/apps/details?id=com.sleepycookie.stillstanding"
        webbrowser.open(link)
        speak("It seems like you fell and you might need some assistance, if you want me to be sure, download Still Standing on your phone.")
def default(args):
    link = "https://www.google.com/search?q=" + args[0]
    webbrowser.open(link)
    return "Hmm, let me search that for you."

def speak(audioString):
    global count
    try:
        if count<7:
            count = 0
    except NameError:
        count = 0
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 -q audio.mp3")
 
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

    if data!=[None]:
        data = stringProcess(data).lower()

    return data