from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from plantpalapi.models import Plant, SunType, WaterSpan

class PlantView(ViewSet):
    """Plant view - list of plants
    """

    def retrieve(self, request, pk):
        """Handle GET requests for single plant


            Returns:
            Response -- JSON serialized plant
        """
        try:
            plant = Plant.objects.get(pk=pk)
            serializer = PlantSerializer(plant)
            return Response(serializer.data)
        except Plant.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all plants
        """
        plants = Plant.objects.all()
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)


class PlantSerializer(serializers.ModelSerializer):
    """"JSON serializer for plants
    """
    class Meta:
        model = Plant
        fields = ('id', 'plantPhoto', 'name', 'water', 'waterSpanId', 'sunType', 'lastWatered', 'petToxic', 'notes')
        depth = 3