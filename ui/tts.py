from gtts import gTTS
import pygame


def textToSpeech(textStr):
    tts = gTTS(text=textStr, lang='en')
    tts.save("ui/sounds/temp.mp3")
    pygame.init()
    pygame.mixer.music.load("ui/sounds/temp.mp3")
    pygame.mixer.music.play()