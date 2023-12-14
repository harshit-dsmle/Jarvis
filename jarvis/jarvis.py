import datetime
import json
import os
import smtplib
import subprocess
import sys
import time
import webbrowser
from difflib import get_close_matches
from time import sleep
from urllib.request import urlopen

import psutil
import pyautogui
import pyjokes
import pyttsx3
import pywhatkit
import random2
import requests
import screen_brightness_control as sbc
import speech_recognition as sr
import wikipedia
import winshell
from bs4 import BeautifulSoup as soup
from requests import get
from twilio.rest import Client
from win10toast import ToastNotifier

import talkdata as td
from program_paths import p_paths

engine = pyttsx3. init()
voices = engine.getProperty('voices')
# print(voices[0].id
engine.setProperty('voice', voices[0].id)


bot_name = "jarvis"
mozila_path='"C:\\Program Files\\Mozilla Firefox\\firefox.exe" %s'
toast=ToastNotifier()    

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def takecommands():
    query = str(input("type here  "))
    return query

#To convert voice into text
def  takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source , duration=0.2)
        audio = r.listen(source, phrase_time_limit=30)

    try:
        print("recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")

    except Exception:
        print("said nothing")
        return"none"
    return query


def check_name():
    query = takecommand().lower()
    if (bot_name) in query:
        query = query.replace(bot_name, "")
        query = query.lstrip(' ')
        query = query.rstrip(' ')
        return query

    else:
        return ("none")

#for news headlines
def news():
    news_url="https://news.google.com/news/rss"
    client=urlopen(news_url)
    xml_page=client.read()
    client.close()

    soup_page=soup(xml_page,"xml")
    news_list=soup_page.findAll("item")
    newslimit=5
    # read news title
    for news in news_list:
        speak(news.title.text)
        print(news.title.text)
        print("-"*60)
        newslimit=newslimit-1
        if newslimit==0:
            return


#To wish
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        return("good morning")
    elif hour>=12 and hour<18:
        return("good afternoon")


    else:
        return("good evening")

#to send email
def sendemail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.ehlo()
    server.login('dipendrasinghchouhan2003@gmail.com', '[#chuchu007]')
    server.sendmail('dipendrasinghchouhan2003@gmail.com', to, content)
    server.close

#To translate
def translate(word):
    data = json.load(open('data.json'))
    word = word.lower()
    if word in data:
        speak(data[word])
    elif len(get_close_matches(word, data.keys())) > 0:
        x = get_close_matches(word, data.keys())[0]
        speak('Did you mean ' + x +
        ' instead,  respond with Yes or No.')
        ans = takecommand().lower()
        if 'yes' in ans:
            speak(data[x])
        elif 'no' in ans:
            speak("Word doesn't exist. Please make sure you spelled it correctly.")
        else:
            #changed from we to I
            speak("I did not understand your entry.")

    else:
        speak("Word doesn't exist. Please double check it.")

#Close apps
def close_app(app_name):
    running_apps=psutil.process_iter(['pid','name']) #returns names of running processes
    found=False
    for app in running_apps:
        sys_app=app.info.get('name').split('.')[0].lower()

        if sys_app in app_name.split() or app_name in sys_app:
            pid=app.info.get('pid') #returns PID of the given app if found running
            
            try: #deleting the app if asked app is running.(It raises error for some windows apps)
                app_pid = psutil.Process(pid)
                app_pid.terminate()
                found=True
            except:
                pass
            
        else:
            pass
    if not found:
        speak(app_name+" not found running Sir")
    else:
        speak(app_name+' closed Sir')

def you_tube(query):
    speak("opening youtube...")
    query = query.replace("open youtube ","")
    query = query.lstrip(' ')
    web = "https://www.youtube.com/results?search_query="+query
    webbrowser.open(web)
    speak("done")

#To play music
def play_music():
    speak("ok i am playing music to freshup your mood")
    music_dir = "C:\\Users\\Admin\\Music"
    songs = os.listdir(music_dir)
    song=random2.choice(songs)
    os.startfile(os.path.join(music_dir, song))

#Weather
def wea_ther():
    # Google Open weather website
    # to get API of Open weather
    api_key = "93a80005c31cd8ef59c11ad2d32fe8f1"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak(" City name ")
    city_name=takecommand()
    complete_url = (base_url+"appid="+api_key+"&q="+city_name)
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = round(y["temp"] -273.15)
        current_pressure = y["pressure"] * 0.0295
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        print("current Temperature in" + city_name +" is" + str(current_temperature)+ " degree celcius " + " \n atmospheric pressure in"+ city_name+ " is" + str(current_pressure)+" inches of mercury" + " \n humidity in"+ city_name+ " is"+ str(current_humidiy)+" percent" + " the weather in" + city_name + " will be" + str(weather_description))
        speak("current Temperature in" + city_name +" is" + str(current_temperature)+ " degree celcius " + " \n atmospheric pressure in"+ city_name+ " is" + str(current_pressure)+" inches of mercury" + " \n humidity in"+ city_name+ " is"+ str(current_humidiy)+" percent" + " the weather in" + city_name + " will be" + str(weather_description))

    else:
        speak(" City Not Found ")




#*********************************************MAIN PROGRAM***********************************************************#
if __name__ == '__main__':
    toast.show_toast("Jarvis","welcome back sir", icon_path='notification.ico') 
    wish_say=wish()
    speak(wish_say+" sir")
    speak("welcome back")
    speak("Jarvis here, how can i help you")
    while True:


        query = check_name()

        #logic building for tasks

        if "none" in query:
            continue

        elif (len(query) == 0):
            speak("i am here sir , tell me what can i do for you")

        # To open apps
        elif "open notepad" in query:
                speak("opening notepad")
                location = "C:/WINDOWS/system32/notepad.exe"
                notepad = subprocess.Popen(location)

        elif "close notepad" in query:
                speak("closing notepad")
                notepad.terminate()

        elif ("open ms word") in query:
            speak("opening ms word")
            location="C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
            word=subprocess.Popen(location)

        elif ("close ms word") in query:
            speak("closing ms word")
            word.terminate()

        elif "open cmd" in query:
            speak("ok wait a moment i am opening command prompt")
            os.system("start cmd")

        elif("open task manager") in query:
            pyautogui.hotkey('ctrl', 'shift', 'esc')

        #To open apps
        elif ("launch") in query:
            query=query.replace("launch" , "")
            query=query.replace(" " ,"")
            location = p_paths.get(query)
            subprocess.Popen(location)
            speak(query+" opened sir")       

        #To close programs
        elif ("close") in query:
            query=query.replace("close" , "")
            query=query.replace(" " ,"")
            close_app(query)


        #To open camera
        elif "open camera" in query:
            speak("ok i am opening camera and you make sure that you'r looking osm for a shoot")
            os.system("start microsoft.windows.camera:")
            os.close()

        #To play music 
        elif "play music" in query:
            play_music()


        elif "what is the time now" in query:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print(current_time)
            speak(f"the time is {current_time}")

        #To show ip address
        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"your IP address is {ip}")

        #wikipedia search
        elif "wikipedia" in query:
            speak("searching from wikipedia...")
            query = query.replace("wikipedia","")
            query = query.replace("on","")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            speak(results)
            # print(results)

        #youtube search
        elif "open youtube" in query:
            you_tube(query)

        elif ("play" and "youtube") in query:
            query = query.replace("play","")
            query = query.replace("youtube","")
            query = query.replace(" on ","")
            speak("playing"+ query + "on youtube")
            pywhatkit.playonyt(query)

        #google search    
        elif "search" in query:
            query = query.lstrip(' ')
            query = query.rstrip(' ')
            if len(query)==6:
                speak("what should i search")
                query=takecommand().lower()
                speak("searching"+query+" "+"on Firefox")
                pywhatkit.search(query)
                speak("done sir")

            else:
                query = query.replace("search", "")
                print(query)
                speak("searching"+query+" "+"on Firefox")
                pywhatkit.search(query)
                speak("done sir")

        elif 'open stack overflow' in query:
            speak("Here you go to Stack Over flow, Happy coding")
            webbrowser.get(mozila_path).open("stackoverflow.com")

        elif "open google" in query:
            speak("ok what would you like to search on google")
            cm = takecommand().lower()
            webbrowser.open(f"{cm}")

        #empty recycle bin
        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak("Recycle Bin Recycled")

        #news
        elif 'news' in query:
            news()

        #whatsapp messege            
        elif "whatsapp message" in query:
            speak("tell me the phone number")
            phone = takecommand()
            ph = '+91' + phone
            speak("tell me the message")
            msg = takecommand()
            speak("tell me the time")
            speak("time in hour")
            hour = int(takecommand())
            speak("time in minutes")
            min = int(takecommand())
            pywhatkit.sendwhatmsg(ph,msg,hour,min,20)
            speak("ok sending whatsapp message")

        #jokes
        elif "joke" in query:
            a=random2.choice(pyjokes.get_jokes())
            speak(a)


        #system commands     
        elif "logout" in query:
            speak('logging out in 5 second')
            sleep(5)
            os.system("shutdown - l")

        elif "shutdown" in query:
            speak('shutting down in 5 second')
            sleep(5)
            os.system("shutdown /s /t 1")

        elif "restart" in query:
            speak('restarting in 5 second')
            sleep(5)
            os.system("shutdown /r /t 1")

        #email commands
        elif "email to harshit" in query:
            try:
                speak("what should i say")
                content=takecommand().lower()
                to="harshitlp2001@gmail.com"
                sendemail(to, content)
                speak("email has been sent to harshit")

            except Exception as e:
                print(e)
                speak("sorry sir i cant able to send this email")

        elif "email to shivangi" in query:
            try:
                speak("what should i say")
                content=takecommand().lower()
                to="shivangi.srivastava2020@vitbhopal.ac.in"
                sendemail(to,content)
                speak("email has been sent sir")

            except Exception as e:
                print(e)
                speak("sorry sir i cant able to send this email")

        elif "email to harshit goswami" in query:
            try:
                speak("what should i say")
                content=takecommand().lower()
                to=("harshit.goswami2020@vitbhopal.ac.in")
                sendemail(to,content)
                speak("email has been sent")

            except Exception as e:
                print(e)
                speak("sorry sir i cant able to send this email")

        elif "email to divyansh" in query:
            try:
                speak("what should i say")
                content=takecommand().lower()
                to=("divyansh.mittal2020@vitbhopal.ac.in")
                sendemail(to,content)
                speak("email has been sent")

            except Exception as e:
                print(e)
                speak("sorry sir i cant able to send this email")

        elif "email to paras sir" in query:
            try:
                speak("what should i say")
                content=takecommand().lower()
                to="paras.jain@vitbhopal.ac.in"
                sendemail(to,content)
                speak("email has been sent sir")

            except Exception as e:
                print(e)
                speak("sorry sir i cant able to send this email")

        elif "send email" in query:
            try:
                speak("what should i say")
                content=takecommand().lower()
                speak("whom should i send sir please type")
                to=input(str("type email id"))
                sendemail(to,content)
                speak("email has been sent sir")

            except Exception as e:
                print(e)
                speak("sorry sir i cant send this mail")

        #location finder
        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.co.in/maps/place/"+location+"")

        #whether forecast
        elif "weather" in query:

            # Google Open weather website
            # to get API of Open weather
            api_key = "93a80005c31cd8ef59c11ad2d32fe8f1"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak(" City name ")
            city_name=takecommand()
            complete_url = (base_url+"appid="+api_key+"&q="+city_name)
            response = requests.get(complete_url)
            x = response.json()

            if x["cod"] != "404":
                y = x["main"]
                current_temperature = round(y["temp"] -273.15)
                current_pressure = y["pressure"] * 0.0295
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                print("current Temperature in" + city_name +" is" + str(current_temperature)+ " degree celcius " + " \n atmospheric pressure in"+ city_name+ " is" + str(current_pressure)+" inches of mercury" + " \n humidity in"+ city_name+ " is"+ str(current_humidiy)+" percent" + " the weather in" + city_name + " will be" + str(weather_description))
                speak("current Temperature in" + city_name +" is" + str(current_temperature)+ " degree celcius " + " \n atmospheric pressure in"+ city_name+ " is" + str(current_pressure)+" inches of mercury" + " \n humidity in"+ city_name+ " is"+ str(current_humidiy)+" percent" + " the weather in" + city_name + " will be" + str(weather_description))

            else:
                speak(" City Not Found ")

        elif "send message " in query:
                # You need to create an account on Twilio to use this service
                account_sid = 'AH8q3dGK2f2vLZVgbRfLTjQPySe2yRaJHs'
                auth_token = '152b437a0bb91a115d0485a248290822s'
                client=Client(account_sid, auth_token)

                message = client.messages \
                                .create(
                                    body = takecommand(),
                                    from_='Sender No',
                                    to ='Receiver No'
                                )

                print(message.sid)

        #remember
        elif "write a note" in query:
            speak("What should i write, sir")
            note = takecommand()
            file = open('jarvis.txt', 'w')
            speak("Sir, Should i include date and time")
            snfm = takecommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
                speak("note has been saved sir")
            else:
                file.write(note)
                speak("notes has been saved sir")
        
        elif "show note" in query:
            speak("Showing Notes")
            file = open("jarvis.txt", "r")
            print(file.read())
            speak(file.read(6))

        #basic talks
        elif ("how are you jarvis") in query:
            speak("i am fine what about you")


        elif ("i like your name jarvis") in query:
            speak("thanks that's so nice to hear")

        elif ("do you like your name") in query:
            speak("yes i like my name very much")

        elif ("who makes you") in query:
            speak("i was made by a team of some students from V I T institute ")

        elif ("what is your working") in query:
            speak("i work similar as google assistant but i have a speacial characteristic that i can work on offline mode to make it convenient and easier for you")

        elif ("hello jarvis") in query:
            speak("hey nice to hear your voice hows your day")

        elif ("what is your name") in query:
            speak("Did I forget to introduce myself")
            speak("I am your jarvis, personal assistant")

        elif ("your birthday") in query:
            speak("I try to live every day like its my birthday ,I get more cake that way")

        elif ("are you a robot") in query:
            speak("I would prefer to think of myself as your friend, Who also happens to be artificially intelligent")

        elif ("what about yours day how is it") in query:
            speak("its splendid that i am talking to you let me know if there is anything i can do for you")

        #shutdown command
        elif ("goodbye" or "good bye") in query:
            speak("Thanks For Your Time, Good Bye!")
            sys.exit()

        #brightness features
        elif ("set brightness") in query:
            current_brightness = sbc.get_brightness()
            speak("current brightness level is")
            speak(current_brightness)
            speak("At what level of brightness should I do sir?")
            new_brightnes = int(takecommand().lower())
            sbc.set_brightness(new_brightnes)
            speak("brightness set to level")
            speak(new_brightnes)

        elif ("decrease brightness") in query:
            current_brightness = sbc.get_brightness()
            speak("current brightness level is")
            speak(current_brightness)
            new_brightnes = current_brightness - 10
            sbc.set_brightness(new_brightnes)
            speak("brightness set to level")
            speak(new_brightnes)

        elif ("increase brightness") in query:
            current_brightness = sbc.get_brightness()
            speak("current brightness level is")
            speak (current_brightness)
            new_brightnes = current_brightness + 10
            sbc.set_brightness(new_brightnes)
            speak("brightness set to level")
            speak(new_brightnes)

        #Dictionary for you
        elif 'dictionary' in query:
            speak('What you want to search in your intelligent dictionary?')
            translate(takecommand())

        elif ("voice") and ("female") in query:
            engine.setProperty('voice', voices[1].id)
            bot_name = "friday"
            speak("Hello Sir, I have switched my voice")

        elif ("voice") and ("male") in query:
            engine.setProperty('voice' , voices[0].id)
            bot_name = "jarvis"
            speak("Hello Sir, I have switched my voice")

        elif query in td.a_goodgreet:
            if wish_say == query:
                speak(wish_say + " sir")

            else:
                speak("its"+ wish_say.replace("good","") +" sir")

        #---------------------------pyautogui features--------------#
