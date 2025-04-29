import smtplib
import os
from dotenv import load_dotenv
import re
import speech_recognition as sr
import pyttsx3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Load environment variables
load_dotenv(dotenv_path='..\\Data\\.env')

# Email credentials
sender_id = os.getenv('EMAIL_ID')
password = os.getenv('EMAIL_PASSWORD')

# Initialize text-to-speech
engine = pyttsx3.init()

# Define the folder where attachments are stored
ATTACHMENT_FOLDER = r"C:\Users\MSSP\OneDrive\Documents"  # Change this to your folder path

def speak(text):
    """Converts text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Captures voice input and converts it to text, displaying the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        try:
            speak("Listening...")
            print("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # Increased timeout
            text = recognizer.recognize_google(audio).strip().lower()
            print(f"Recognized: {text}")  # Display recognized text
            return text
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            print("Error: No speech detected.")
            return None
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Please try again.")
            print("Error: Could not understand speech.")
            return None
        except sr.RequestError:
            speak("Could not request results. Please check your internet connection.")
            print("Error: API request failed.")
            return None

def send_email(receiver_id, subject, body, attachment_path=None):
    """Sends an email with an optional attachment"""

    msg = MIMEMultipart()
    msg['From'] = sender_id
    msg['To'] = receiver_id
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach file if provided
    if attachment_path:
        filename = os.path.basename(attachment_path)
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_id, password)
        server.sendmail(sender_id, receiver_id, msg.as_string())
        server.quit()
        return True
    except smtplib.SMTPRecipientsRefused:
        speak("Invalid email address.")
        print("Error: Invalid email address.")
        return False
    except smtplib.SMTPException:
        speak("Error sending email.")
        print("Error: Failed to send email.")
        return False

def check_email(email):
    """Validates email format"""
    verifier = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return bool(re.fullmatch(verifier, email))

def find_file_in_folder(filename):
    """Search for a file by name, even if the user does not specify an extension."""
    print(f"Searching for file: {filename}")  # Debugging

    available_files = os.listdir(ATTACHMENT_FOLDER)
    print("Available files:", available_files)  # Debugging

    # Normalize filenames (lowercase, remove spaces)
    filename = filename.lower().replace(" ", "")

    for file in available_files:
        file_clean = file.lower().replace(" ", "")

        # Match with or without extension
        if filename in file_clean or filename in os.path.splitext(file_clean)[0]:
            file_path = os.path.join(ATTACHMENT_FOLDER, file)
            print(f"File found: {file_path}")  # Debugging
            return file_path

    print("File not found in folder.")  # Debugging
    return None

def compose_and_send_email():
    """Handles the email composition by listening to user input and sending an email."""

    speak("Type the receiver's email ID.")
    receiver_id = input("Enter the receiver's email ID: ")

    while not check_email(receiver_id):
        speak("Invalid email format. Please enter again.")
        print("Invalid email format. Please enter again.")
        receiver_id = input("Enter the receiver's email ID: ")

    speak("Tell the subject of the email.")
    subject = listen()
    while not subject:  # Retry if speech was not recognized
        speak("I couldn't understand. Please say the subject again.")
        subject = listen()

    speak("Tell the body of the email.")
    body = listen()
    while not body:  # Retry if speech was not recognized
        speak("I couldn't understand. Please say the body again.")
        body = listen()

    speak("Would you like to attach a file? Please say yes i want to attach or no i dont want to attach.")
    response =listen()
    attachment_path = None

    if response and "yes i want to attach" in response:
        speak("Please say the name of the file you want to attach.")
        filename = listen()
        if filename:
            attachment_path = find_file_in_folder(filename)
            if attachment_path:
                speak(f"File {filename} found. Sending email with attachment.")
                print(f"File {filename} found. Sending email with attachment.")
            else:
                speak(f"File {filename} not found in the folder. Sending email without attachment.")
                print(f"File {filename} not found in the folder. Sending email without attachment.")

    success = send_email(receiver_id, subject, body, attachment_path)

    if success:
        speak("Email sent successfully.")
        print("Email sent successfully.")
    else:
        speak("Error occurred while sending email.")

# Run the process

    
