import json
from typing import List, Dict
from django.db import models


class ReportManager(models.Manager):
    def create_report(self, payload: Dict):
        ocurrences = payload.get('ocurrences', [])
        payload.update(total=len(ocurrences))
        report = self.create(**payload)
        return report


class OcurrenceReport(models.Model):
    commit = models.CharField(null=False, max_length=40)
    _total = models.IntegerField(null=False)
    _ocurrences = models.TextField(null=False)
    commited_epoch = models.IntegerField(null=True)
    last_of_day = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReportManager()

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
        return f"<{self.id} {self.commit} {self._total}>"