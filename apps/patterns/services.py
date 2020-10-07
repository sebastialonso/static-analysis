import arrow
from datetime import datetime
from typing import Optional
from apps.patterns.git import repo_at
from .models import OcurrenceReport
from .analyzer import analyze_repo_with_pattern


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


def to_arrow(in_datetime: datetime) -> arrow.Arrow:
    return arrow.Arrow(
        year=in_datetime.year,
        month=in_datetime.month,
        day=in_datetime.day,
        hour=in_datetime.hour,
        minute=in_datetime.minute,
        second=in_datetime.second
    )
