# apihandle/views.py

# apihandle/views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Match, FilterCriteria
from .serializers import MatchSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    @action(detail=False, methods=['get'])
    def filtered_matches(self, request):
        filter_criteria = FilterCriteria.objects.all()
        leagues = [criteria.name for criteria in filter_criteria]
        matches = Match.objects.filter(league__name__in=leagues)
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

