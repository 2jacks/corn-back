from .models import Farmer, Field, Research, AOI, Indexes
from accounts.models import User
import os
import json
from utils.geoprocessing import calc_stats
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import FieldSerializer, ResearchSerializer, AOISerializer
from django.http import Http404, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings


class FieldList(APIView):
    def get(self, request, username):
        user_id = User.objects.get(username=username)
        serializer = FieldSerializer(Field.objects.filter(owner=user_id), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FieldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FieldDetail(APIView):
    def get_object(self, username, fieldId):
        try:
            return Field.objects.get(id=fieldId)
        except Field.DoesNotExist:
            raise Http404

    def get(self, request, username, pk, format=None):
        snippet = self.get_object(pk)
        serializer = FieldSerializer(snippet)
        return Response(serializer.data)

    def delete(self, request, username, pk, format=None):
        field = self.get_object(pk)
        field.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResearchList(APIView):
    def get(self, request, username, fieldId, format=None):
        researches = Research.objects.filter(field_id=fieldId)
        serializer = ResearchSerializer(researches, many=True)
        return Response(data=serializer.data)


class ResearchDetail(APIView):
    def get_object(self, pk):
        try:
            return Research.objects.get(id=pk)
        except Research.DoesNotExist:
            raise Http404

    def get(self, request, username, fieldId, researchId, format=None):
        researches = self.get_object(researchId)
        serializer = ResearchSerializer(researches)
        return Response(data=serializer.data)

    def delete(self, request, user_id, pk, format=None):
        research = self.get_object(pk)
        research.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResearchFiles(APIView):
    def get(self, request, username, fieldId, researchId, filefield):
        research = Research.objects.get(id=researchId)
        print(research.rgb)
        indexes = Indexes.objects.get(research_id=researchId)
        if filefield == 'rgb':
            filepath = os.path.join(settings.MEDIA_ROOT, "{0}".format(research.rgb))
        if filefield == 'ndvi':
            filepath = os.path.join(settings.MEDIA_ROOT, "{0}".format(indexes.ndvi_png))
        if filefield == 'ndwi':
            filepath = os.path.join(settings.MEDIA_ROOT, "{0}".format(indexes.ndwi_png))

        return FileResponse(open(filepath, 'rb'))




class ResearchAOIs(APIView):
    def get(self, request, username, fieldId, researchId):
        aois = AOI.objects.filter(research_id=researchId)
        serializer = AOISerializer(aois, many=True)
        return Response(data=serializer.data)

    def post(self, request, username, fieldId, researchId):
        req = request.data
        print(req)
        research = Research.objects.get(id=researchId)
        indexes = Indexes.objects.get(research_id=researchId)
        aoi = req['geom']['geometry']
        ndvi = os.path.join(settings.MEDIA_ROOT, "{0}".format(indexes.ndvi_tiff))
        ndvi_stats = calc_stats(json.dumps(aoi), ndvi)

        os.remove(settings.MEDIA_ROOT + '\\ndvi_clipped.tif')

        res = {'geom': aoi,
               'min_index': ndvi_stats[0],
               'max_index': ndvi_stats[1],
               'mean_index': ndvi_stats[2],
               'research': req['researchId'],
               'area': req['area']
               }
        serializer = AOISerializer(data=res)
        print('serializer', serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, fieldId, researchId):
        aoi = AOI.objects.get(id=request.data.aoiId)
        aoi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)