from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import urllib.request


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        elif os.path.exists(directory):
            for file in os.scandir(directory):
                os.remove(file.path)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
createFolder('./images/')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(3)
url = 'https://www.coupang.com/vp/products/1391941541?vendorItemId=70421336400&sourceType=HOME_RELATED_ADS&searchId=feed-2dbaca13780545a083bb3b3380333690-related_ads&clickEventId=09febaf0-0210-4823-a8ec-8289f481f32e&isAddedCart='
driver.get(url)

try:
    driver.find_element(By.CSS_SELECTOR, '#itemBrief > div > p.essential-info-more > a').click()
except:
    pass

elem = driver.find_element(By.TAG_NAME, "body")
for i in range(60):
    elem.send_keys(Keys.PAGE_DOWN)

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

shipping_fee = driver.find_element(By.CSS_SELECTOR, '.prod-shipping-fee-message > span').text
list.append("배송비: " + shipping_fee)

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
    production = driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-description').text
    list.append(production)
except:
    production = driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.dawn-only-product.without-subscribe-buy-type.DISPLAY_0.only-one-delivery > div.prod-description').text
    list.append(production)

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