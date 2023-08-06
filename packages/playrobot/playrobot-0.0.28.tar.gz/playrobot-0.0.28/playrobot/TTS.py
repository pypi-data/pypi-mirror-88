from gtts import gTTS
from pygame import mixer
import calendar
import time
import math
import re
import requests

LANGUAGE = 'zh-tw'

#語音輸出
def wordToSound(text):
    global LANGUAGE
    file_name ='test2.mp3'
    tts = gTTS(text, lang = LANGUAGE)
    tts.save(file_name)
    mixer.init()
    mixer.music.load(file_name)
    mixer.music.play()
    while mixer.music.get_busy() == True:
        continue
    mixer.music.stop()
    mixer.quit()
