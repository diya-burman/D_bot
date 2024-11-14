import pyttsx3
from datetime import datetime
import os
import time 
from playsound import playsound #type: ignore
engine = pyttsx3.init('sapi5') 
engine.setProperty('volume', 2)
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def say(text):
    try:
        print(f"Saying: {text}")
        engine.say(text)
        engine.runAndWait()
    except RuntimeError as e:
        if str(e) == "run loop already started":
            engine.stop()
            engine.say(text)
            engine.runAndWait()

def read_alarm_time():
    # Read alarm time from the file
    with open("alarmtext.txt", "rt") as extractedTime:
        time = extractedTime.read().strip()
    return time

def clear_alarm_file():
    # Clear the contents of alarm file
    with open("alarmtext.txt", "r+") as deleteTime:
        deleteTime.truncate(0)

def ring(alarm_time):
    print(f"Alarm is set for {alarm_time}.")
    while True:
        currTime = datetime.now().strftime("%H:%M:%S")
        if currTime == alarm_time:
            say("Alarm ringing")
            # Use playsound to play the music
            playsound("src/music.mp3")  # Ensure the path is correct
            break  # Exit after the alarm rings
        time.sleep(1) 