import time 
from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options




def crawling(keyword, numImages, result_dir):
    #크롬 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option("detach",True)

    # 웹드라이버 실행
    driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver')

    # 이미지 검색 url
    url = 'https://pixabay.com/ko/photos/search/'

    # 이미지 검색하기
    driver.get(url + keyword)

    # 이미지 검색 영역의 xpath
    xpath = '//*[@id="app"]/div[1]/div/div[2]/div[4]'
    # //*[@id="app"]/div[1]/div/div[2]/div[3]/div/div
    try:
        # 쿠키 허용 팝업이 나타날 때까지 대기
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        accept_button = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
        accept_button.click()
        time.sleep(4)
    except:
        print("쿠키 허용 팝업이 나타나지 않았습니다.")

    # 100장 이하 이미지를 요구받은 경우
    if numImages <= 100:
        image_area = driver.find_element_by_xpath(xpath)
        image_elements = image_area.find_elements_by_tag_name("img")
        for i in range(numImages):
            x2_image_url = image_elements[i].get_attribute("srcset").split(" ")[2]
            driver.execute_script("window.open(' ');")
            new_tab = driver.window_handles[-1]
            driver.switch_to.window(new_tab)
            driver.get(x2_image_url)
            image_element = driver.find_element_by_tag_name("img")
            image_element.screenshot(result_dir + "/" + str(time.time()) + ".png")
            driver.close()
            original_tab = driver.window_handles[0]
            driver.switch_to.window(original_tab)

    # 100장 이상을 요구받은 경우
    else:
        while numImages > 0:
            image_area = driver.find_element_by_xpath(xpath)
            image_elements = image_area.find_elements_by_tag_name("img")
            for i in range(len(image_elements)):
                x2_image_url = image_elements[i].get_attribute("srcset").split(" ")[2]
                driver.execute_script("window.open(' ');")
                new_tab = driver.window_handles[-1]
                driver.switch_to.window(new_tab)
                driver.get(x2_image_url)
                image_element = driver.find_element_by_tag_name("img")
                image_element.screenshot(result_dir + "/" + str(time.time()) + ".png")
                driver.close()
                original_tab = driver.window_handles[0]
                driver.switch_to.window(original_tab)

                numImages -= 1
                if i == len(image_elements) - 1:
                    next_button = driver.find_element_by_partial_link_text("다음 페이지")
                    next_button.click()
                    time.sleep(3)