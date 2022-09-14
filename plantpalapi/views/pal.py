from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from plantpalapi.models import PlantPalUser


class PlantPalView(ViewSet):
    """Pals view - list of plant pal users
    """

    def retrieve(self, request, pk):
        """Handle GET requests for single pal
        """
        try:
            pal = PlantPalUser.objects.get(pk=pk)
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

class PalSerializer(serializers.ModelSerializer):
    """"JSON serializer for plant pal user
    """
    class Meta:
        model = PlantPalUser
        fields = ('id', 'user', 'profilePic', 'address', 'bio')
        depth = 2