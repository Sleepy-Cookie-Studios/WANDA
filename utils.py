import speech_recognition as sr
from gtts import gTTS
import os
import urllib
import json

def knowledgeGraph(query, key):
    if key == 0:
        return "Before I can help you with that, you need to provide me with some keys"

    api_key = key
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

def weather(location, key):
    if key == 0:
        return "Before I can help you with that, you need to provide me with some keys"
    
    service_url = "http://api.openweathermap.org/data/2.5/weather"
    API_KEY = key
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