import speech_recognition as sr
import pywhatkit
import pyttsx3


speaker = pyttsx3.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)
speaker.say('Hello, how may I help you?')
speaker.runAndWait()

listener = sr.Recognizer()

def getSpeech():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration = 0.2)
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
            
    except:
        print('No command')
        return None
    return command

l = ['name', '+919999999999']

def getNum(l, command):
    counter = 0
    for i in l:
        if i ==command:
            numIndex = counter + 1
            num = l[numIndex]
            return num
        counter = counter + 1
        
    return None
while True:
    command =getSpeech()
    if 'send whatsapp message to' in command:
        name = command.replace('send whatsapp message to', '')
        name = name.strip()
        number = getNum(l, name)
        speaker.say('what would you like me to say')
        speaker .runAndWait()
        newCommand = getSpeech()
        speaker.say('what time would you like me to send the message?')
        speaker.runAndWait()
        sendTime = getSpeech()
        if ':' in sendTime:
            sendTime = sendTime.replace(':', '')
            sendTime = sendTime.strip()
        speaker.say('message to '+name+ 'has been scheduled')
        speaker.runAndWait()
        hours = sendTime[0:2]
        hours = int(hours)
        minutes = sendTime[2:4]
        minutes = int(minutes)
        pywhatkit.sendwhatmsg(number, newCommand, hours, minutes)
