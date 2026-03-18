import sys
from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import eel
import time


# Initialize OpenRouter client

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)


# Speak Function

def speak(text): 
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)

    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


# Listen Function

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening.....")
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)
    try:
        print("recognizing")
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said:{query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception:
        return ""
    return query.lower()


# Main Command Function

@eel.expose 
def allCommands(message=1):
    if message == 1:  
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        #  Stop command
        if "stop" in query or "exit" in query or "quit" in query:
            speak("Goodbye! Shutting down.")
            eel.close()
            sys.exit(0)

        #  Open apps
        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)
            eel.ShowHood()
            return  

        #  YouTube
        elif "on youtube" in query or "youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
            eel.ShowHood()
            return  

        #  WhatsApp / Mobile related commands only
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)

            if contact_no != 0:
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query:
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")

                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                    whatsApp(contact_no, query, message, name)

            else:
                speak("Sorry, that contact was not found.")

        else:
            #  General Question → AI Fallback
            completion = client.chat.completions.create(
                model="deepseek/deepseek-r1-0528-qwen3-8b:free",
                messages=[{"role": "user", "content": query}]
            )
            response = completion.choices[0].message.content
            print("LLM:", response)
            speak(response)
            eel.DisplayMessage(response)

    except Exception as e:
        print("error", e)

    eel.ShowHood()
