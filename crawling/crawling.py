import os
import time

from selenium import webdriver


def main():
    start = time.time()
    home = os.path.expanduser('~')
    chrome_path = os.path.join(home, 'practice', 'chromedriver')
    phantom_path = os.path.join(home, 'practice', 'phantomjs-2.1.1-macosx/bin/phantomjs')
    # Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
    # driver = webdriver.Chrome(chrome_path)
    # driver.implicitly_wait(3)
    # PhantomJS의 경우 | 아까 받은 PhantomJS의 위치를 지정해준다.
    driver = webdriver.PhantomJS(phantom_path)

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


if __name__ == '__main__':
    main()
