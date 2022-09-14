from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from plantpalapi.models import Plant, SunType, WaterSpan, PlantPalUser

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

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized plant instance
        """
        #Getting the gamer that is logged in using their aut token
        user = PlantPalUser.objects.get(user=request.auth.user)
        #Get game type object from data base to make sure game type user is trying to add exists
        #Data passed in from the client is held in the request.data dictionary
        #Whichever keys are used on the request.data must match what the client is passing to the server.
        sun_type = SunType.objects.get(pk=request.data["sunType"])
        water_span = WaterSpan.objects.get(pk=request.data["waterSpanId"])

        plant = Plant.objects.create(
            userId=user,
            plantPhoto=request.data["plantPhoto"],
            name=request.data["name"],
            water=request.data["water"],
            waterSpanId=water_span,
            sunType=sun_type,
            lastWatered=request.data["lastWatered"],
            petToxic=request.data["petToxic"],
            notes=request.data["notes"]
        )
        serializer = PlantSerializer(plant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PlantSerializer(serializers.ModelSerializer):
    """"JSON serializer for plants
    """
    class Meta:
        model = Plant
        fields = ('id', 'plantPhoto', 'name', 'water', 'waterSpanId', 'sunType', 'lastWatered', 'petToxic', 'notes')
        depth = 3