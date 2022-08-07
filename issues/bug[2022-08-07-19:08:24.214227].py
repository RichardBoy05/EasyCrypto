import webbrowser


class Browser:

    def __init__(self, url):
        self.url = url

    def search(self):
        webbrowser.open(self.url)
