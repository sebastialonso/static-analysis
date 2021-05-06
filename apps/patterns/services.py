import arrow
from datetime import datetime
import git
from typing import Optional, List
from apps.patterns.git import repo_at
from .models import OcurrenceReport
from .analyzer import analyze_repo_with_pattern
from ..utils import to_arrow

def create_commit_report(commit: Optional[str] = None, force_delete=True, always_pull=True):
    with repo_at(commit, force_delete=force_delete, always_pull=always_pull) as repo:

        hits = analyze_repo_with_pattern(pattern="apps.catalog.models")

        head_commit = repo.head.commit
        commit_arrow = to_arrow(head_commit.committed_datetime)

        args = dict(
            ocurrences=hits,
            commit=head_commit.hexsha,
            commited_epoch=commit_arrow.timestamp
        )
        report = OcurrenceReport.objects.create_report(args)
        return report


def report_ocurrence(study_app: str, ignore_paths: List[str], commit: str = None, verbose: bool = False):
    with repo_at(commit=commit, force_delete=False, always_pull=True) as repo:

        if repo.__class__ == git.HEAD:
            current_commit = repo.commit
        if repo.__class__ == git.Repo:
            current_commit = repo.head.commit

        try:
            report = OcurrenceReport.objects.filter(commit=current_commit.hexsha,
                                                    app_name=study_app).get()
            if verbose:
                print(f"Report found for {current_commit.hexsha}. No analysis needed!")

        except OcurrenceReport.DoesNotExist:
            if verbose:
                print(f"Analyzing commit {current_commit.hexsha}")
            pattern = f"apps.{study_app}.models"
            hits = analyze_repo_with_pattern(study_app=study_app, pattern=pattern, ignore_paths=ignore_paths)

            payload = dict(
                app_name=study_app,
                ocurrences=hits,
                commit=current_commit.hexsha,
                commited_epoch=to_arrow(current_commit.committed_datetime).timestamp,
            )
            report = OcurrenceReport.objects.create(**payload)

        return report

