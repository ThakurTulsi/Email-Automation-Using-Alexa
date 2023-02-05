# STEP 1: importing libraries
from datetime import datetime
from imaplib import Commands
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests, json, sys
import smtplib  
from email.message import EmailMessage


# pyAudio
# pyjokes
# pywhatkit
# wikipedia
# openweatherapi

listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices') 
voices = engine.setProperty('voice', voices[1].id)

def engine_talk(text):
    engine.say(text)
    engine.runAndWait()

def weather(city):
    # Enter your API Key here
    api_key = "insert-your-api-key"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # give city name
    city_name = city

    # complete url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # now x contains list of nested dictionaries
    # check the value of "cod" key is equal to
    # "404", means city is found otherwise
    # city is not found
    if x["cod"] != "404":

        # store the value of main
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding to the vale of "pressure" key of y
        # current_pressure = y["pressure"]

        # store the value corresponding to the value of "humidity" key of y
        # current_humidity = y["humidity"]


        # store the value of "weather" key in variable z
        # z = x["weather"]

        # store the value corresponding to "description" key at the 0th index of z
        # weather_description = z[0]["description"]
        # current_temperature = (current_temperature-32)*5/9
        # current_temperature = int(current_temperature)
        # current_temperature = 28
        return str(current_temperature)


def user_commands():
    try: 
     with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=1)
        
        print("Start Speaking...")
        
        voice = listener.listen(source)
        command = listener.recognize_google(voice, language='en-US')
        command = command.lower()
        if 'alexa' in command:
            command = command.replace('alexa', '')
            print('Me:'+command)
    except:
     pass     
    return command    


def send_email(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587) #smtp.gmail.com is server name and 587 is port number like a door
    server.starttls() #tls means transport layer security
    server.login('abc@gmail.com', 'your-passkey')
    email = EmailMessage()
    email['From'] = 'abc@gmail.com'
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(message)
    server.send_message(email)
    # server.sendmail('abc@gmail.com', , 'Hey there! Make sure you join the meeting tomorrow. Thanks')


email_list = { 
    'myself':'abc@gmail.com',
    'team':'def@gmail.com',
    'classmate':'ghi@gmail.com',
    'sister':'jkl@gmail.com', 
    'manager': 'mno@gmail.com',
    'test': 'pqr@gmail.com'
}


def run_alexa():
    command  =  user_commands()
    if 'play' in command:
        song = command.replace('play', '')
        print('Alexa: playing'+song)
        engine_talk('playing' +song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        command = command.replace('alexa','')
        time = datetime.datetime.now().strftime('%I:%M:%p')
        print('Alexa: The current time is '+time)
        engine_talk('The current time is'+time)

    elif 'who is' in command:
        name = command.replace('who is','')
        # print('Me: who is'+name)
        info = wikipedia.summary(name, 1)
        print('Alexa: '+info)
        engine_talk(info)



    elif 'email' in command:
        engine_talk('To whom you want to send message')
        name =  user_commands()
        receiver = email_list[name]
        print(receiver)    
        engine_talk('What is the subject of your email?')
        subject =  user_commands()
        engine_talk('Please tell me the text of your email')
        message = user_commands()
        send_email(receiver, subject, message)
        print('Hey user, your email has been successfully sent')
        engine_talk('Hey user, your email has been successfully sent')

    elif 'what is' in command:
        name = command.replace('what is','')
        # print('Me: who is'+name)
        info = wikipedia.summary(name, 1)
        print('Alexa: '+info)
        engine_talk(info)    

    elif 'joke' in command:
        joke= pyjokes.get_joke()
        print('Alexa: '+joke)
        engine_talk(joke)

    elif 'weather' in command:
        engine_talk('Please tell name of Place')
        city = user_commands()
        # weather_api = weather('India') 
        weather_api = weather(city)
        print('Alexa: The weather in '+city+' is'+weather_api+ ' degree farenheit') 
        engine_talk('The weather in'+city+'is'+weather_api + 'degree farenheit') 

    elif 'intelligent'  in command:
        string='I know, I was born smart'
        print('Alexa: ' +string)   
        engine_talk(string)

    elif 'stop' in command:
        print('Alexa: Okay, Good bye')
        engine_talk('Okay, Good Bye')
        sys.exit()



    else:
        engine_talk('Sorry, I could not hear you properly')
       


while True:
    run_alexa()                   
