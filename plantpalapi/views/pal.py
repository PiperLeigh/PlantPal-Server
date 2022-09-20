from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from plantpalapi.models import PlantPalUser
import uuid
import base64
from django.core.files.base import ContentFile

class PlantPalView(ViewSet):
    """Pals view - list of plant pal users
    """

    def retrieve(self, request, pk):
        """Handle GET requests for single pal
        """
        try:
            pal = PlantPalUser.objects.get(user=request.auth.user)
            serializer = PalSerializer(pal)
            return Response(serializer.data)
        except PlantPalUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all pals
        """
        pals = PlantPalUser.objects.all()
        serializer = PalSerializer(pals, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        
        user = PlantPalUser.objects.get(user=request.auth.user)
        format, imgstr = request.data["profilePic"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')

        pal = PlantPalUser.objects.create(
            user=user,
            profilePic=data,
            address=request.data["address"],
            bio=request.data["bio"]
        )
        serializer = PalSerializer(pal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
        Response -- Empty body with 204 status code
        """
        pal = PlantPalUser.objects.get(user=request.auth.user)
        try:
            format, imgstr = request.data["profilePic"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
                               name=f'{uuid.uuid4()}.{ext}')
            pal.profilePic = data  # matches above
        except:
            pass

        pal.address = request.data["address"]
        pal.bio = request.data["bio"]

        pal.save()
        request.auth.user.email = request.data["email"]
        request.auth.user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PalSerializer(serializers.ModelSerializer):
    """"JSON serializer for plant pal user
    """
    class Meta:
        model = PlantPalUser
        fields = ('id', 'user', 'profilePic', 'address', 'bio')
        depth = 2
