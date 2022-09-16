from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from plantpalapi.models import Plant, SunType, WaterSpan, PlantPalUser
import uuid
import base64
from django.core.files.base import ContentFile



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

        user = PlantPalUser.objects.get(user=request.auth.user)
        sun_type = SunType.objects.get(pk=request.data["sunType"])
        water_span = WaterSpan.objects.get(pk=request.data["waterSpanId"])
        format, imgstr = request.data["plantPhoto"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')

        plant = Plant.objects.create(
            userId=user,
            plantPhoto=data,
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

    def update(self, request, pk):
        """Handle PUT requests for a plant

        Returns:
        Response -- Empty body with 204 status code
        """

        format, imgstr = request.data["plantPhoto"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')

        plant = Plant.objects.get(pk=pk)
        plant.plantPhoto = data
        plant.name = request.data["name"]
        plant.water = request.data["water"]
        plant.lastWatered = request.data["lastWatered"]
        plant.petToxic = request.data["petToxic"]
        plant.notes = request.data["notes"]

        sunType = SunType.objects.get(pk=request.data["sunType"])
        plant.sunType = sunType
        waterSpanId = WaterSpan.objects.get(pk=request.data["waterSpanId"])
        plant.waterSpanId = waterSpanId
        plant.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        plant = Plant.objects.get(pk=pk)
        plant.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PlantSerializer(serializers.ModelSerializer):
    """"JSON serializer for plants
    """
    class Meta:
        model = Plant
        fields = ('id', 'plantPhoto', 'name', 'water', 'waterSpanId', 'sunType', 'lastWatered', 'petToxic', 'notes')
        depth = 3