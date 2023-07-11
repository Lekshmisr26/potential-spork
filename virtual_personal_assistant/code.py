import pyttsx3
import speech_recognition as sr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def start_engine():
  engine = pyttsx3.init()
  voices = engine.getProperty('voices')
  engine.setProperty('voice', voices[0].id)  # Select the voice
  return engine

def speak(engine, text):
  engine.say(text)
  engine.runAndWait()

def recognize_speech():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    audio = r.listen(source)
    
    try:
      print("Recognizing speech...")
      query = r.recognize_google(audio)
      print("You said:", query)
      return query.lower()
    except sr.UnknownValueError:
      print("Sorry, I didn't catch that. Could you please repeat?")
      return ""
    except sr.RequestError:
      print("Sorry, I'm currently experiencing technical issues. Please try again later.")
      return ""

def send_email(sender_email, sender_password, recipient_email, subject, message):
  try:
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Add the message body
    msg.attach(MIMEText(message, 'plain'))

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.send_message(msg)
    server.quit()

    print("Email sent successfully!")
  except smtplib.SMTPException as e:
    print("Error sending email:", str(e))

def perform_stress_reduction():
  engine = start_engine()
  speak(engine, "Performing stress reduction activities...")
   
  # Provide voice instructions and guide the user through stress reduction activities
  speak(engine, "Let's perform some stress reduction activities.")

  # Activity 1: Deep Breathing
  speak(engine, "Activity 1: Deep Breathing")
  speak(engine, "Take a deep breath in through your nose, and then slowly exhale through your mouth.")
  # Provide some time for the user to perform the activity

  # Activity 2: Progressive Muscle Relaxation
  speak(engine, "Activity 2: Progressive Muscle Relaxation")
  speak(engine, "Start by tensing the muscles in your toes, hold for a few seconds, and then relax.")
  # Provide instructions for tensing and relaxing different muscle groups

  # Activity 3: Visualization
  speak(engine, "Activity 3: Visualization")
  speak(engine, "Imagine yourself in a peaceful and serene environment, such as a beach or a garden.")
  # Provide details and guide the user through the visualization exercise

  speak(engine, "These were some stress reduction activities. Remember to take breaks and practice self-care regularly.")

  engine.quit()

def perform_anxiety_management():
    engine = start_engine()
    speak(engine, "Performing anxiety management activities...")
    speak(engine, "Welcome to anxiety management activities. Let's get started.")

    # Breathing exercise
    speak(engine, "We will begin with a breathing exercise.")
    speak(engine, "Sit or lie down in a comfortable position.")
    speak(engine, "Close your eyes and take a deep breath in through your nose, filling your lungs.")
    time.sleep(2)
    speak(engine, "Hold your breath for a few seconds.")
    time.sleep(2)
    speak(engine, "Now slowly exhale through your mouth, releasing all the tension.")
    time.sleep(2)
    speak(engine, "Repeat this breathing pattern for a few minutes, focusing on your breath.")
    time.sleep(2)
    speak(engine, "Take your time and relax.")

    # Progressive muscle relaxation
    speak(engine, "Next, we will practice progressive muscle relaxation.")
    speak(engine, "Start by tensing the muscles in your feet and toes.")
    time.sleep(2)
    speak(engine, "Hold the tension for a few seconds, then release and let the muscles relax completely.")
    time.sleep(2)
    speak(engine, "Move on to your calves and thighs, tensing and relaxing the muscles.")
    time.sleep(2)
    speak(engine, "Continue this process, moving up your body to your abdomen, chest, arms, and face.")
    time.sleep(2)
    speak(engine, "Feel the tension leaving your body as you relax each muscle group.")
    time.sleep(2)
    speak(engine, "Take your time and enjoy the sensation of relaxation.")

    # Guided visualization
    speak(engine, "Lastly, we will practice guided visualization.")
    speak(engine, "Close your eyes and imagine yourself in a peaceful and serene place.")
    time.sleep(2)
    speak(engine, "Picture the details of this place, such as the colors, sounds, and scents.")
    time.sleep(2)
    speak(engine, "Feel the calmness and tranquility washing over you.")
    time.sleep(2)
    speak(engine, "Stay in this visualization for a few minutes, allowing yourself to fully experience the relaxation.")

    speak(engine, "You have completed the anxiety management activities. I hope you feel more relaxed now.")

    engine.quit()


def respond_to_query(query):
  engine = start_engine()
  # Implement your response logic here based on the query
  # Provide the response in voice using the speak() function
  if query == "what's your name":
    speak(engine, "My name is Chat Assistant.")
  elif query == "tell me a joke":
    speak(engine, "Why don't scientists trust atoms? Because they make up everything!")
  else:
    speak(engine, "I'm sorry, I don't have a response for that.")

    engine.quit()


def personalize(query, mood, goal):
  # Implement your personalization logic here
  # Use the query, mood, and goal to personalize the assistant's responses
  print("Personalizing based on query:", query)
  print("Current mood:", mood)
  print("Goal:", goal)
  if query == "send email":
    send_email_feature()
  elif query == "stress reduction":
    perform_stress_reduction()
  elif query == "anxiety management":
    perform_anxiety_management()
  else:
    respond_to_query(query)


def send_email_feature():
  engine = start_engine()

  speak(engine, "Please provide the required details for sending the email.")

  speak(engine, "Enter your email address:")
  sender_email = recognize_speech()

  speak(engine, "Enter your email password:")
  sender_password = recognize_speech()

  speak(engine, "Enter the recipient's email address:")
  recipient_email = recognize_speech()

  speak(engine, "Enter the subject of the email:")
  subject = recognize_speech()

  speak(engine, "Enter the content of the email:")
  message = recognize_speech()

  send_email(sender_email, sender_password, recipient_email, subject, message)

  engine.quit()


# Main code execution
engine = start_engine()
while True:
  speak(engine, "How can I assist you?")
  user_input = recognize_speech()

  if user_input != "":
    if user_input == "quit":
      speak(engine, "Goodbye!")
      break
      
      speak(engine, "Enter your current mood:")
      mood = recognize_speech()
      
      speak(engine, "Enter your goal:")
      goal = recognize_speech()

      personalize(user_input, mood, goal)

engine.quit()




