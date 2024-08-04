import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
from googlesearch import search
import requests
from bs4 import BeautifulSoup

listener = sr.Recognizer()
machine = pyttsx3.init()

def talk(text):
    """Make Jarvis speak the provided text."""
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    """Capture and process voice instruction from the user."""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            instruction = listener.recognize_google(voice)
            instruction = instruction.lower()
            if "jarvis" in instruction:
                instruction = instruction.replace('jarvis', '')
                print(instruction)
    except Exception as e:
        print("Error:", e)
        instruction = ''
    return instruction

def extract_text_from_url(url):
    """Extract meaningful text from a webpage given its URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')

        content = ' '.join([para.text for para in paragraphs[:3]])  
        if content:
            return content
        else:
            return "I couldn't find any information on that page."
    except Exception as e:
        print("Error while extracting text from URL:", e)
        return "I'm having trouble retrieving information from the web."

def search_google(query):
    """Perform a Google search and return informative content."""
    try:
        search_results = search(query, num_results=1)
        for url in search_results:
            return extract_text_from_url(url)
        return "I couldn't find any information on that."
    except Exception as e:
        print("Error while searching Google:", e)
        return "I'm having trouble connecting to the internet."

def play_jarvis():
    """Main function to process instructions and perform tasks."""
    instruction = input_instruction()
    if not instruction:
        talk("I didn't catch that. Please say it again.")
        return

    print("Instruction:", instruction)
    if "play" in instruction:
        song = instruction.replace('play', '')
        talk("Playing " + song)
        pywhatkit.playonyt(song)
    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date is " + date)
    elif 'how are you' in instruction:
        talk('I am good, how are you?')
    elif 'what is your name' in instruction:
        talk('I am Jarvis, what can I do for you?')
    elif 'who is' in instruction:
        person = instruction.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    else:
        talk('Let me search that for you.')
        answer = search_google(instruction)
        print("Informative Result:", answer)
        talk(answer)

play_jarvis()
