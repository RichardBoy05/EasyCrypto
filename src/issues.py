import json
import time
import requests
import alerts as alt
import tkinter as tk
from github import Github
from logger import Logger
from datetime import datetime
from safedata import Safe as Sd


class Issue:
    """ Defines the structure for objects that represent a GitHub Issue """

    def __init__(self, win: tk.Toplevel, title: str, body: str, labels: list[str], attachments: list[str]):
        self.win = win
        self.OWNER = 'RichardBoy05'
        self.REPO = 'EasyCrypto'
        self.TOKEN = Sd.get_token()
        self.url = f'https://api.github.com/repos/{self.OWNER}/{self.REPO}/import/issues'
        self.headers = {
            'Authorization': f'token {self.TOKEN}',
            'Accept': 'application/vnd.github.golden-comet-preview+json'
        }

        self.title = title
        self.body = body
        self.labels = labels
        self.attachments = attachments
        self.time = datetime.now()
        self.footer = f'\n\n[Generato da **EasyCrypto** il {self.time.strftime("%d/%m/%y alle %H:%M:%S")}'
        self.log = Logger(__name__).default()
        self.log_footer = "\n\n----------------------------------------------------------------------------------\n\n"

        if len(self.attachments) == 0:
            self.content = self.body + self.footer
        else:
            self.content = self.__link_attachment() + self.footer

        self.data = {
            'issue': {'title': self.title,
                      'body': self.content,
                      'labels': self.labels}
        }

    def create_issue(self) -> None:
        """Creates a new issue on the EasyCrypto GitHub repository"""

        content = json.dumps(self.data)

        try:
            response = requests.request('POST', self.url, data=content, headers=self.headers)
        except requests.exceptions.ConnectionError as e:
            alt.issue_connection_error_alert(self.win, e)
            self.log.warning('requests.exceptions.ConnectionError', exc_info=True)
            return

        if response.status_code == 202:
            alt.issue_reported_alert(self.win)
            self.log.info(f'Issue "{self.title}" successfully generated!{self.log_footer}')
        else:
            alt.issue_error_alert(self.win, response)
            self.log.error(f'An error has occured while trying to report an issue.\n{response}{self.log_footer}')

    def __link_attachment(self) -> str:
        """ Adds a link to the end of the Issue body for each of the attachments """

        links = '\n\n**[Allegati]**'

        for i in self.attachments:
            if not self.__upload_file(i):
                continue

            text = f'\n[{i[i.rfind("/") + 1::]}]'
            filelink = f'{self.title}[{self.time}]{i[i.rfind(".")::]})'
            url = f'(https://github.com/{self.OWNER}/{self.REPO}/tree/main/issues/{filelink}'.replace(' ', '-')

            links += (text + url)

        return self.body + links

    def __upload_file(self, attachment: str) -> bool:
        """ Uploads a file to the EasyCrypto repository """
        extension = attachment[attachment.rfind(".")::]
        git_path = f'issues/{self.title}[{self.time}]{extension}'.replace(' ', '-')
        github = Github(self.TOKEN)

        try:
            repo = github.get_repo(f"{self.OWNER}/{self.REPO}")
        except requests.exceptions.ConnectionError:
            self.log.warning('requests.exceptions.ConnectionError', exc_info=True)
            return False

        with open(attachment, 'rb') as file:
            data = file.read()

        if data == b'':
            alt.empty_issue_attachment_alert(self.win, attachment[attachment.rfind('/') + 1::])
            self.log.warning(f'Attempt to attach an empty file to an issue!{self.log_footer}')
            return False

        try:
            # noinspection PyTypeChecker
            repo.create_file(git_path, 'New issue attachment', data, branch='main')
        except requests.exceptions.ConnectionError:
            self.log.warning('requests.exceptions.ConnectionError', exc_info=True)
            return False

        time.sleep(1)
        return True
