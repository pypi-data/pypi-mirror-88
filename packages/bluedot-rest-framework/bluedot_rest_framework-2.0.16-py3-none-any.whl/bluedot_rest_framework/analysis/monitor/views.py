from rest_framework.viewsets import ModelViewSet
from .models import AnalysisMonitor
from .serializers import AnalysisMonitorSerializer


class AnalysisMonitorView(ModelViewSet):
    model_class = AnalysisMonitor
    serializer_class = AnalysisMonitorSerializer
    permission_classes = []
