from github import Github, GithubException
from dotenv import load_dotenv
import os
from pprint import pprint
from datetime import datetime, timedelta
load_dotenv(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot\Antipetros_Discord_Bot\.env")
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO = 'official-antistasi-community/A3-Antistasi'
NOW = datetime.now()


def get_issues():
    github = Github(login_or_token=GITHUB_TOKEN)
    user = github.get_user()
    repo = github.get_repo(REPO)
    _time = NOW - timedelta(days=2)

    _issues = repo.get_issues(state='open', since=_time)
    for issue in _issues:
        print(issue.title)


if __name__ == '__main__':
    get_issues()
