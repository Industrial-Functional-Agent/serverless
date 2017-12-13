import logging
import os
import re

from selenium import webdriver

from models import Post


class Crawler:
    def __init__(self, menu_link='menuLink334'):
        self.driver = None
        self.menu_link = menu_link

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

    def crawling(self):
        assert self.driver is not None

        self.driver.get('http://cafe.naver.com/joonggonara.cafe')
        if type(self.driver) == webdriver.Chrome:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        self.driver.find_element_by_id(self.menu_link).click()
        script = """
        window.myFunc = function() {
            let doc = document.getElementById('cafe_main').contentDocument;
            let article_list = doc.getElementsByName('ArticleList')[0];
            let articles = article_list.children[0].getElementsByTagName('tbody')[0];
            return articles.innerText;
        };
        """.replace('\n', '').replace('let', 'var')

        post = []
        for i in range(10):
            self.move_article_page(i)
            self.driver.execute_script(script)
            text = self.driver.execute_script('return window.myFunc();')
            post += self.post_process(text)

        self.driver.close()
        return post

    def move_article_page(self, article_page_num=1):
        script = """
        window.myFunc = function(i) {
            let doc = document.getElementById('cafe_main').contentDocument;
            let t = doc.getElementsByClassName("Nnavi")[0];
            let td = t.getElementsByTagName("td")[i];
            td.getElementsByTagName("a")[0].click();
        };
        """.replace('\n', '').replace('let', 'var')

        self.driver.execute_script(script)
        self.driver.execute_script('window.myFunc({});'.format(article_page_num))

    def post_process(self, text):
        delete_useless_korean = text.replace('퍼스나콘/아이디', '')
        split_by_article = re.split(r'\t[0-9]+\n', delete_useless_korean)

        split_by_tab = [article.replace('\n\n', '').split('\t') for article in split_by_article]

        posts = []
        for article in split_by_tab[:-1]:
            article_number = article[0]
            article_title = article[1]

            is_macbook = article_title.find('맥북') != -1 or re.findall('[mM][aA][cC]',
                                                                      article_title)
            is_pro = article_title.find('프로') != -1 or re.findall('[pP][rR][oO]',
                                                                  article_title)

            if is_macbook and is_pro:
                posts.append(Post(menu_link=self.menu_link,
                                  number=int(article_number),
                                  title=article_title))

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        old_latest_post_id = Post.get_latest_number(menu_link=self.menu_link)
        logger.info("old_latest_post_id: {}".format(old_latest_post_id))

        if len(posts) > 0:
            new_latest_post_id = max([post.number for post in posts])
            logger.info("new_latest_post_id: {}".format(new_latest_post_id))
            for post in posts:
                if post.number > old_latest_post_id:
                    post.save()

        return [post for post in posts if post.number > old_latest_post_id]


if __name__ == '__main__':
    crawler = Crawler()
    crawler.load_phantom(os.path.join(os.getcwd(),
                                      'phantomjs',
                                      'phantomjs-2.1.1-macosx',
                                      'bin',
                                      'phantomjs'))
    text = str(crawler.crawling())
    print(text)
