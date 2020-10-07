from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response

from .serializers import OcurrenceSerializer
from .models import OcurrenceReport
from .services import create_commit_report


class OcurrenceViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = OcurrenceSerializer

    def get_queryset(self):
        return OcurrenceReport.objects.all()

    def retrieve(self, request, pk):
        report = self.get_object()
        body = self.serializer_class(report)
        return Response(body.data)

