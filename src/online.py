import requests
import wikipedia
import pywhatkit as kit # type: ignore

def find_my_id():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address("ip")

def search_on_wikipedia(query):
    result = wikipedia.summary(query, sentences=2)
    return result

def search_on_google(query):
    kit.search(query)

def youtube(video):
    kit.playonyt(video)