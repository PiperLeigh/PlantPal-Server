from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from plantpalapi.models import Swap, PlantPalUser
import uuid
import base64
from django.core.files.base import ContentFile
from rest_framework.decorators import action


class SwapView(ViewSet):
    """Swap view - list of plant pal swaps
    """

    def retrieve(self, request, pk):
        """Handle GET requests for single swap
        """
        try:
            swap = Swap.objects.get(pk=pk)
            pal = PlantPalUser.objects.get(user=request.auth.user)
            swap.attending = pal in swap.attendees.all()
            serializer = SwapSerializer(swap)
            return Response(serializer.data)
        except Swap.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all swaps
        """
        swaps = Swap.objects.all()
        pal = PlantPalUser.objects.get(user=request.auth.user)
        for swap in swaps:
            swap.attending = pal in swap.attendees.all()
        serializer = SwapSerializer(swaps, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized plant instance
        """
        # Getting the gamer that is logged in using their aut token
        host = PlantPalUser.objects.get(user=request.auth.user)
        format, imgstr = request.data["coverPhoto"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr),
                           name=f'{uuid.uuid4()}.{ext}')

        swap = Swap.objects.create(
            title=request.data["title"],
            coverPhoto=data,
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
        swap = Swap.objects.get(pk=pk)
        host = PlantPalUser.objects.get(user=request.auth.user)
        try:
            format, imgstr = request.data["coverPhoto"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
                               name=f'{uuid.uuid4()}.{ext}')
            swap.coverPhoto = data  # matches above
        except:
            pass
        swap.title = request.data["title"]
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

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        pal = PlantPalUser.objects.get(user=request.auth.user)
        swap = Swap.objects.get(pk=pk)
        swap.attendees.add(pal)
        return Response({'message': 'Pal added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""
        pal = PlantPalUser.objects.get(user=request.auth.user)
        swap = Swap.objects.get(pk=pk)
        swap.attendees.remove(pal)
        return Response({'message': 'Pal left'}, status=status.HTTP_204_NO_CONTENT)


class SwapSerializer(serializers.ModelSerializer):
    """"JSON serializer for swaps
    """
    class Meta:
        model = Swap
        fields = ('id', 'title', 'coverPhoto', 'host', 'location', 'date', 'time', 'description', 'attendees',
                  'attending')
        depth = 2
