from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time, os
import urllib.request
import json
import base64
import requests
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import openai
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image


def get_files_count(folder_path):
    files = os.listdir(folder_path)
    return len(files)


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        elif os.path.exists(directory):
            for file in os.scandir(directory):
                os.remove(file.path)
    except OSError:
        print ('Error: Creating directory. ' +  directory)



# crawling
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
createFolder('./images/')
driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
driver.implicitly_wait(3)
url = 'https://www.coupang.com/vp/products/1391941541?vendorItemId=70421336400&sourceType=HOME_RELATED_ADS&searchId=feed-2dbaca13780545a083bb3b3380333690-related_ads&clickEventId=09febaf0-0210-4823-a8ec-8289f481f32e&isAddedCart='
driver.get(url)

try:
    driver.find_element(By.CSS_SELECTOR, '#itemBrief > div > p.essential-info-more > a').click()
except:
    pass

elem_detail = driver.find_element(By.TAG_NAME, "body")
for i in range(60):
    elem_detail.send_keys(Keys.PAGE_DOWN)

createFolder('./images/')
links = []
detail_images = driver.find_elements(By.ID, "productDetail")
for detail_image in detail_images:
    if detail_image.find_elements(By.TAG_NAME, "img") != None:
        detail_images = detail_image.find_elements(By.TAG_NAME, "img")
        for detail_image in detail_images:
            if detail_image.get_attribute('src') != None:
                links.append(detail_image.get_attribute('src'))

for k, i in enumerate(links):
    url = i
    urllib.request.urlretrieve(url, './images/'+str(k)+'.jpg')

print('상품 정보를 불러오고 있습니다. 잠시만 기다려주세요...')

list=[]
product = driver.find_element(By.CSS_SELECTOR, '.prod-buy-header__title').text
list.append("상품명: " + product)

price = driver.find_elements(By.CSS_SELECTOR, '.total-price > strong')
list.append("가격: " + price[0].text)
try:
    list.append("와우 할인가: " + price[1].text)
except:
    pass

try:
    unit_price = driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.dawn-only-product.without-subscribe-buy-type.DISPLAY_0.only-one-delivery > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.major-price-coupon > span.unit-price.font-medium').text
    list.append(unit_price)
except:
    pass

if(driver.find_element(By.CSS_SELECTOR, '.prod-shipping-fee-message > span').text != ""):
    shipping_fee = driver.find_element(By.CSS_SELECTOR, '.prod-shipping-fee-message > span').text
    list.append("배송비: " + shipping_fee)
else:
    shipping_fee1 = driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-shipping-fee-and-pdd-wrapper.apply-unknown-customer-handling > div.shipping-fee-list > div.radio-list-item.SHIPPING_FEE_NUDGE_DISPLAY_0.selected > span.shipping-fee-list-item.inline-flex-v-center').text
    shipping_fee2 = driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-shipping-fee-and-pdd-wrapper.apply-unknown-customer-handling > div.shipping-fee-list > div.radio-list-item.SHIPPING_FEE_NUDGE_DISPLAY_1 > span.shipping-fee-list-item.inline-flex-v-center').text
    list.append("배송비: " + shipping_fee1 + " 또는 " + shipping_fee2)

if driver.find_element(By.CSS_SELECTOR, '.prod-pdd-container > div').text != "":
    shipping_day = driver.find_element(By.CSS_SELECTOR, '.prod-pdd-container > div').text
    list.append("배송 예정일: " + shipping_day)
else:
    ship = driver.find_elements(By.CSS_SELECTOR, '.prod-pdd-list > div')
    list.append("배송 예정일: " + ship[0].text + " 또는 " + ship[1].text)

try:
    deliver_info = driver.find_element(By.CSS_SELECTOR, "#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price.with-seller-store-rating > div.prod-vendor-container").text
    list.append(deliver_info)
except:
    pass

try:
    option=driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_1 > div.prod-shipping-fee-and-pdd-wrapper.apply-unknown-customer-handling').text
    list.append(option)
except:
    pass

try:
    options=driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-option > div > div > div > button > table > tbody > tr > td:nth-child(1)').text
    list.append(options)
except:
    pass

try: 
    production = driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-description').text
    list.append(production)
except:
    pass

try:
    production = driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.dawn-only-product.without-subscribe-buy-type.DISPLAY_0.only-one-delivery > div.prod-description').text
    list.append(production)
except:
    pass

table1 = driver.find_element(By.CSS_SELECTOR, '#itemBrief > div')
tbody1 = table1.find_element(By.TAG_NAME, "tbody")
rows1 = tbody1.find_elements(By.TAG_NAME, "tr")
for tr in rows1:
    ths = tr.find_elements(By.TAG_NAME, "th")
    tds = tr.find_elements(By.TAG_NAME, "td")
    for th, td in zip(ths, tds):
        list.append(th.text.strip() + ": " + td.text.strip())

def get_page_data():
    users = driver.find_elements(By.CSS_SELECTOR, '.sdp-review__article__list__info__user__name.js_reviewUserProfileImage')
    ratings = driver.find_elements(By.CSS_SELECTOR, '.sdp-review__article__list__info__product-info__star-orange.js_reviewArticleRatingValue')
    headline = driver.find_elements(By.CSS_SELECTOR, '.sdp-review__article__list__headline')
    contents = driver.find_elements(By.CSS_SELECTOR, '.sdp-review__article__list__review__content.js_reviewArticleContent')
    survey = driver.find_elements(By.CSS_SELECTOR, '.sdp-review__article__list__survey')
        
    if len(users) == len(ratings):            
        for index in range(len(users)):
            data = {}
            data['사용자'] = users[index].text
            data['평점'] = int(ratings[index].get_attribute('data-rating'))
            try:
                data['리뷰 제목'] = headline[index].text
            except:
                data['리뷰 제목'] = ""
            try:
                data['리뷰 내용'] = contents[index].text
            except:
                data['리뷰 내용'] = ""
            try:
                data['설문 조사'] = survey[index].text
            except:
                data['설문 조사'] = ""
            list.append(data)
            
get_page_data() 
print(list)

driver.close()


# 사진 자르기
from PIL import Image

def image_crop( infilename , save_path):
    img = Image.open( infilename )
    (img_h, img_w) = img.size

    # crop 할 사이즈 : grid_w, grid_h
    grid_w = 1960 # crop width
    grid_h = 860 # crop height
    range_w = (int)(img_w/grid_w)
    range_h = (int)(img_h/img_h)
 
    i = 0
 
    folderSize = get_files_count(save_path)
    for w in range(range_w):
        for h in range(range_h):
            bbox = (h*grid_h, w*grid_w, (h+1)*(grid_h), (w+1)*(grid_w))
            # 가로 세로 시작, 가로 세로 끝
            crop_img = img.crop(bbox)

            fname = "{}.jpg".format("{0:01d}".format(folderSize + i))
            crop_img.save('images/' + fname)
            i += 1
 
if not os.path.exists('images'):
    print("사진이 없습니다.")
else:
    length = get_files_count('images')
    for i in range(length):
        image_crop('./images/' + str(i) + '.jpg', './images/')


# OCR
 # 본인의 APIGW Invoke URL로 치환
URL = ""
    
 # 본인의 Secret Key로 치환
KEY = ""
    
ocr_result = []
if not os.path.exists('images'):
    print("사진이 없습니다.")
else:
    length = get_files_count('images')
    for i in range(length):
        with open('images/'+ str(i) +'.jpg', "rb") as f:
            img = base64.b64encode(f.read())
            image = Image.open('images/'+ str(i) +'.jpg')
            (image_h, image_w) = image.size
            if(image_h > 860 or image_w > 1960):
                continue
        headers = {
            "Content-Type": "application/json",
            "X-OCR-SECRET": KEY
        }
    
        data = {
            "version": "V1",
            "requestId": "sample_id", # 요청을 구분하기 위한 ID, 사용자가 정의
            "timestamp": 0, # 현재 시간값
            "lang": "ko",
            "resultType": "string",
            "images": [
                {
                    "name": "sample_image",
                    "format": "jpg",
                    "data": img.decode('utf-8')
                }
            ]
        }

        data = json.dumps(data)
        response = requests.post(URL, data=data, headers=headers)
        res = json.loads(response.text)

        ocr_text = []

        for i in range(len(res['images'][0]['fields'])):
            plz = res['images'][0]['fields'][i]['inferText']
            ocr_text.append(plz)

        result = ' '.join(s for s in ocr_text)
        ocr_result.append(result)
print(ocr_result)


# GPTchatBot
# 본인의 API Key로 치환
openai.api_key = ""


messages = []


init = "이제 내가 물어볼건데 한 줄로 대답해주길 바래. 이 때 ml은 미리리터 라고 알려주고 x는 곱하기라고 말해줘. 배송 예정일 같은 경우는 몇월 며칠이라고 읽어줘. 그리고 모든 대답은 존댓말로 해줘. 이제 물어볼게"


content = str(list) + str(ocr_result)

def answer(recognizer,audio):
    
    text = recognizer.recognize_google(audio, language='ko')

    if('종료' in text):
        stop_listening(wait_for_stop=False)
        exit()

    else:    
        try:
            text = recognizer.recognize_google(audio, language='ko')
            
            print('[사용자]'+ text)

            user_content = content + "              " + init + text
            
            
            messages.append({"role": "user", "content": f"{ user_content}"})

            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

            assistant_content = completion.choices[0].message["content"].strip()

            messages.append({"role": "assistant", "content": f"{assistant_content}"})

            speak(assistant_content)

            messages.clear()

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
