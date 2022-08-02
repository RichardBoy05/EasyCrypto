import json
import requests
import alerts as alt
from github import Github
from datetime import datetime
from safedata import Safe as Sd


class Issue:
    def __init__(self, title: str, body: str, labels: list[str], attachments: list[str]):
        self.OWNER = 'RichardBoy05'
        self.REPO = 'EasyCrypto'
        self.TOKEN = Sd.git_token

        self.title = title
        self.body = body
        self.labels = labels
        self.attachments = attachments
        self.time = datetime.now()

        self.url = f'https://api.github.com/repos/{self.OWNER}/{self.REPO}/import/issues'
        self.headers = {
            'Authorization': f'token {self.TOKEN}',
            'Accept': 'application/vnd.github.golden-comet-preview+json'
        }

        if len(self.attachments) == 0:
            content = self.body
        else:
            content = self.__link_attachment()

        self.data = {
            'issue': {'title': self.title,
                      'body': content,
                      'labels': self.labels}
        }

    def create_issue(self):
        """Creates a new issue on the EasyCrypto GitHub repository"""

        content = json.dumps(self.data)

        try:
            response = requests.request('POST', self.url, data=content, headers=self.headers)
        except requests.exceptions.ConnectionError as e:
            alt.issue_connection_error_alert(e)
            return

        if response.status_code == 202:
            alt.issue_reported_alert()
        else:
            alt.issue_error_alert(response)

    def __link_attachment(self):
        """Adds a link to the end of the issue body for every one of the attachments"""

        content = self.body + '\n\n**[Allegati]**'

        for i in self.attachments:
            if not self.__upload_file(i):
                continue

            content += f'\n[{i[i.rfind("/")+1::]}](https://github.com/RichardBoy05/EasyCrypto/tree/main/issues/{self.title}[{self.time}]{i[i.rfind(".")::]})'
            content = content.replace(' ', '-')

        return content

    def __upload_file(self, attachment):
        """Uploads a file to the EasyCrypto repository at 'issues/{attachment}"""

        git_path = f'issues/{self.title}[{self.time}]{attachment[attachment.rfind(".")::]}'.replace(' ', '-')
        github = Github(self.TOKEN)
        repo = github.get_repo("%s/%s" % (self.OWNER, self.REPO))

        with open(attachment, 'rb') as file:
            data = file.read()

        if data == b'':
            return False

        # noinspection PyTypeChecker
        repo.create_file(git_path, 'New issue attachment', data, branch='main')  # Add, commit and push branch
        return True
