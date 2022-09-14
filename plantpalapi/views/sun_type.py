"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from plantpalapi.models import SunType


class SunTypeView(ViewSet):
    """Plant pal sun type view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single sun type
        Returns:
            Response -- JSON serialized sun type
        """
        try:
            sun_type = SunType.objects.get(pk=pk)
            serializer = SunTypeSerializer(sun_type)
            return Response(serializer.data)
        except SunType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all sun types

        Returns:
            Response -- JSON serialized list of water spans
        """
        sun_type = SunType.objects.all()
        serializer = SunTypeSerializer(sun_type, many=True)
        return Response(serializer.data)

class SunTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = SunType
        fields = ('id', 'label')
        depth = 1