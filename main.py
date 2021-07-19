from selenium import webdriver
import pymysql
import json
import requests

Tmp = '21.03.16 15:40'

Kakao_Token = "BAJa80iTuB5J238kT_Ukj9T8uSjGcMdMmP3JMworDSAAAAF6vYPC8g"


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


def Daum():
    driver = webdriver.Chrome('C:/Users/M/PycharmProjects/chromedriver.exe')
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

    global Tmp

    if(Tmp == dates.text):
        print("새 메일이 없습니다.")
        Kakao("새 메일이 없습니다.")
    else:
        print(titles.text)
        Kakao(titles.text)
        Tmp = dates.text

    driver.quit()


if __name__ == "__main__":
    Daum()
    Daum()
