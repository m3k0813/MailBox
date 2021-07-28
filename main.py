from typing import Text
from selenium import webdriver
import pymysql
import json
import requests
from selenium.webdriver.common.keys import Keys
import pyperclip
import time

db = pymysql.connect(
    user='root',
    passwd='',
    host='localhost',
    db='mailb',
    charset='utf8'
)

# 카카오톡 메세지 보내기
Kakao_Token = ""


def Kakao(text):
    header = {"Authorization": 'Bearer ' + Kakao_Token}
    url = "https://kapi.kakao.com//v2/api/talk/memo/default/send"
    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }
    data = {"template_object": json.dumps(post)}
    return requests.post(url, headers=header, data=data)

# 다음 메일


def Daum():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(
        '/chromedriver.exe',  options=options)
    driver.implicitly_wait(2)
    driver.get(
        'https://logins.daum.net/accounts/signinform.do?url=https%3A%2F%2Fmail.daum.net%2F')
    driver.implicitly_wait(3)

    my_id = ""
    my_pwd = ""

    driver.find_element_by_name('id').send_keys(my_id)
    driver.find_element_by_name('pw').send_keys(my_pwd)

    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()

    # 메일 제목 추출
    title = driver.find_element_by_css_selector('strong.tit_subject')
    # 메일 날짜 추출
    date = driver.find_element_by_class_name('txt_date')

    curs = db.cursor(pymysql.cursors.DictCursor)

    curs.execute('SELECT * FROM dates;')  # Select 데이터 조회
    date_db = curs.fetchone()

    if(date_db['date'] != date.text):
        Kakao("새 메일: "+title.text)
        sql = "update dates set date = %s"  # 데이터 수정
        val = (date.text)
        curs.execute(sql, val)
        db.commit()

    driver.quit()


# 네이버 메일
def Naver():
    driver = webdriver.Chrome('/chromedriver.exe')
    driver.get(
        'https://nid.naver.com/nidlogin.login?url=http%3A%2F%2Fmail.naver.com%2F')

    # 아이디 입력폼
    tag_id = driver.find_element_by_name('id')
    # 패스워드 입력폼
    tag_pw = driver.find_element_by_name('pw')

    my_id = ''
    my_pwd = ''

    tag_id.click()
    pyperclip.copy(my_id)
    tag_id.send_keys(Keys.CONTROL, 'v')  # 복사 후 붙혀넣기

    tag_pw.click()
    pyperclip.copy(my_pwd)
    tag_pw.send_keys(Keys.CONTROL, 'v')

    # 로그인 버튼 클릭
    driver.find_element_by_id('log.login').click()
    time.sleep(3)

    # 메일 제목
    title = driver.find_element_by_css_selector("strong.mail_title")
    date = driver.find_element_by_class_name("iDate")
    curs = db.cursor(pymysql.cursors.DictCursor)

    curs.execute('SELECT * FROM num;')  # Select 데이터 조회
    num_db = curs.fetchone()

    if(num_db['mailsn'] != date.text):
        Kakao("새 메일: "+title.text)
        sql = "update num set mailsn = %s"  # 데이터 수정
        val = (date.text)
        curs.execute(sql, val)
        db.commit()

    driver.quit()


if __name__ == "__main__":
    while(1):
        print("다음 메일 시작")
        Daum()
        print("네이버 메일 시작")
        Naver()
        time.sleep(60)
