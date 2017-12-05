import os

from selenium import webdriver

from post_process import post_process


class Crawler:
    def __init__(self):
        self.driver = None

    def load_chrome(self, chrome_driver, chrome=None):
        chrome_path = os.path.join(os.getcwd(), chrome_driver)
        options = webdriver.ChromeOptions()

        if chrome is not None:
            options.binary_location = os.path.join(os.getcwd(), chrome)
            # options.binary_location = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'

        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        options.add_argument('single-process')
        options.add_argument('no-sandbox')
        driver = webdriver.Chrome(chrome_path, chrome_options=options)

        self.driver = driver

    def load_phantom(self, phantom):
        phantom_path = os.path.join(os.getcwd(), phantom)
        driver = webdriver.PhantomJS(phantom_path,
                                     service_log_path=os.path.devnull)

        self.driver = driver

    def crawling(self, article_page_num):
        """
        /ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=1
        /ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=2
        /ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=3
        /ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=4
        /ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=5
        /ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=6
        /ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=7
        /ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=8
        /ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=9
        /ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=10
        /ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L&search.questionTab=A&search.totalCount=151&search.page=11

        doc = document.getElementById('cafe_main').contentDocument;
        t = doc.getElementsByClassName("Nnavi")[0]
        td = t.getElementsByTagName("td")[3]
        td.getElementsByTagName("a")[0].click()
        """

        assert self.driver is not None

        # self.driver.implicitly_wait(3)
        self.driver.get('http://cafe.naver.com/joonggonara.cafe')
        # 맥북/노트북 탭으로 들어감

        if type(self.driver) == webdriver.Chrome:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        self.driver.find_element_by_id('menuLink334').click()
        script = """
        window.myFunc = function() {
            let doc = document.getElementById('cafe_main').contentDocument;
            let article_list = doc.getElementsByName('ArticleList')[0];
            let articles = article_list.children[0].getElementsByTagName('tbody')[0];
            return articles.innerText;
        };
        """.replace('\n', '').replace('let', 'var')

        self.driver.execute_script(script)
        text = self.driver.execute_script('return window.myFunc();')
        self.driver.close()

        return text


if __name__ == '__main__':
    crawler = Crawler()
    crawler.load_chrome(os.path.join(os.getcwd(), 'chromedriver-mac'))
    text = crawler.crawling()
    text = post_process(text)
    print(text)
