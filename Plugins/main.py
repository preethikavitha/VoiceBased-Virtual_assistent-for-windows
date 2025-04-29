try:
    import os
    import logging
    import pyttsx3
    import sys
    import cv2
    import face_recognition
    import numpy as np
    import speech_recognition as sr
    import webbrowser
    import yt_dlp
    import pywhatkit
    import pyautogui
    from keras_preprocessing.sequence import pad_sequences
    from keras.models import load_model
    from pickle import load
   


    #sys.path.insert(0, os.path.expanduser('~') + "/PycharmProjects/Virtual_Voice_Assistant")
    sys.path.insert(0, os.path.expanduser('~')+"/Virtual-Voice-Assistant") # adding voice assistant directory to system path

    # importing modules made for assistant
    from database import *
    from image_generation import generate_image
    from gmail import *
    from API_functionalities import *
    from system_operations import *
    from browsing_functionalities import *
except (ImportError, SystemError, Exception, KeyboardInterrupt) as e:
    print("ERROR OCCURRED WHILE IMPORTING THE MODULES")
    exit(0)

# Suppress TensorFlow warnings
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Face Data Path
FACE_DATA_PATH = "user_face.npy"

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 185)

sys_ops = SystemTasks()
tab_ops = TabOpt()
win_ops = WindowOpt()

# Load trained chatbot model
model = load_model('..\\Data\\chat_model')

# Load tokenizer
with open('..\\Data\\tokenizer.pickle', 'rb') as handle:
    tokenizer = load(handle)

# Load label encoder
with open('..\\Data\\label_encoder.pickle', 'rb') as enc:
    lbl_encoder = load(enc)

# Initialize recognizer
recognizer = sr.Recognizer()

def speak(text):
    """Speak out the given text."""
    print("ASSISTANT -> " + text)
    try:
        engine.say(text)
        engine.runAndWait()
    except KeyboardInterrupt or RuntimeError:
        return

   
def detect_blink(eye_aspect_ratio):
    return eye_aspect_ratio < 0.20

def get_eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def register_user():
    if os.path.exists(FACE_DATA_PATH):
        print("Face already registered.")
        return

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not access the camera.")
        return

    print("Please look at the camera to register...")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image. Please check your camera.")
            break

        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
            np.save(FACE_DATA_PATH, face_encoding)
            print("Face registered successfully!")
            break

        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def check_antispoof(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    color_std = np.std(frame)
    return laplacian_var >= 20 and color_std >= 15

def authenticate_user():
    if not os.path.exists(FACE_DATA_PATH):
        print("No face data found. Registering...")
        register_user()
        return authenticate_user()

    stored_encoding = np.load(FACE_DATA_PATH)
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Error: Could not access the camera.")
        return False

    print("Authenticating... Please blink to verify liveness.")
    blink_detected = False
    match_confirmed = False
    start_time = time.time()

    while time.time() - start_time < 10:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image. Exiting...")
            break

        if not check_antispoof(frame):
            print("Spoof attempt detected. Blocked.")
            break

        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            if face_encodings:
                match = face_recognition.compare_faces([stored_encoding], face_encodings[0], tolerance=0.45)
                if match[0]:
                    match_confirmed = True

            face_landmarks_list = face_recognition.face_landmarks(frame)
            for landmarks in face_landmarks_list:
                left_eye = np.array(landmarks['left_eye'])
                right_eye = np.array(landmarks['right_eye'])
                left_ear = get_eye_aspect_ratio(left_eye)
                right_ear = get_eye_aspect_ratio(right_eye)

                if detect_blink(left_ear) or detect_blink(right_ear):
                    blink_detected = True

        if blink_detected and match_confirmed:
            print("Liveness and identity confirmed. Access granted.")
            cam.release()
            cv2.destroyAllWindows()
            return True

        cv2.imshow("Authenticate", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    return False
def record():
    """Capture voice input and return text."""
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        recognizer.dynamic_energy_threshold = True
        print("Listening...")
        audio = recognizer.listen(mic)
        try:
            text = recognizer.recognize_google(audio, language='en-in').lower()
            print("USER ->", text)  # Print user voice input
        except:
            return None
    return text

def chat(text):
    """Predict intent based on input text."""
    max_len = 20
    result = model.predict(pad_sequences(tokenizer.texts_to_sequences([text]), truncating='post', maxlen=max_len), verbose=False)
    intent = lbl_encoder.inverse_transform([np.argmax(result)])[0]
    return intent

def youtube(query):
    """Play YouTube video."""
    query = query.replace('play', ' ').replace('on youtube', ' ').replace('youtube', ' ').strip()
    print(f"Searching for videos: {query}...")

    try:
        ydl_opts = {'quiet': True, 'default_search': 'ytsearch', 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            video_url = info['entries'][0]['webpage_url']

        print(f"Opening video: {video_url}")
        webbrowser.open(video_url)
        return "Enjoy..."

    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Error: {e}"

def whatsapp():
    """Send a WhatsApp message after authentication."""
    if not authenticate_user():
        speak("Authentication failed. Cannot send WhatsApp message.")
        return

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


    l = ['name', '+919999999999']  # add name and phone number into the list

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
        return

def compose_and_send_email1():
    """Authenticate and send an email."""
    if not authenticate_user():
        speak("Authentication failed. Cannot send email.")
        return
    compose_and_send_email()
    
def screenshot() -> None:
    """Takes a screenshot and saves it."""

    img = pyautogui.screenshot()
    timestamp = time.strftime("%Y%m%d_%H%M%S")  # Generate a unique timestamp
    img_path = os.path.expanduser(f"~\\Pictures\\screenshot_{timestamp}.png")
    img.save(img_path)
    speak(f"Screenshot saved as {img_path}.")
    print(f"Screenshot saved as {img_path}.")

def main(query):
        add_data(query)
        intent = chat(query)
        done = False
        if ("google" in query and "search" in query) or ("google" in query and "how to" in query) or "google" in query:
            googleSearch(query)
            return
        
        elif ('whatsapp' in query):
            whatsapp()
            return

        elif ("youtube" in query and "search" in query) or "play" in query or ("how to" in query and "youtube" in query):
            youtube(query)
            return
        elif "distance" in query or "map" in query:
            get_map(query)
            return
        if intent == "joke" and "joke" in query:
            joke = get_joke()
            if joke:
                speak(joke)
                done = True
        elif intent == "news" and "news" in query:
            news = get_news()
            if news:
                speak(news)
                done = True
        elif intent == "ip" and "ip" in query:
            ip = get_ip()
            if ip:
                speak(ip)
                done = True
        elif intent == "movies" and "movies" in query:
            speak("Some of the latest popular movies are as follows :")
            get_popular_movies()
            done = True
        elif intent == "tv_series" and "tv series" in query:
            speak("Some of the latest popular tv series are as follows :")
            get_popular_tvseries()
            done = True
        elif intent == "weather" and "weather" in query:
            city = re.search(r"(in|of|for) ([a-zA-Z]*)", query)
            if city:
                city = city[2]
                weather = get_weather(city)
                speak(weather)
            else:
                weather = get_weather()
                speak(weather)
            done = True
        elif intent == "internet_speedtest" and "internet" in query:
            speak("Getting your internet speed, this may take some time")
            speed = get_speedtest()
            if speed:
                speak(speed)
                done = True
        elif intent == "system_stats" and "stats" in query:
            stats = system_stats()
            speak(stats)
            done = True
        elif intent == "image_generation" and "image" in query:
            speak("what kind of image you want to generate?")
            text = record()
            speak("Generating image please wait..")
            generate_image(text)
            done = True
        elif intent == "system_info" and ("info" in query or "specs" in query or "information" in query):
            info = systemInfo()
            speak(info)
            done = True
        elif intent == "email" and "email" in query:
            compose_and_send_email1()
        elif intent == "select_text" and "select" in query:
            sys_ops.select()
            done = True
        elif intent == "copy_text" and "copy" in query:
            sys_ops.copy()
            done = True
        elif intent == "paste_text" and "paste" in query:
            sys_ops.paste()
            done = True
        elif intent == "delete_text" and "delete" in query:
            sys_ops.delete()
            done = True
        elif intent == "new_file" and "new" in query:
            sys_ops.new_file()
            done = True
        elif intent == "switch_tab" and "switch" in query and "tab" in query:
            tab_ops.switchTab()
            done = True
        elif intent == "close_tab" and "close" in query and "tab" in query:
            tab_ops.closeTab()
            done = True
        elif intent == "new_tab" and "new" in query and "tab" in query:
            tab_ops.newTab()
            done = True
        elif intent == "close_window" and "close" in query:
            win_ops.closeWindow()
            done = True
        elif intent == "switch_window" and "switch" in query:
            win_ops.switchWindow()
            done = True
        elif intent == "minimize_window" and "minimize" in query:
            win_ops.minimizeWindow()
            done = True
        elif intent == "maximize_window" and "maximize" in query:
            win_ops.maximizeWindow()
            done = True
        elif intent == "screenshot" and "screenshot" in query:
            screenshot()
            done = True
        elif intent == "stopwatch":
            pass
        elif intent == "wikipedia" and ("tell" in query or "about" in query):
            description = tell_me_about(query)
            if description:
                speak(description)
            else:
                googleSearch(query)
            done = True
        elif intent == "math":
            answer = get_general_response(query)
            if answer:
                speak(answer)
                done = True
        elif intent == "open_website":
            completed = open_specified_website(query)
            if completed:
                done = True
        elif intent == "open_app":
            completed = open_app(query)
            if completed:
                done = True
        elif intent == "note" and "note" in query:
            speak("what would you like to take down?")
            note = record()
            take_note(note)
            done = True
        elif intent == "get_data" and "history" in query:
            get_data()
            done = True
        elif intent == "exit" and ("exit" in query or "terminate" in query or "quit" in query):
            exit(0)
        if not done:
            answer = get_general_response(query)
            if answer:
                speak(answer)
            else:
                speak("Sorry, not able to answer your query")
        return

"""
def main(query):

    intent = chat(query)

    if "whatsapp" in query:
        whatsapp()
    elif "email" in query:
        send_email()
    elif "play" in query or "youtube" in query:
        youtube(query)
    elif intent == "exit" and ("exit" in query or "terminate" in query or "quit" in query):
            exit(0)
    else:
        speak("Sorry, I don't understand.")
"""

def listen_audio():
    """Continuously listen and respond to user queries."""
    while True:
        response = record()
        if response:
            main(response)

if __name__ == "__main__":
    if authenticate_user():
        speak("Face authentication successful. You can now use voice commands.")
        listen_audio()
    else:
        speak("Access denied.")
        sys.exit(0)