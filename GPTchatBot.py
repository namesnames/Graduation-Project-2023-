
import time,os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import openai
import pyttsx3

from pydub import AudioSegment
from pydub.playback import play



openai.api_key = ""

messages = []

def answer(recognizer,audio):
    answer_text = ''
    
    
    #while True:

    try:
        text = recognizer.recognize_google(audio, language='ko')
        #user_content = input("user : ")
        print('[이한주]'+ text)

        user_content = text            
        
        messages.append({"role": "user", "content": f"{user_content}"})

        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

        assistant_content = completion.choices[0].message["content"].strip()

        messages.append({"role": "assistant", "content": f"{assistant_content}"})

        speak(assistant_content)

    except sr.UnknownValueError:
        print('인식 실패')
    except sr.RequestError as e:
        print('요청 실패 : {0}'.format(e))   



# 소리내 읽기 (TTS)
# def speak(text):
#     print('[인공지능]'+ text)
#     file_name = 'voice.mp3'
#     tts = gTTS(text=text, lang='ko')
#     tts.save(file_name)
#     playsound(file_name)
#     if os.path.exists(file_name): # voice.mp3 파일 삭제 -> 권한 문제가 생겨서 제대로 안 될 수가 있어서
#         os.remove(file_name)
    

# 소리내 읽기 (TTS)
def speak(text):
    print('[인공지능]'+ text)
    file_name = 'voice.mp3'
    tts = gTTS(text=text, lang='ko')
    tts.save(file_name)

    # 속도 조절
    sound = AudioSegment.from_file(file_name, format='mp3')
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * 1.15)})
    # sound_with_altered_frame_rate = sound_with_altered_frame_rate[:-50]
    sound_with_altered_frame_rate.export(file_name, format='mp3')

    # 재생
    playsound(file_name)

    # 파일 삭제
    if os.path.exists(file_name): # voice.mp3 
        os.remove(file_name)   
        
    

#마이크로부터 음성듣기
r = sr.Recognizer()
m = sr.Microphone()

speak('무엇을 도와드릴까요?')


stop_listening = r.listen_in_background(m, answer)
# stop_listening(wait_for_stop=False)

while True:
    time.sleep(0.1)

