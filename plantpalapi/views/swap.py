from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from plantpalapi.models import Swap, PlantPalUser, swap

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

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized plant instance
        """
        #Getting the gamer that is logged in using their aut token
        host = PlantPalUser.objects.get(user=request.auth.user)

        swap = Swap.objects.create(
            title=request.data["title"],
            coverPhoto=request.data["coverPhoto"],
            host=host,
            location=request.data["location"],
            date=request.data["date"],
            time=request.data["time"],
            description=request.data["description"]
        )
        serializer = SwapSerializer(swap)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a swap

        Returns:
        Response -- Empty body with 204 status code
        """
        host = PlantPalUser.objects.get(user=request.auth.user)

        swap = Swap.objects.get(pk=pk)
        swap.title = request.data["title"]
        swap.coverPhoto = request.data["coverPhoto"]
        swap.host = host
        swap.location = request.data["location"]
        swap.date = request.data["date"]
        swap.time = request.data["time"]
        swap.description = request.data["description"]

        swap.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        swap = Swap.objects.get(pk=pk)
        swap.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SwapSerializer(serializers.ModelSerializer):
    """"JSON serializer for swaps
    """
    class Meta:
        model = Swap
        fields = ('id', 'title', 'coverPhoto', 'host', 'location', 'date', 'time', 'description', 'attendees')
        depth = 1