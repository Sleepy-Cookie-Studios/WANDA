#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

#from time import strftime, localtime
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

def setup():
    settings = defaultdict(lambda:[None])
    utils.speak("What is your name?")
    while settings['name'] == [None]:
        settings['name'] = utils.recordAudio()
    with open(os.path.join(path,'settings.json'), 'w') as f:
        json.dump(settings, f)

def setupSkills(path):
    knownSkillsNames=['howAreYou','time','date','place','who','thanks','identify','rick','weather','opinions','goodbye','introduce']
    knownSkills = list()
    for skill in knownSkillsNames:
        with open(os.path.join(path,skill+'.json'), 'r') as f:
            knownSkills.append(json.load(f))
    return knownSkills

def wandaV2(data, knownSkills, method):
    for skill in knownSkills:
        thingy = (e in data for e in skill[method])
        if any(thingy):
            if skill['responseType']=='text':
                utils.speak(skill['response'][0])
            else:
                args = list()
                for argument in skill['arguments']:
                    if argument==None:
                        break
                    args.append(eval(argument))
                utils.speak(getattr(utils , skill['response'][0])(args))
            return
    if data != [None]:
        if method=='trigger':                
            wandaV2(data,knownSkills, 'extendedTrigger')
        else:
            utils.speak(utils.default([data]))
    else:
        utils.stillStanding()



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

    global nearest
    nearest = loadNearestModel()
    nearestDepth = 1

    skills = setupSkills(os.path.join(path,'skillset'))

    for skill in skills:
        newTriggers = list()
        for trigger in skill['trigger']:
            words = trigger.split(' ')
            for word in words:
                newWord = searchSimilar(nearest,word,nearestDepth)
                if newWord is None:
                    continue
                newTriggers.append(trigger.replace(word,''.join(newWord)))
        skill['extendedTrigger'] = newTriggers
        #print(skill['extendedTrigger'])

    closure = ['goodbye',''.join(searchSimilar(nearest,'goodbye',nearestDepth))]

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
            wandaV2(data, skills, 'trigger')
            session.append(data)
            if any(e in data for e in closure):
                break
        session = [x for x in session if x != [None]]
        print(session)