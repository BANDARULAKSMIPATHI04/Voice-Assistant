import tkinter as tk
from tkinter import Label, Frame, Button, scrolledtext 
import speech_recognition as sr
import pyttsx3
import threading 
from datetime import datetime,timedelta # Import the datetime and timedelta classes from the datetime module
import webbrowser
import pywhatkit as kit 
import wikipedia
from googlesearch import search
import os # Import the os module
import pygame
import math

# Define the name of the assistant
assistant_name = "Alexa"

 
# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# list available voices 
voices = engine.getProperty('voices')
# set the voice property to the desired voice
engine.setProperty('voice', voices[1].id)
    
def speak(text):
    print(f"Speaking: {text}") # Debugging statement
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:       
        label.config(text="Listening...", fg= "#00FF00") # Green text for listening state
        root.update()
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            label.config(text=f"You said: {command}",fg="#FFFFFF") # White text for user input 
            root.update()
            process_command(command.lower())
        except sr.UnknownValueError:
            label.config(text="Sorry, I didn't understand.", fg="#FF0000") # Red text for errors
        except sr.RequestError:
            label.config(text="API unavailable.", fg="#FF0000")
        except sr.WaitTimeoutError:
            label.config(text="No speech detected.", fg="#FF0000")
        root.update()

# Process the recognized command
def process_command(command):
    response = ""
    
    if "hello" in command:
        response = "Hello! How can I help you?"
    elif "your name" in command:
        response = "I am your voice assistant."
    elif "thank you" in command: # check if the command contains the phrases "thank you"
        response = "You're welcome! If you need anything else,just let me know."
    elif "time" in command: # check if the command contains the word "time" 
        now = datetime.now()
        response = now.strftime("The time is %H:%M:%S")
    elif "today" in command and "date" in command:
        now = datetime.now()
        response = now.strftime("Today's date is %B %d,%Y")     
    elif "tomorrow" in command and "date" in command:
        tomorrow = datetime.now() + timedelta(days=1)
        response = tomorrow.strftime("Tomorrow's date is %B %d,%Y")
    elif "tomorrow" in command and "day" in command:
        tomorrow = datetime.now()+ timedelta(days=1)
        response = tomorrow.strftime("Tomorrow is %A") 
    elif "yesterday" in command and "date" in command:
        yesterday = datetime.now() - timedelta(days=1)
        response = yesterday.strftime("Yesterday's date was %B %d,%Y")   
    elif "yesterday" in command and "day" in command:
        yesterday = datetime.now() - timedelta(days=1)
        response = yesterday.strftime("Yesterday was %A")
    elif "date" in command:
        now = datetime.now()
        response = now.strftime("Today is %B %d,%Y")
    elif "day" in command:
        now = datetime.now()
        response = now.strftime("Today is %A")
    elif "add" in command:
        numbers = [int(s) for s in command.split() if s.isdigit()]
        response = f"The sum of {numbers} is {sum(numbers)}"
    elif "subtraction" in command:
        numbers = [int(s) for s in command.split() if s.isdigit()]
        response = f"The difference of {numbers} is {numbers[0] - numbers[1]}"
    elif "multiply" in command:
        numbers = [int(s) for s in command.split() if s.isdigit()]
        response = f"The product of {numbers} is {numbers[0] * numbers[1]}"
    elif "divide" in command:
        numbers = [int(s) for s in command.split() if s.isdigit()]
        response = f"The quotient of {numbers} is {numbers[0] / numbers[1]}"
    elif "search" in command: 
        search_term = command.replace("search","")
        response = f"searching for {search_term}"
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
    elif "play" in command:
        song = command.replace("play","").strip()
        response = f"playing {song} on YouTube"
        kit.playonyt(song)
    elif 'search for' in command or 'google' in command:
      search_term = search_term.replace('search for','')
      search_term = search_term.replace('google', '')
      speak('searching for' + command)
      pk.search(command)
    elif"joke" in command:
        response = "why did the scarecrow win an award? Because he was outstanding in his field!"   
    elif "open" in command:
        if "chrome" in command:
            response = "Opening Google Chrome"
            os.system("start chrome")
        elif "notepad" in command:
            response = "Opening Notepad"
            os.system("start notepad")

        else:
            website = command.replace("open", "").strip()
            response = f"Opening {website} in browser"
            webbrowser.open(f"https://www.{website}.com")
    elif "news" in command:
        response = "Opening latest news."
        webbrowser.open("https://news.google.com/")
    elif "exit" in command:
        response = "Goodbye!"
        speak(response)
        root.destroy() 
    elif "tell me about" in command or "what is" in command:
        query = command.replace("tell me about", "").replace("what is", "").strip()
        response = get_wikipedia_summary(query)

    speak(response)
    response_text.insert(tk.END, f"\n{response}\n")
    response_text.yview(tk,END)    

def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That query is ambiguous. Here are some options: {e.options}"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any information on that topic."
    except Exception as e:
        return "An error occurred while fetching information."   


# UI elements
def create_ui(root):
    global label,response_text # Declare global variables        

def start_listening():
    threading.Thread(target=recognize_speech, daemon=True).start()

# Enhanced UI elements
def create_ui(root):
    main_frame = Frame(root, bg="#1E1E1E")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    title_label = Label(main_frame, text="Voice Assistant", font=("Helvetica", 24, "bold"), fg="#00FF00", bg="#1E1E1E")
    title_label.pack(pady=10) 

# Scrolled text for detailed responses
    response_text = scrolledtext.ScrolledText(main_frame, font=("Arial", 12), fg="#FFFFFF", bg="#282828", wrap=tk.WORD, height=8)
    response_text.pack(pady=10, fill=tk.X)

    label = Label(main_frame, text="Click the button & speak", font=("Arial", 14), fg="#FFFFFF", bg="#1E1E1E")
    label.pack(pady=10)

    btn = Button(main_frame, text="Speak", command=start_listening, font=("Arial", 14), bg="#00A86B", fg="#FFFFFF", padx=20, pady=10, bd=0)
    btn.pack(pady=10)

    close_btn = Button(main_frame, text="Close", command=root.destroy, font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", padx=10, pady=5, bd=0)
    close_btn.pack(pady=10)

    return main_frame, label, response_text

# GUI Setup
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("600x500") #increase the size of the window
root.configure(bg="#1E1E1E")  #Dark grey background

# create the UI elements FIRST 
main_frame, label, response_text = create_ui(root)

#Bind Escape key to close the window
root.bind("<Escape>", lambda event: root.destroy())

# Start the main event loop AFTER creating the UI elements
root.mainloop()


