from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from plantpalapi.models import Swap, PlantPalUser

class SwapView(ViewSet):
    """Swap view - list of plant pal swaps
    """

    def retrieve(self, request, pk):
        """Handle GET requests for single swap
        """
        try:
            swap = Swap.objects.get(pk=pk)
            serializer = SwapSerializer(swap)
            return Response(serializer.data)
        except Swap.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all swaps
        """
        swaps = Swap.objects.all()
        host = PlantPalUser.objects.get(user=request.auth.user)
        serializer = SwapSerializer(swaps, many=True)
        return Response(serializer.data)

class SwapSerializer(serializers.ModelSerializer):
    """"JSON serializer for swaps
    """
    class Meta:
        model = Swap
        fields = ('id', 'title', 'coverPhoto', 'host', 'location', 'date', 'time', 'description', 'attendees')
        depth = 1