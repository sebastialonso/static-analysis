import json
import arrow
from collections import OrderedDict
from typing import List, Dict
from django.db import models
from itertools import groupby
from .utils import epoch_to_datetime_string


class OcurrenceReportManager(models.Manager):
    def aggregate_last_of_day_from_apps(self, apps: List[str]):
        reports = list(self.filter(app_name__in=apps, last_of_day=True))
        accum = OrderedDict()
        reports = sorted(reports, key=lambda report: arrow.get(report.commited_epoch).format('YYYY-MM-DD'))
        for date, grouped_reports in groupby(reports, lambda report: arrow.get(report.commited_epoch).format('YYYY-MM-DD')):
            # At this point we should have reports from all apps in `apps` for the given date
            accum[date] = sum([report.total for report in list(grouped_reports)])
        return accum

class OcurrenceReport(models.Model):
    commit = models.CharField(null=False, max_length=40)
    _total = models.IntegerField(null=False)
    _ocurrences = models.TextField(null=False)
    commited_epoch = models.IntegerField(null=True)
    last_of_day = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    app_name = models.CharField(max_length=20, null=False, default="undetermined")

    objects = OcurrenceReportManager()

    @property
    def ocurrences(self) -> List[str]:
        raw_ocurrences = getattr(self, "_ocurrences")
        return json.loads(raw_ocurrences)

    @ocurrences.setter
    def ocurrences(self, value: List[str]) -> None:
        dumped_value = json.dumps(value)
        setattr(self, "_ocurrences", dumped_value)
        setattr(self, "_total", len(value))


    @property
    def total(self) -> List[str]:
        return getattr(self, "_total")

    @total.setter
    def total(self, value: int) -> None:
        setattr(self, "_total", value)

    def __str__(self):
        committed_at = epoch_to_datetime_string(epoch=self.commited_epoch)
        return f"<{self.commit} App:{self.app_name} Count:{self._total} {committed_at}>"

    class Meta:
        unique_together = ['commit', 'app_name']