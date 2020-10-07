import git
import os
import subprocess
from contextlib import contextmanager

from django.conf import settings


def repo_exists():
    try:
        git.Repo(_study_repo_path())
        return True
    except git.InvalidGitRepositoryError:
        return False


def get_repo():
    return git.Repo(_study_repo_path())


def clone_repo():
    repo = git.Repo.clone_from(settings.REPO_GIT_URL, _study_repo_path(), branch=settings.REPO_DEFAULT_BRANCH)
    return repo


def pull_repo(repo):
    origin = repo.remotes.origin
    origin.pull()


def delete_repo():
    subprocess.run(["rm", "-rf", _study_repo_path()])


def _study_repo_path():
    return os.path.join(os.getcwd(), settings.REPO_CLONE_PATH)


def get_active_branch_name_from_repo(path):
    repo = git.Repo(path)
    return repo.active_branch.name



@contextmanager
def repo_at(commit, clone=False, always_pull=True, force_delete=True):

    if clone or not repo_exists():
        repo = clone_repo()
    else:
        repo = get_repo()
        # Force pull repo
        if always_pull:
            pull_repo(repo)

    if commit:
        # Reset head to the specific commmit
        repo = repo.head.reset(commit=commit, index=True, working_tree=True)

    yield repo

    if force_delete:
        delete_repo()
