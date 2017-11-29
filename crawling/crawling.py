import os
import time

from selenium import webdriver


def load_chrome(chromedriver, chrome):
    chrome_path = os.path.join(os.getcwd(), chromedriver)
    # Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
    options = webdriver.ChromeOptions()
    options.binary_location = os.path.join(os.getcwd(), chrome)
    # options.binary_location = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_argument('single-process')
    options.add_argument('no-sandbox')
    driver = webdriver.Chrome(chrome_path, chrome_options=options)
    return driver


def crawling():
    start = time.time()
    phantom_path = os.path.join(os.getcwd(), 'phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    # driver.implicitly_wait(3)
    # PhantomJS의 경우 | 아까 받은 PhantomJS의 위치를 지정해준다.
    driver = webdriver.PhantomJS(phantom_path,
                                 service_log_path=os.path.devnull)

    driver.get('http://cafe.naver.com/joonggonara.cafe')
    # 맥북/노트북 탭으로 들어감
    # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    driver.find_element_by_id('menuLink334').click()
    script = """
    window.myFunc = function() {
        let doc = document.getElementById('cafe_main').contentDocument;
        let article_list = doc.getElementsByName('ArticleList')[0];
        let articles = article_list.children[0].getElementsByTagName('tbody')[0];
        return articles.innerText;
    };
    """.replace('\n', '').replace('let', 'var')

    driver.execute_script(script)
    text = driver.execute_script('return window.myFunc();')
    print(text)
    driver.close()
    print('total time is {}'.format(time.time() - start))

    return text


def post_process(text):
    text.split('\n')


if __name__ == '__main__':
    crawling()
