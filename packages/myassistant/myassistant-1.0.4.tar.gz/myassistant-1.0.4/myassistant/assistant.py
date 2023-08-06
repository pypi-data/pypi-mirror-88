import speech_recognition as sr
import pyttsx3
import os
from datetime import datetime
import psutil
from time import sleep
import platform
import webbrowser
import wikipedia
import random
import requests
import smtplib
from prettytable import PrettyTable
import sounddevice as sd 
from scipy.io.wavfile import write 
import wavio as wv 
  



#this function will print all the commands
def show():
    table = PrettyTable()
    table.field_names=["commands","works"]
    table.add_row(["more information ","you will find on (code with govind) youtube channel"])
    table.add_row(["----------------","------------------------------------------------------"])
    table.add_row(["show me commands","Will show you all commands"])
    table.add_row(["check battery percentage","Will tell real time battery percentage of your system"])
    table.add_row(["system details","Will tell the system specification"])
    table.add_row(["open youtube","start youtube and also ask for search query before opening youtube"])
    table.add_row(["open google","start google and also ask for search query before opening google"])
    table.add_row(["open wikipedia","collect information from wikipedia according to given query and save it in a .txt file (initial path is current working dir..) can be change"])
    table.add_row(["latest news","Will collect bcc news by the help of new API and stored in a .txt file in the give path (initial path is current working dir..) can be change"])
    table.add_row(["open editor","start the code editor if give else it will not work"])
    table.add_row(["i want to mail","can mail someone (to given mails) more information on youtube(code with govind)"])
    table.add_row(["record voice"," Will start recording voice initial time is 10 second (can we change)"])
    table.add_row(["open textarea"," Will open textarea.pythonanywhere.com must visit guys you will find many of things :)"])
    table.add_row(["what's the time","will tell you the current time"])
    table.add_row(["wait","this command will mute the programme for given seconds (initial seconds are 10 )"])
    table.add_row(["exit","this command will kill the the programme"])
    print(table)

class Assistant:        
    name = "user" #By default name is user
    voice = "male" #By default voice version is male   
    path = os.getcwd() #Diractory to save file . By default it's current working dir.
    wait =10 #seconds to wait
    duration = 10 #initial recording time is 10 seconds
    code = None #name of code editor
    mails={} #mails name with their email address
    my_mail = None #your email address and it should be less secured on becuase it use SMTP (python module)
    my_password = None #your password 
    
    def __init__(self):
        show()

    #this method for main use
    def speech_to_text(self):
        self.energy_threshold = 350  
        self.dynamic_energy_ratio = 10
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            listen = r.listen(source)
        print("Recognizing...")
        try:
            text = r.recognize_google(listen,language='en-IN')
            print(f"user said : {text}")
            return text.lower()
        except Exception:
            return "cant undersand"
    
    #this method is for searching purpose only becouse it returns None and we act according to it for searching 
    def speech_to_text_for_social(self):
        self.energy_threshold = 350  
        self.dynamic_energy_ratio = 10
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("what you want to search Listening....")
            listen = r.listen(source)
        print("Recognizing...")
        try:
            text = r.recognize_google(listen,language='en-IN')
            print(f"user said : {text}")
            return text.lower()
        except Exception:
            return None
        

    def text_to_speech(self,audio):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')        
        if self.voice  == 'female':
            engine.setProperty('voice',voices[1].id)
        else:
            engine.setProperty('voice',voices[0].id)
        engine.say(audio)
        engine.runAndWait()
        return 
    
    def wish(self):
        txt = "  How can i help you  "
        time = int(datetime.now().strftime("%H"))
        if(time>=0 and time<12):
            return f"good morning {self.name}  {txt}"
        elif (time>=12 and time<17):
            return f"good afternoun {self.name}  {txt}"    
        elif (time>=17 and time<24):
            return f"good evening {self.name}  {txt}"
        else:
            return 

    #return all commands related to this module
    def commnad(self):
        show()
        return 
        
    #return real time battery percentage
    def battery(self):
        b_t_r_y = psutil.sensors_battery()
        percent = str(b_t_r_y.percent)
        return percent

    def platform_info(self):
        txt = []
        system = platform.system()
        txt.append(f"the system is {system}")
        version = platform.version()
        txt.append("the version is " + version)
        processor = platform.processor()
        txt.append(f"the processor is {processor}")
        architecture = platform.architecture()[0]
        txt.append("the architecture is " + architecture)
        return txt
    
    def youtube(self,search):
        r = f"https://www.youtube.com/results?search_query={search}"
        webbrowser.open(r)
        return 

    def google(self,search):
        r = f"https://www.google.com/search?q={search}"
        webbrowser.open(r)
        return 

    def wiki_pedia(self,search):
        
        try:
            no = random.randint(1,100)
            data = wikipedia.summary(search)
            with open(f"{path}/{search}{no}.txt","w") as f:
                f.write(data)
            return True
        except Exception:
            return False

    def waiting(self):
        sleep(self.wait)
        return 

    def news(self):
        try:
            url = ('http://newsapi.org/v2/top-headlines?'
                'sources=bbc-news&'
                'apiKey=57518eb1c8d74766a4e953cd9afa05cd')
            response = requests.get(url)
            data = response.json()
            file_name = f"{self.path}/new_paper_{random.randint(0,1000)}.txt"

            for i in range(0,data['totalResults']):
                with open(file_name,"a") as f:
                    f.write(f"Tital : {data['articles'][i]['title']}\nPublish Date : {data['articles'][i]['publishedAt']}\nurl : {data['articles'][i]['url']}\nDescription : {data['articles'][i]['description']}\nContent : {data['articles'][i]['content']}\n\n\n")
            return [True,file_name]    
        except Exception:
            return False

    def code_editor(self):
        if self.code != None:
            try:
                os.system(f" start {self.code}")
                return "done"
            except Exception:
                return "try to open but unable to do it sorry"
        else:
            return "code editor path is not given"            
    
    def return_time(self):
        hour = int(datetime.now().strftime("%H"))
        minute = int(datetime.now().strftime("%M"))
        if hour<12:
            return [hour,minute,"AM"]
        elif hour>=12 and hour<13:
            return [12,minute,"PM"]
        else:
            hour = hour-12
            return [hour,minute,"PM"]
        
    def mail_to(self,to,content):
        try:
            subject = "this email is generated from code"
            subject_content=f'Subject : {subject}\n\n{content}'
            server=smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.login(self.my_mail,self.my_password)
            server.sendmail(self.my_mail,to,subject_content)
            server.close()
            return "mail sended"
        except Exception:
            return "Exception occures may be your less secure is not on for your given email address please cheack"

    def voice_recoder(self):   
        try:
            freq = 44100  
            # Start recorder with the given values  
            # of duration and sample frequency 
            recording = sd.rec(int(self.duration * freq),samplerate=freq, channels=2) 
            # Record audio for the given number of seconds 
            sd.wait() 
            # This will convert the NumPy array to an audio 
            # file with the given sampling frequency 
            record_name = f"recording{random.randint(0,1000)}.wav"
            write(f"{self.path}/{record_name}", freq, recording) 
            return f"audio file is stored with the name of {record_name}"
        except Exception:
            return "somthing went wrong cant able to record sorry"



def run(obj):
    obj.text_to_speech(obj.wish())
    while(True):
        try:
            obj.text_to_speech("ready")
            text = obj.speech_to_text()
        except Exception:
            obj.text_to_speech("maybe i am not connected to internet at this moment waiting for response")
            
        
        if "commands" in text:
            obj.text_to_speech("the commands are as follows ")
            obj.commnad()
            obj.text_to_speech("waiting for 5 seconds")
            sleep(5)

        elif "battery" in text:
            obj.text_to_speech("ok wait i am checking battery percentage ")
            bt = obj.battery()
            sleep(1)
            obj.text_to_speech(f"so your device is running on {bt} percentage battery ")
            sleep(1)

        elif "system details" in text:
            obj.text_to_speech(" wait a minute i am collecting information ")
            details = obj.platform_info()
            obj.text_to_speech(details)
        
        elif "youtube" in text:
            obj.text_to_speech("what you want to search sir tell me ")
            search = obj.speech_to_text_for_social()
            if search !=None:
                obj.text_to_speech("ok wait i am searching ")
                obj.youtube(search)
                obj.text_to_speech("waiting for 5 seconds")
                sleep(5)
            else:
                obj.text_to_speech("not able to do this operation sorry")


        elif "google" in text:
            obj.text_to_speech("what you want to search sir tell me ")
            search = obj.speech_to_text_for_social()
            if search != None:    
                obj.text_to_speech("ok wait i am searching ")
                obj.google(search)
                obj.text_to_speech("waiting for 5 seconds")
                sleep(5)
            else:
                obj.text_to_speech("not able to do this operation sorry")

        elif "wikipedia" in text:
            obj.text_to_speech("what you want to search sir tell me ")
            search = obj.speech_to_text_for_social()
            if search != None:
                obj.text_to_speech("wait i am searching ")
                bool = obj.wiki_pedia(search)
                if bool:
                    obj.text_to_speech(f"related data is collected and stored in current directary with the name {search}")
                else:
                    obj.text_to_speech("no data found try again")
            else:
                obj.text_to_speech("not able to do this operation sorry")


        elif "wait" in text:
            obj.text_to_speech(f"ok waiting time is {obj.wait} seconds")
            obj.waiting()

        elif "cant undersand" in text:
            print("cant undersand")
            obj.text_to_speech(".")
        
        elif "exit" in text:
            obj.text_to_speech(f"thanks {obj.name}  for using this module from code with govind")
            exit()


        elif "news" in text:
            obj.text_to_speech("ok wait fetching data using a p i")
            res = obj.news()
            if res[0]:
                obj.text_to_speech(f"new is stored in given path with the name of {res[1]}")
            else:
                obj.text_to_speech("somthing went wrong try again later in some time")

        elif "open editor" in text:
            res = obj.code_editor()
            obj.text_to_speech(res)

        elif "time" in text:
            obj.text_to_speech("ok checking wait")
            res = obj.return_time()
            obj.text_to_speech(f" it's {res} right now")

        elif "mail" in text:
            obj.text_to_speech("whome you want to send a mail")
            name_to_send = obj.speech_to_text_for_social()
            if name_to_send !=None:
                flag=None
                for key in obj.mails:
                    if  key in name_to_send:
                        key_name = key
                        flag=1
                if flag==1:
                    obj.text_to_speech("what is the message start")
                    content = obj.speech_to_text_for_social()
                    if content !=None:
                        res = obj.mail_to(obj.mails[key_name],content)
                        obj.text_to_speech(res)
                    else:
                        obj.text_to_speech("not able to do this operation sorry")
                else:
                    obj.text_to_speech("no name found may be you have not added it to mails please check it and try again")
            else:
                obj.text_to_speech("no response found sorry try again")


        elif "record" in text:
            obj.text_to_speech(f" the recording time is {obj.duration} seconds start recording in 1 seconds")
            res = obj.voice_recoder()
            obj.text_to_speech("time over time over stop")
            obj.text_to_speech(res)


        elif "text area" in text:
            obj.text_to_speech("ok wait opening textarea")
            textarea_website = "https://textarea.pythonanywhere.com/"
            webbrowser.open(textarea_website)
            obj.text_to_speech("waiting for 5 seconds")
            sleep(5)

        else:
            obj.text_to_speech("sorry not understand")



            