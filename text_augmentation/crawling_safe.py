from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys


def getdata(startpage=1, count=100, outfilename="1_100.txt"):
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(3)
    # driver.maximize_window()
    # 시작페이지
    url = 'https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/sfc/dis/disasterMsgList.jsp?menuSeq=679'
    driver.get(url)

    # page 이동
    driver.execute_script("document.getElementById('bbs_page').value = " + str(startpage) + ";")
    # driver.find_element_by_css_selector("a.go_btn").click()
    driver.find_element_by_css_selector("a.go_btn").send_keys(Keys.ENTER)
    time.sleep(0.5)

    # 목록으로 이동
    driver.find_elements_by_id('bbs_tr_0_bbs_title')[0].click()
    time.sleep(0.5)

    out = open(outfilename, "w", encoding="utf-8")
    errorcount = 0

    valid_word = ["방문", "이용", "탑승"]
    for i in range(count):
        try:
            replys = driver.find_element_by_css_selector('div.boardView')
            tlist = replys.find_elements_by_id('sj')
            title = tlist[0].text
            text = replys.find_elements_by_id('cn')[0].text
            text = text.replace("\n", "\t")
            if "-송출지역-" in text:    # 오직 문자내용만 추출
                text = text[:text.index("-송출지역-")]
            print(i, errorcount, title, text)
            if (len(title) == 0):   #길이0은 무시
                break
            #out.write(title)
            for w in range(3):
                if valid_word[w] in text:
                    out.write(text)
                    out.write("\n")
                    break

            replys = driver.find_element_by_css_selector('ul.boardView_listWrap')

            # 다음 목록
            replys.find_elements_by_id('bbs_gubun')[0].click()
            time.sleep(0.1)
        except:
            errorcount += 1

    out.close()
    driver.close()


####### 사용법 예시
getdata(startpage=361, count=200, outfilename='disaster0717_3601-3800.txt')
