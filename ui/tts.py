from gtts import gTTS
import pyglet

def textToSpeech(textStr):
    tts = gTTS(text=textStr, lang='en')
    tts.save("ui/sounds/temp.mp3")
    music = pyglet.media.load("ui/sounds/temp.mp3", streaming=False)
    music.play()