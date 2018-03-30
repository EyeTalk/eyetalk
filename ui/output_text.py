from gtts import gTTS
import pygame
import smtplib
from time import sleep


server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login('eyetalktest', 'eyetalk1')

# John's phone, we should change this as necessary
my_phone = '6507439481@mms.att.net'
pygame.init()


def textToSpeech(textStr):
    tts = gTTS(text=textStr, lang='en')
    tts.save("ui/sounds/temp.mp3")
    pygame.mixer.music.load("ui/sounds/temp.mp3")
    sleep(0.25)
    pygame.mixer.music.play()


def send_text_message(textStr):
    message = textStr.title()
    server.sendmail('eyetalktest@gmail.com', my_phone, message)
