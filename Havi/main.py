import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import pyjokes
import requests
from pytube import YouTube
import time
import pyautogui
import sys
import pyaudio
import re
import json
import openai
from pywikihow import search_wikihow
import PyPDF2
from bs4 import BeautifulSoup #pip install bs4  # for weather
import psutil
import api_key


# text to speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 180)
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)

# # Set OpenAI API key
openai.api_key = "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"
# completion = openai.Completion()


# Text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()




# To convert voice into text 
def takequery():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Vinay said: {query}")
        return query
    
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that. Could you please repeat?")
        return "none"
    except sr.RequestError:
        speak("Sorry, I'm having trouble accessing the recognition service.")
        return "none"
    


def get_video_details_and_download(url, download=True):
    try:
        yt = YouTube(url)
        print("Video Title: ", yt.title)
        print("Video Duration:", yt.length, "seconds")
        print("Video Resolution:", yt.streams.get_highest_resolution().resolution)
        print("Video Views: ", yt.views)
        print("\n Video Description: \n", yt.description)
        print("Video Published Date:", yt.publish_date)
        print("Video Author:", yt.author)

        file_size_bytes = yt.streams.get_highest_resolution().filesize
        file_size_mb = file_size_bytes / (1024 * 1024)
        print(f"Video_Size: {file_size_mb:.2f} MB")

        if download:
            video = yt.streams.get_highest_resolution()
            video.download()
        return yt.title, yt.length, yt.streams.get_highest_resolution().resolution, yt.views, yt.description, yt.publish_date, yt.author, file_size_mb
    except Exception as e:
        print(f"Error: {e}")
        return None

video_url = ""
video_details = get_video_details_and_download(url=video_url, download=True)
if video_details:
    title, duration_seconds, resolution, views, description, publish_date, author, file_size_mb = video_details


def wish():
    hour = int(datetime.datetime.now().hour)
   # tt = time.strftime("%I:%M %p")

    if hour>=0 and hour<=12:
        speak("Good Morning boss")
    elif hour>12 and hour<=18:
        speak("Good Afternoon boss")
    else:
        speak("Good Evening boss")
    speak("I am Havi Online and ready. please tell me how can i help you")

# PDF Reader
# def pdf_reader(filename,read_from_which_page_number = 0, startfile = True):
#     if startfile == True:
#         os.startfile(filename)
#     book = open(filename,"rb")
#     pdf_reader = PyPDF2.PdfReader(book)
#     pages = len(pdf_reader.pages)
#     print("Number of pages: ", pages)
#     page = pdf_reader.getPage(read_from_which_page_number)
#     text = page.extract_text()
#     book.close()
#     speak(text)
# print(pdf_reader(r"C:\Users\vinay\Downloads\Letter of Recommendation - 2.pdf",startfile = False))

def news():
    main_url = "https://newsapi.org/v2/everything?q=tesla&from=2024-01-23&sortBy=publishedAt&apiKey=310e14f800b4442096d200a0dcd19873"

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")

def img_gen(prompt, output_file):
    #API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    #API_URL =  "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-x1-base-1.0"
    API_URL = "https://api-inference.huggingface.co/models/ARDICAI/stable-diffusion-2-1-finetuned"

    headers = {"Authorization": f"Bearer {api_key.API_KEY}"}

    def command(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content
    
    image_bytes = command({
        "inputs": prompt,
    })

    with open(output_file, "wb") as f:
        f.write(image_bytes)

def send_email(to,subject, content):
    sender_email = "kommisettivinay07@gmail.com"
    password = "Vinayak@7"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(sender_email,password)
    message = f'Subject: {subject}\n\n{content}'
    server.sendmail(sender_email,to,message)
    server.close()


# def TaskExecution():
if __name__ == "__main__":
    wish()
    while True:
        query = takequery().lower()

        #Logic Building for tasks

        if "open query prompt" in query:
            os.system("start cmd")
        elif "hello" in query:
            speak("Hey Boss, may i help you something.")
        
        elif "how are you" in query or "how r u" in query:
            speak("i am fine sir what about you.")
        
        elif "also good" in query or "fine" in query:
            speak("That's great to hear from you")
        
        # elif "thank you" in query or "thanks" in query:
        #     speak("it's my pleasure sir")
        
        elif "who are you" in query:
            print("I am Havi personal assistant for Vinay")
            speak("I am Havi personal assistant for Vinay")
        
        elif "who created you" in query:
            print("I was created by 6 members named by vinayak, haritha, prudhvi, kaushal, akshay, ayushi")
            speak("I was created by 6 members named by Vinayak")
            speak("Haritha")
            speak("prudhvi")
            speak("kaushal")
            speak("akshay")
            speak("aayushi")
            
        elif "what's the time" in query:
                strTime = datetime.datetime.now().strftime("%H:%M")
                speak(f"Sir, the time is {strTime}")
        
        elif "wikipedia" in query:
            speak("Searching wikipedia")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences = 2)
            speak("According to wikipedia")
            speak(results)
            print(results)

        elif "download youtube video" in query:
            video_url = "https://www.youtube.com/watch?v=EsRyyJmO-u8" 
            get_video_details_and_download(video_url)

        # elif "generate description of the given image" in query:
        #     generate_image_descriptor()

        
        elif "open notepad" in query:
            speak("Launching notepad")
            pyautogui.hotkey('win')
            time.sleep(1)
            pyautogui.write('notepad')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            speak("What should i write")
            ab = takequery().lower()
            time.sleep(1)
            pyautogui.write(f"{ab}", interval = 0.1)
        
        elif "tell me the latest news" in query:
            news()
            
        elif "wait for sometime" in query:
            speak("ok boss i will be in sleep mode for 15 seconds")
            time.sleep(15)
        
        elif "just open google" in query:
            webbrowser.open("WWW.google.com")
        elif "open google" in query:
            speak("what should i search on google")
            cm = takequery().lower()
            webbrowser.open(f"{cm}")
        elif "open youtube" in query:
            webbrowser.open("WWW.youtube.com")
        elif "search on youtube" in query:
            speak("what should i search on youtube")
            qry = takequery().lower()
            kit.playonyt(f"{qry}")

        elif "generate image" in query or "generate an image" in query:
            speak("which image you want to generate give me some specifications you would like")
            qy = takequery().lower()
            img_gen(f"{qy}","img_gen.png")
            # image_list = generate_images("Angry cat chasing small rat in windy climate in fully developed city")


        elif "send mail" in query:
            try:
                speak("What should i send")
                content = takequery()
                to = ('vinayakkommisetti@gmail.com')
                speak("Subject to your mail!")
                subject = takequery()
                send_email(to,subject,content)
                speak("Email has been sent successfully")
            except Exception as e:
                speak("Sorry, there being an error to send email!")
                print(e)

            

        elif "close Microsoft edge" in query or "close msedge" in query:
            os.system("taskkill /f /im msedge.exe")
        elif "close chrome" in query:
            os.system("taskkill /f /im chrome.exe")
        
        elif "open excel" in query:
            cpath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk"
            speak("Launching excel")
            os.startfile(cpath)
        elif "open brave" in query:
            apath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Brave.lnk"
            speak("Launching brave")
            os.startfile(apath)
        
        elif "open powerpoint" in query:
            bpath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk"
            speak("Launching Power point")
            os.startfile(bpath)
        
        elif "close excel" in query:
            os.system("taskkill /f /im excel.exe")
        
        elif "close brave" in query:
            os.system("taskkill /f /im brave.exe")
        
        elif "close powerpoint" in query:
            os.system("taskkill /f /im powerpnt.exe")

        elif "open linkedIn" in query: # Not working
            webbrowser.open("WWW.linkedin.com")
        elif "open facebook" in query:
            webbrowser.open("WWW.facebook.com")
        elif "open instagram" in query:
            webbrowser.open("WWW.instagram.com")
        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam',img)
                k = cv2.waitKey(50)
                if k==27:
                    break
            cap.release()
            cv2.destroyAllWindows()
        elif "play music" in query:
                music_dir = "C:/Users/vinay/Music"
                songs = os.listdir(music_dir)
                for song in songs:
                    if song.endswith('.mp3'):
                         os.startfile(os.path.join(music_dir, song))
        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your Ip address is {ip}")
        elif "send message" in query:
            kit.sendwhatmsg("+919133075535","This is testing protocol",2,35)
        
        elif "read pdf" in query:
            pdf_reader()
        


# To close any application
        elif "close notepad" in query:
            speak("Okay sir, closing notepad")
            os.system("taskkill /f /im notepad.exe")

 # To set an alarm
        elif "set alarm" in query:
            nn = int(datetime.datetime.now().hour)
            if nn == 16:
                alarm_dir = 'C:\\Users\\vinay\\Alarm'
                alarms = os.listdir(alarm_dir)
                os.startfile(os.path.join(alarm_dir,alarms[0]))
        
        elif "volume up" in query or "increase volume" in query:
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            

        elif "volume down" in query or "decrease volume" in query:
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")

        
        elif "volume mute" in query or "mute volume" in query or "mute" in query:
            pyautogui.press("volumemute")
                     
                
        elif "take screenshot" in query or "take a screenshot" in query or "capture the screen" in query:
                speak("By what name do you want to save the screenshot?")
                name = takequery().lower()
                speak("Alright sir, taking the screenshot")
                img = pyautogui.screenshot()
                name = f"{name}.png"
                img.save(name)
                speak("The screenshot has been succesfully captured")

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
        
        elif "shutdown the system" in query:
            os.system("shutdown /r /t 5")
        
        elif "restart the system" in query:
            os.system("shutdown /r /t 5")
        
        # elif "sleep the system" in query:
        #     os.system("rundll132.exe powrprof.dll, SetSuspendState 0,1,0")
        
        elif "change the window" in query: # Not working
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

 
# How to do mode
        elif "activate how to do mod" in query:
            speak("How to do mode is activated")
            while True:
                speak("Please Tell me what you want to know")
                how = takequery()
                try:
                    if "exit" in how or "close" in how:
                        speak("Ok boss, how to do mode is closed")
                        break
                    else:
                        max_results = 1
                        how_to = search_wikihow(how,max_results)
                        assert len(how_to) == 1
                        how_to[0].print()
                        speak(how_to[0].summary)
                except Exception as e:
                    speak("Sorry sir, i am not able to find this")
        
# Battery Percentage
        elif "how much power left" in query or "what's the battery percentage" in query:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f"sir our system have {percentage} percent battery")
            if percentage >= 75:
                speak("we have enough power to continue our work")
            elif percentage >= 40 and percentage <= 75:
                speak("we should connect our system to charging point to charge our battery")
            elif percentage >= 15 and percentage <= 30:
                speak("we dont have enough power to work, please plug in the charger")
            elif percentage <= 15:
                speak("we have very low power, please plug in the charger otherwise the system will automatically shut down")
        
                
        elif "no thanks" in query:
            speak("Thank You sir have a great day")
            sys.exit()
        elif "exit" in query:
            speak("Thank You boss , have a nice day")
            sys.exit()

        elif "thanks for helping" in query:
            speak("It's my pleasure sir, Hope you enjoy the music")
            speak("Signing off ")
            webbrowser.open("https://www.youtube.com/watch?v=_4kHxtiuML0")
            sys.exit()
            # speak("sir, do you have any other work")
            
        elif "temperature" in query:
            search = "temperature in punjab"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div",class_="BNeawe").text
            speak(f"Current {search} is {temp}")
        
        



# if __name__ == "__main__":
#     #speak("Hey Vinay")
#     while True:
#         permission = takequery()
#         if "wake up" in permission:
#             TaskExecution()
#         elif "goodbye" in permission:
#             sys.exit()