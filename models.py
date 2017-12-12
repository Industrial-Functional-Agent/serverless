from pynamodb.models import Model
from pynamodb.attributes import NumberAttribute, UnicodeAttribute


class Post(Model):
    class Meta:
        table_name = 'Post'
        region = 'ap-northeast-2'

    @staticmethod
    def get_latest_number(menu_link):
        return list(Post.query(hash_key=menu_link, scan_index_forward=False, limit=1))[0].number

    menu_link = UnicodeAttribute(hash_key=True)  # menuLink334
    number = NumberAttribute(range_key=True)
    title = UnicodeAttribute()

    # def __str__(self):
    #     return 'http://cafe.naver.com/joonggonara/{}\t{}'.format(self.number, self.title)
