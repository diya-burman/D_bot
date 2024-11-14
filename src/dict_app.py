import os
import pyautogui #type: ignore
import pyttsx3
import webbrowser
import time
import re

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
            # Reset the engine to handle the issue
            engine.stop()
            engine.say(text)
            engine.runAndWait()

dictapp = {
    "command prompt": "cmd",
    "paint": "mspaint",  
    "word": "winword",
    "excel": "excel",
    "chrome": "chrome",
    "vscode": "code",
    "powerpoint": "powerpnt",
    "youtube": "https://youtube.com", 
    "lms": "https://lms.thapar.edu",  
    "personal mail": "https://mail.google.com/mail/u/0/#inbox",  
    "college mail": "https://mail.google.com/mail/u/1/#inbox",  
    "striver": "https://takeuforward.org",  
    "github": "https://github.com",  
    "leetcode": "https://leetcode.com",  
    "twitter": "https://x.com",  
    "google": "https://google.com",  
    "udemy": "https://udemy.com",  
    "youtube music": "https://music.youtube.com" ,
    "chat gpt": "https://chatgpt.com/"
}

def openapp(query):
    
    query = query.replace("open", "").strip()
    if ".com" in query or ".co.in" in query or ".org" in query:
        say(f"Opening {query}...")
        webbrowser.open(query)
    else:
        for app, website in dictapp.items():
            if app in query:
                say(f"Opening {app}...")
                # Open application if found
                os.system(f"start {dictapp[app]}")
                return
            
def closeapp(query):
    keys = list(dictapp.keys())
    found = False  # Flag to check if the application or website was found
        
    for app in keys:
        if app in query.lower():  # Use lower() for case-insensitive matching
            # Check if the app is a web service
            if app in ["youtube", "lms", "personal mail", "college mail", "striver", "github", "leetcode", "twitter", "google", "udemy", "youtube music"]:
                say(f"Closing the browser tab for {app}...")  # Announce closing tab
                # Try to activate the browser and close the tab
                # Focus on the browser (Chrome in this case)
                # Similar logic for other websites
                pyautogui.hotkey("alt", "tab")  # Switch to the browser
                time.sleep(0.5)  # Allow time for the switch
                pyautogui.hotkey("ctrl", "w")  # Close the corresponding tab
            else:
                # Attempt to close the application if it exists
                try:
                    os.system(f"taskkill /f /im {dictapp[app].split('/')[-1]}.exe")  # Close the application
                    say(f"Closing {app}...")
                except Exception as e:
                    say(f"Error closing {app}: {str(e)}")
            found = True
            break  # Exit the loop after closing the app/tab
    if not found:
        say("Application or website not found.")

        