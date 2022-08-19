
# built-in modules
import webbrowser


class Browser:
    """ Searches the URL (given as a parameter) using the default browser """

    def __init__(self, url):
        self.url = url

    def search(self) -> None:
        webbrowser.open(self.url)
