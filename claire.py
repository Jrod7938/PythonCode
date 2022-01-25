#CLAIRE: CLEARLY LIMITED ARTIFICIAL INTELLIGENCE RUNNING EXPERIMENTS
import pyttsx3
import speech_recognition as sr
import webbrowser  
import datetime  
import wikipedia 
import wolframalpha
import os
import subprocess


  
appId = '7PRYW6-WTETRTVY6E'
client = wolframalpha.Client(appId)
  
# this method is for taking the commands
# and recognizing the command from the
# speech_Recognition module we will use
# the recongizer method for recognizing
def takeCommand():
  
    r = sr.Recognizer()
  
    # from the speech_Recognition module 
    # we will use the Microphone module
    # for listening the command
    with sr.Microphone() as source:
        print('Listening')
          
        # seconds of non-speaking audio before 
        # a phrase is considered complete
        r.pause_threshold = 0.7
        audio = r.listen(source)
          
        # Now we will be using the try and catch
        # method so that if sound is recognized 
        # it is good else we will have exception 
        # handling
        try:
            print("Recognizing")
              
            # for Listening the command in english
            # english we can also use 'en-US' 
            Query = r.recognize_google(audio, language='en-US')
            print("the command is printed=", Query)
              
        except Exception as e:
            print(e)
            print("Say that again sir")
            return "None"
          
        return Query
  
def speak(audio):
      
    engine = pyttsx3.init()
    # getter method(gets the current value
    # of engine property)
    voices = engine.getProperty('voices')
      
    # setter method .[0]=male voice and 
    # [33]=female voice in set Property on mac
    engine.setProperty('voice', voices[33].id)
      
    # Method for the speaking of the the assistant
    engine.say(audio)  
      
    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()
  
def tellDay():
      
    # This function is for telling the
    # day of the week
    day = datetime.datetime.today().weekday() + 1
      
    #this line tells us about the number 
    # that will help us in telling the day
    Day_dict = {1: 'Monday', 2: 'Tuesday', 
                3: 'Wednesday', 4: 'Thursday', 
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
      
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week)
  
  
def tellTime():
      
    # This method will give the time
    time = str(datetime.datetime.now())
      
    # the time will be displayed like 
    # this "2020-06-05 17:50:14.582630"
    #nd then after slicing we can get time
    print(time)
    hour = time[11:13]
    min = time[14:16]
    speak("Sir the time is " + hour + "Hours and" + min + "Minutes")    
  
def is_runnning(app):
    count = int(subprocess.check_output(["osascript",
                "-e", "tell application \"System Events\"",
                "-e", "count (every process whose name is \"" + app + "\")",
                "-e", "end tell"]).strip())
    return count > 0


def Hello():
      
    # This function is for when the assistant 
    # is called it will say hello and then 
    # take query
    speak("hello sir, I am Claire your desktop assistant. How may I help you?")
  
  
def Take_query():
  
    # calling the Hello function for 
    # making it more interactive
    Hello()
      
    # This loop is infinite as it will take
    # our queries continuously until and unless
    # we do not say bye to exit or terminate 
    # the program
    while(True):
          
        # taking the query and making it into
        # lower case so that most of the times 
        # query matches and we get the perfect 
        # output
        query = takeCommand().lower()
        wake = 'claire'

        if wake in query or "clare" in query or "clear" in query:
            if "open the website" in query:
                query = query.split()
                query = query[-1]
                speak(f"Opening {query}")
                
                
                # in the open method we just to give the link
                # of the website and it automatically open 
                # it in your default browser
                webbrowser.open(f"https://www.{query}")
                print(f"www.{query}")
                continue
                
            elif "what day is it" in query:
                tellDay()
                continue
            
            elif "what time is it" in query:
                tellTime()
                continue
            
            # this will exit and terminate the program
            elif "bye" in query:
                speak("Goodbye sir")
                exit()
            
            elif "from wikipedia" in query or "use wikipedia" in query:
                
                # if any one wants to have a information
                # from wikipedia
                speak("Checking the wikipedia ")
                query = query.split()
                query = " ".join(query[3:])
                print(query)
                
                # it will give the summary of 4 lines from 
                # wikipedia we can increase and decrease 
                # it also.
                try:
                    result = wikipedia.summary(query, sentences=3)
                    print(result)
                    speak("According to wikipedia")
                    speak(result)
                except Exception as e:
                    print(e)
                    speak(f"Sir i was unable to search that, please try again. {e}")

            
            elif "who are you" in query:
                speak("I am Claire. Your deskstop Assistant")

            # What Claire can do
            elif "what can you do" in query:
                speak("I can open websites or applications, tell the time, answer general knowledge questions, and you can program me to do more.")
            
            
            # "Question, how far is earth from the sun"
            elif "from database" in query or "use database" in query:
                try:            
                    query = query.split()
                    query = " ".join(query[3:])
                    print(query)
                    res = client.query(query)
                    answer = next(res.results).text
                    print(answer)
                    speak(f"The answer is: {answer}")
                except Exception as e:
                    print(e)
                    speak(f"Sorry sir I didn't get that. {e}")

            # Open an app
            elif "open the app" in query or "open app" in query:
                try:
                    query = query.split()
                    app = query[-1]
                    os.system(f"open -a {app}")
                    if is_runnning(app):
                        speak(f"Successfully opened {app}")
                    else:
                        speak(f"I was unsuccessful in opening {app}")
                except Exception as e:
                    print(e)
                    speak(f"Sorry sir, I was unable to open tha application for you. {e}")
  
            # Close an app
            elif "close the app" in query or "close app" in query:
                try:
                    query = query.split()
                    app = query[-1]
                    os.system(f"osascript -e 'quit app \"{app}\"'")
                    if is_runnning(app) == False:
                        speak(f"Successfully closed {app}")
                    else:
                        speak(f"I was unsuccessful in closing the {app}")
                except Exception as e:
                    print(e)
                    speak(f"Sorry sir, I was unable to close tha application for you. {e}")
        
        # Says good boy to Lucifer (Buddy) when I say good boy :)
        else:
            if "good boy" in query:
                speak("Good boy. You are such a good boy buddy.")
if __name__ == '__main__':
      
    # main method for executing
    # the functions
    Take_query()