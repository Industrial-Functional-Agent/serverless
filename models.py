class Post(object):
    def __init__(self, no, title):
        self.no = no
        self.title = title

    def __str__(self):
        return "{}\t{}".format(self.no, self.title)
