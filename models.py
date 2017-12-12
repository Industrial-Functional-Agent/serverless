class Post(object):
    def __init__(self, number, title):
        self.number = number
        self.title = title

    def __str__(self):
        return 'http://cafe.naver.com/joonggonara/{}\t{}'.format(self.number, self.title)
