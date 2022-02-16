# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import json

url = 'https://map.naver.com/v5/search/'

service = webdriver.chrome.service.Service('../drivers/chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.implicitly_wait(0.5)
driver.get(url)

sleep(1.5)

searchbox = driver.find_element(By.CSS_SELECTOR,'.input_box > input:nth-child(2)')

# 반려동물 미용
searchcontent = input('검색 내용 입력 : ')

# 입력값 검색창에 입력 후 엔터
searchbox.send_keys(searchcontent)
searchbox.send_keys(Keys.ENTER)
sleep(0.3)
soup = BeautifulSoup(driver.page_source, 'html.parser')
sleep(0.5)

# -------------- 새로운 창 ----------------

# iframe 찾아서 switch하기
iframe = driver.find_element(By.ID,'searchIframe')
driver.switch_to.frame(iframe)
sleep(0.5)

# shop container ; 초기 설정
soup2 = BeautifulSoup(driver.page_source, 'html.parser')

# json 리스트 생성
lst = list()

# 한 section 기준으로 스크롤 내릴 것임
lastsection = driver.find_elements(By.CSS_SELECTOR,'ul > li')
# 액션 생성
action = ActionChains(driver)

## 페이지 읽어오기
pagebar = driver.find_elements(By.CSS_SELECTOR,'._2ky45 a')
# pagebar의 요소들 중 양쪽 끝 화살표 제외하고 사용
for page_num in pagebar[1:-1]:
    page_num.click()
    sleep(1)

    ## 한 페이지 최대 50개까지 출력하기 (총 4번 스크롤 밑으로 내리기)
    for i in range(1,5):
        try:
            # 10개 단위로 마지막 섹션으로 커서 이동
            action.move_to_element(lastsection[10*i-1]).perform()
            sleep(0.2)
            soup3 = BeautifulSoup(driver.page_source, 'html.parser')
            lastsection = driver.find_elements(By.CSS_SELECTOR, 'ul > li')
        except:
            # 만약 해당 페이지의 섹션 수가 50개 미만이라면:
            break
    sleep(0.2)
    soup3 = BeautifulSoup(driver.page_source, 'html.parser')
    sleep(0.3)
    # 한 가게 section
    # shops = soup3.find('ul').find_all('li')
    cnt = -1

    # 해당 페이지 내 모든 섹션
    shops = driver.find_elements(By.CSS_SELECTOR,'ul > li > div:nth-last-child(2) > a')
    print(len(shops))
    for shop in shops:
        temp = dict()
        cnt += 1
        # s_name = shop.find('span', class_='_3Apve').text
        # 가게 이름 눌러서 세부정보 창 열기
        shops[cnt].click()
        sleep(0.2)
        driver.switch_to.default_content()
        sleep(0.2)
        newframe = driver.find_element(By.ID, 'entryIframe')
        driver.switch_to.frame(newframe)
        sleep(0.2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        s_name = soup.find('span', class_='_3XamX').text.strip()
        address = soup.find('span', class_='_2yqUQ').text.strip()
        star = soup.find('span',class_='_1Y6hi _1A8_M')
        # 만약 평점이 없다면:
        if star == None:
            # 0점처리
            star = '0.0'
        else:
            star = star.find('em').text.strip()
        # print(f'상호명: {s_name}, 주소: {address}, 점수: {star}')

        # 딕셔너리에 추가
        temp['s_name'] = s_name
        temp['star'] = star
        temp['address'] = address
        lst.append(temp)

        driver.switch_to.default_content()
        driver.switch_to.frame(iframe)

# json dict 생성
json_dict = dict()
json_dict[searchcontent] = lst
json_lst = json.dumps(json_dict, ensure_ascii=False)

with open(f'{searchcontent}_naver.json','w',encoding='utf-8') as f:
    f.write(json_lst)






