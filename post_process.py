import re

from models import Post


def post_process(text):
    delete_useless_korean = text.replace('퍼스나콘/아이디', '')
    split_by_article = re.split(r'\t[0-9]+\n', delete_useless_korean)

    split_by_tab = [article.replace('\n\n', '').split('\t') for article in split_by_article]

    result = []
    for article in split_by_tab[:-1]:
        article_number = article[0]
        article_title = article[1]

        is_macbook = article_title.find('맥북') != -1 or re.findall('[mM][aA][cC]',
                                                                  article_title)
        is_pro = article_title.find('프로') != -1 or re.findall('[pP][rR][oO]',
                                                              article_title)

        if is_macbook and is_pro:
            result.append(Post('http://cafe.naver.com/joonggonara/{}'.format(article_number), article_title))

    return result
