class RequestBuilder:
    base_url = "http://recruit-recruiters-scraper.herokuapp.com/jobs?"

    def __init__(self):
        self.url = RequestBuilder.base_url

    def title(self, title):
        self.url += ("title=%s" % title)
        return self

    def location(self, location):
        self.url += ("&location=%s" % location)
        return self

    def page(self, page):
        self.url += ("&page=%s" % page)
        return self

    def build(self):
        return self.url
