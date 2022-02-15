# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

lat = '14139953.7607221'
lon = '4518552.6933668'
url = f'https://map.naver.com/v5/search/'

service = webdriver.chrome.service.Service('../drivers/chromedriver.exe')
driver = webdriver.Chrome(service=service)

searchcontent = '서울 반려동물미용'

driver.implicitly_wait(5)
driver.get(url)

sleep(1)

searchbox = driver.find_element(By.CSS_SELECTOR,'.input_box > input:nth-child(2)')

searchbox.send_keys(searchcontent)
searchbox.send_keys(Keys.ENTER)
sleep(1)
soup = BeautifulSoup(driver.page_source, 'html.parser')
sleep(2)

# 창바뀜 -------------------------------------------------

# frame 찾아서 switch하기
iframe = driver.find_element(By.ID,'searchIframe')
driver.switch_to.frame(iframe)
sleep(1)

# shop container ; 초기 설정
soup2 = BeautifulSoup(driver.page_source, 'html.parser')
openbutton = driver.find_elements(By.CSS_SELECTOR, '._1AEUt')

# 액션 생성
action = ActionChains(driver)

# 4번 반복
for i in range(1,5):
    global soup3
    action.move_to_element(openbutton[10*i-1]).perform()
    sleep(5)
    soup3 = BeautifulSoup(driver.page_source, 'html.parser')
    openbutton = driver.find_elements(By.CSS_SELECTOR, '._1AEUt')
sleep(1)

shops = soup3.find_all('li', {'class': '_22p-O _2NEjP'})
openbutton = driver.find_elements(By.CSS_SELECTOR, '._1AEUt')
cnt = -1

for shop in shops:
    cnt += 1
    s_name = shop.find('span', class_='_3Apve').text
    openbutton[cnt].click()
    sleep(0.5)
    soup2 = BeautifulSoup(driver.page_source, 'html.parser')
    address = soup2.find('div', class_='_2b9ic').text[3:-2]
    openbutton[cnt].click()
    print(s_name,address)




# # 커서 바꾸기
# whatever = driver.find_element(By.CLASS_NAME, 'place_on_pcmap')
# action = ActionChains(driver)
#
# action.move_to_element(whatever).perform()

# # # 스크롤 끝까지 다하기
#
# prev_height = driver.execute_script('return document.body.scrollHeight')
#
#
# while True:
#     driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
#     sleep(1)
#     curr_height = driver.execute_script('return document.body.scrollHeight')
#     if curr_height == prev_height:
#         break
#     else:
#         prev_height = driver.execute_script('return document.body.scrollHeight')
#





