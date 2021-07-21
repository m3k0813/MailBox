from selenium import webdriver
import pymysql
import json
import requests

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
    driver = webdriver.Chrome('./chromedriver.exe')
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
    titles = driver.find_element_by_css_selector('strong.tit_subject')
    # 메일 날짜 추출
    dates = driver.find_element_by_class_name('txt_date')

    curs = db.cursor(pymysql.cursors.DictCursor)

    curs.execute('SELECT * FROM dates;')  # Select 데이터 조회
    date_db = curs.fetchone()

    if(date_db['date'] == dates.text):
        Kakao("새 메일이 없습니다.")
    else:
        Kakao(titles.text)

        sql = "update dates set date = %s"  # 데이터 수정
        val = (dates.text)
        curs.execute(sql, val)
        db.commit()

        driver.quit()


if __name__ == "__main__":
    Daum()
