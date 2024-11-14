import speech_recognition as sr
import os
import time
import pyttsx3
import webbrowser
import subprocess as sp
import keyboard #type: ignore
import requests
import re

from decouple import Config, RepositoryEnv
from datetime import datetime
from random import choice
from conv import random_text
from online import find_my_id, search_on_google, search_on_wikipedia, youtube
from bs4 import BeautifulSoup

# *** Setting up the voice engine ***
engine = pyttsx3.init('sapi5') 
# pyttsx3 converts the given text into speech
# sapi5 is microsoft speech api used for speech recognition
engine.setProperty('volume', 2)
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# voices[0] --> male assistant voice
# voices[1] --> female assistant voice


# *** Loading the configurations ***
config = Config(RepositoryEnv(r"config\.env"))
USER = config('USER')
HOSTNAME = config('BOT')

# *** Starting & Stopping listening ***
listening = False
def start_listening():
    global listening
    listening = True
    print("Started Listening...")
def pause_listening():
    global listening
    listening = False
    print("Stopped Listening...")
keyboard.add_hotkey('ctrl+alt+v', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)

def say(text):
    try:
        print(f"Saying: {text}")
        engine.say(text)
        engine.runAndWait()
    except RuntimeError as e:
        if str(e) == "run loop already started":
            # Reset the engine to handle the issue
            engine.stop()
            engine.say(text)
            engine.runAndWait()


def greet_me():
    hour = datetime.now().hour

    if 6 <= hour < 12:
        say(f"Good Morning {USER}")
    elif 12 <= hour < 17:
        say(f"Good Afternoon {USER}")
    elif 17 <= hour < 21:
        say(f"Good Evening {USER}")
    # Add a slight delay before saying the hostname
    time.sleep(0.1)
    say(f"I am {HOSTNAME}. How may I assist you?")
    
def takeCommand():
    # global listening
    # if not listening:
    #     say("Listening is currently disabled. Press Ctrl+Alt+V to enable it.")
    #     return "None"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 0.5 # this will wait for the user to complete (by default = 0.8)
        r.energy_threshold = 300
        audio = r.listen(source,0,4)
        if not listening:
            return "None"
        try:
            print('Recognizing...')
            query = r.recognize_google(audio,language= "en-in")
            print(f"{USER} said: {query}\n")
            if 'open' in query:
                say(choice(random_text))
            return query
        except Exception as e:
            say("Sorry I couldn't understand, Can you please repeat?")
            return "None"

def alarm(query):
    # Write the alarm time to the alarmtext.txt file
    with open("src/alarmtext.txt", "w") as time_file:  # Use 'w' mode to overwrite
        time_file.write(query.strip())  # Write the time without leading/trailing spaces

    absolute_path = os.path.join(os.getcwd(), "src", "alarm.py")
    os.startfile(absolute_path)
    
if __name__ == '__main__':
    # say('Hello I am V Bot')
    # print(f"USER: {USER}, HOSTNAME: {HOSTNAME}")
    greet_me()
    while True:
        if not listening:
            say("Please enable listening by pressing Ctrl+Alt+V.")
            time.sleep(1)  # Adds a short delay before checking again
            continue    
        if listening:
                query = takeCommand().lower()
                if query != "None":
                    if "stop" in query or "exit" in query:
                        hour = datetime.now().hour
                        if (hour >= 21) or (hour < 6):
                            say("Good Night sir, take care!")
                        else:
                            say("Have a good day sir!")
                        break
                    elif "how are you" in query.lower():
                        say("I'm absolutely fine sir. What about you?")
                    elif "open command prompt" in query.lower():
                        say("Opening command prompt")
                        os.system('start cmd')
                    elif "open camera" in query.lower():
                        say("Opening camera")
                        sp.run('start microsoft.windows.camera:', shell=True)
                    elif "play youtube" in query.lower():
                        say(f"What do you want to play on YouTube {USER}?")
                        video = takeCommand().lower()                    
                        youtube(video)
                    elif "google" in query.lower():
                        say(f"What do you want to search on google {USER}?")
                        query = takeCommand().lower()
                        search_on_google(query)
                    elif "wikipedia" in query.lower():
                        say(f"What do you want to search on wikipedia {USER}?")
                        search = takeCommand().lower()
                        result = search_on_wikipedia(search)
                        say(f"According to wikipedia, {result}")
                        say(f"i am printing on terminal")
                        print(result)
                    elif "the time" in query.lower():
                        strfTime = datetime.now().strftime("%H:%M:%S")
                        say(f"The time is {strfTime}")
                        # hour = datetime.now().strftime("%H")
                        # min = datetime.now().strftime("%M")
                        # say(f"The time is {hour} bajke {min} minute")
                    elif "temperature" in query.lower():
                        # Use regex to extract the location from the query
                        match = re.search(r"temperature in ([\w\s]+)", query, re.IGNORECASE)
                        
                        if match:
                            location = match.group(1)  # Extract the location
                            search = f"temperature in {location}"
                            url = f"https://www.google.com/search?q={search}"

                            r = requests.get(url)
                            data = BeautifulSoup(r.text, "html.parser")
                            # Extract the temperature information
                            temp_element = data.find("div", class_="BNeawe")
                            
                            if temp_element:
                                temp = temp_element.text
                                say(f"The current temperature in {location} is {temp}")
                            else:
                                say("I'm sorry, I couldn't retrieve the temperature information. The webpage structure might have changed.")
                        else:
                            say("I'm sorry, I couldn't find a location in your query.")
                    elif "weather" in query.lower():
                        # Use regex to extract the location from the query                    match = re.search(r"weather in ([\w\s]+)", query, re.IGNORECASE)
                            
                        if match:
                            location = match.group(1)  # Extract the location
                            search = f"weather in {location}"
                            url = f"https://www.google.com/search?q={search}"
                            r = requests.get(url)
                            data = BeautifulSoup(r.text, "html.parser")
                            # Extract the temperature information
                            weather_element = data.find("div", class_="BNeawe")
                            
                            if weather_element:
                                weather = weather_element.text
                                say(f"The current weather in {location} is {weather}")                        
                            else:
                                say("I'm sorry, I couldn't retrieve the weather information. The webpage structure might have changed.")
                        else:
                            say("I'm sorry, I couldn't find a location in your query.")
                    elif "IP address" in query.lower():
                        ip_address = find_my_id()
                        say(f"Your I.P address is {ip_address}")
                        print(f"Your I.P address is {ip_address}")
                    elif "open" in query.lower():
                        from dict_app import openapp
                        openapp(query)
                    elif "close" in query.lower():
                        from dict_app import closeapp
                        closeapp(query)   
                    elif "set an alarm" in query.lower():
                        say("set the time")
                        alarm_time = input()
                        alarm(alarm_time)
                        say("done sir")
                    # todo: add a feature to play a specific song        
                    # # New condition for Spotify
                    # if "play" in query.lower() and "on spotify" in query.lower():
                    #     say("Opening Spotify, what singer would you like to listen to?")
                    #     artist = takeCommand().lower()
                    #     say(f"Playing {artist} on Spotify.")
                    #     # If you have a way to play the artist, use it here. This opens Spotify.
                    #     os.startfile("C:\\Users\\Vaibhav Tandon\\AppData\\Roaming\\Spotify\\Spotify.exe")  # Adjust this path
                    #     # Optionally, you can control playback with Spotify API here.          
                    time.sleep(0.5)  # Delay after each command execution
        else:
            say("Listening is currently disabled. Press Ctrl+Alt+V to enable it.")
            time.sleep(1)  # Adds a short delay before checking again