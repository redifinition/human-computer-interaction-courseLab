import os
import random
import time
import playsound
import speech_recognition as sr
import requests
import subprocess


BEGIN_REPONSE = 'Hello,I \'m here ! I can play music for you, open different kinds of software, get the weather.' \
                'Maybe you can say \'play music for me \',\'tell me the weather\', \'help me open some softwares\'.'

NO_WAKE_UP_RESPONSE = 'Sorry, You have not wake me up.'
MUSIC_CHOICE = 'Here I have prepared some musics for you, which one do you want to hear?'
ERROR_RESPONSE = 'Sorry, I don\'t understand what you have said.Please click the button and speak again.'
PLAY_MUSIC_SERVICE = 'Okay,Let us listen this music named'
WEATHER_SERVICE = 'Okay ,today \'s weather is: '
OPEN_SOFTWARE_SERVICE = 'Okay, I can help you open the following software:notepad'
OPEN_NOTEPAD = 'Okay,I have opened the notepad for you'
OPEN_WEB_BROWSER = 'Okay,I have opened the web browser for you '



class CommandExecutor:
    def __new__(cls, *args, **kwargs) -> object:
        """
        cls : class Singeton
        """
        if not hasattr(cls, "ins"):
            insObject = super(__class__, cls).__new__(cls, *args, **kwargs)
            setattr(cls, "ins", insObject)
        return getattr(cls, "ins")


    def __init__(self):
        # 创建
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()



    def getCommand(self):
        return self.recognize_speech_from_mic(self.recognizer,self.microphone)

    def recognize_speech_from_mic(self,recognizer, microphone):
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                   successful
        "error":   `None` if no error occured, otherwise a string containing
                   an error message if the API could not be reached or
                   speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source,duration=0.2)
            audio = recognizer.listen(source)

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
            # try recognizing the speech in the recording
            # if a RequestError or UnknownValueError exception is caught,
            #     update the response object accordingly
        try:
            houdify_id = 'kz90eBQUZiJ8BvfN6BUH9g=='
            houdify_pwd = 'ZnHajlpCtpEs2cpthYNnI_nH_dzmnsRqO4dUrwF-gmKqFZ-MiPkUrTe2Wh_cfzqTyD7RT_dLmqxV1lziDVHb_w=='
            text =  recognizer.recognize_houndify(audio, houdify_id, houdify_pwd)
            text = text.lower()
            return text
        except sr.RequestError:
            # API was unreachable or unresponsive
            return "oops...Something wrong happened"
        except sr.UnknownValueError:
            # speech was unintelligible
            return "Unable to recognize speech"

    def getResponse(self,result):
        # 根据识别的信息获取相应的回复
        self.said_text = result
        if result == 'hey bro':
            return BEGIN_REPONSE
        elif 'music' in result:
                return MUSIC_CHOICE
        elif 'weather' in result:
                result = WEATHER_SERVICE
                result += '\n'
                result += self.searchWeather()
                return result
        elif 'stay' in result:
                os.system('stay.mp3')
                return MUSIC_CHOICE+'stay.'
        elif 'beautiful' in result:
                os.system('beautiful.mp3')
                return MUSIC_CHOICE + 'Beautiful(鬼怪OST)'
        elif 'love is gone' in result:
                os.system('love.mp3')
                return MUSIC_CHOICE + 'Love is Gone'
        elif 'software' in result:
            return OPEN_SOFTWARE_SERVICE
        elif 'notepad' in result:
            subprocess.run(["notepad"])
            return OPEN_NOTEPAD
        elif 'browser' in result:
            import webbrowser
            webbrowser.open("http://www.baidu.com")
            return OPEN_WEB_BROWSER
        else:
            return ERROR_RESPONSE


    # 查询天气
    def searchWeather(self):
        r = requests.get('http://wthrcdn.etouch.cn/weather_mini?city=上海')
        r.encoding = 'utf-8'
        result = ''
        result += str(r.json()['data']['city'])
        result += '\n'
        for dict in r.json()['data']['forecast']:
            result += str(dict['date'])
            result += (' ' + str(dict['high']))
            result += (' ' + str(dict['low']))
            result += (' ' + str(dict['type']))
            result += '\n'
        return result

class CommandExecutorSingleton(CommandExecutor):
    pass