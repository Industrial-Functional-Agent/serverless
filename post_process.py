import logging
import re

from aws_clients import DynamoDBClient
from models import Post


dynamo_db_client = DynamoDBClient()


def post_process(text):
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
            posts.append(Post(int(article_number), article_title))

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    old_latest_post_id = dynamo_db_client.get_latest_post_id()
    logger.info("old_latest_post_id: {}".format(old_latest_post_id))

    if len(posts) > 0:
        new_latest_post_id = max([post.number for post in posts])
        logger.info("new_latest_post_id: {}".format(new_latest_post_id))
        dynamo_db_client.update_latest_post_id(new_latest_post_id)

    return [post for post in posts if post.number > old_latest_post_id]
