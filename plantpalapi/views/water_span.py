"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from plantpalapi.models import WaterSpan


class WaterSpanView(ViewSet):
    """Plant pal water span view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single water span
        Returns:
            Response -- JSON serialized water span
        """
        try:
            water_span = WaterSpan.objects.get(pk=pk)
            serializer = WaterSpanSerializer(water_span)
            return Response(serializer.data)
        except WaterSpan.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all water spans

        Returns:
            Response -- JSON serialized list of water spans
        """
        water_span = WaterSpan.objects.all()
        serializer = WaterSpanSerializer(water_span, many=True)
        return Response(serializer.data)

class WaterSpanSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = WaterSpan
        fields = ('id', 'label')
        depth = 1