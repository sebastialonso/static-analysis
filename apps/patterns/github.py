from github import Github

from django.conf import settings

def make_client():
    g = Github(settings.GITHUB_TOKEN)
    return g


_client = None


def search_issues_with_query(query: str):
    _client = make_client()
    return list(_client.search_issues(query=query))


def get_repo():
    _client = make_client()
    return _client.get_repo(settings.BACKEND_REPO_SLUG)