import os
import json

from django.views.decorators.csrf import csrf_exempt

from utils.geoprocessing import calc_stats, clip_and_subtract
from django.conf import settings
from django.http import Http404, FileResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Farmer, Field, Research, AOI, Indexes, FitoScan as FitoScanModel
from accounts.models import User
from .serializers import FieldSerializer, ResearchSerializer, AOISerializer, FitoScanSerializer


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

    def delete(self, request, username, format=None):
        field = self.get_object(request.data['fieldId'])
        field.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        if filefield == 'ndwi' and indexes.ndwi_png is not None:
            filepath = os.path.join(settings.MEDIA_ROOT, "{0}".format(indexes.ndwi_png))

        return FileResponse(open(filepath, 'rb'))


class ResearchAOIs(APIView):
    def get(self, request, username, fieldId, researchId):
        aois = AOI.objects.filter(research_id=researchId)
        serializer = AOISerializer(aois, many=True)
        return Response(data=serializer.data)

    def post(self, request, username, fieldId, researchId):
        req = request.data

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
        print(request.data)
        aoi = AOI.objects.get(id=request.data['aoiId'])
        aoi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnalysisViewSet(viewsets.ModelViewSet):
    # def list(self, request):
    #     queryset = Field.objects.all()
    #     serializer = FieldSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = Field.objects.all()
    #     field = get_object_or_404(queryset, pk=pk)
    #     serializer = FieldSerializer(field)
    #     return Response(serializer.data)

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def index_diff(self, request, pk=None):
        data = request.data
        first_res = data['firstRes']
        second_res = data['secondRes']
        mask = data['mask']

        first_research = Research.objects.get(id=first_res)
        second_research = Research.objects.get(id=second_res)

        first_raster = os.path.join(settings.MEDIA_ROOT, str(Indexes.objects.get(research_id=first_research.id).ndvi_tiff))
        second_raster = os.path.join(settings.MEDIA_ROOT,
                                     str(Indexes.objects.get(research_id=second_research.id).ndvi_tiff))
        filepath = clip_and_subtract(first_raster, second_raster, mask)
        return FileResponse(open(filepath, 'rb'))


class FitoScan(APIView):
    def get(self, request, username, fieldId, researchId):
        fitoscans = FitoScanModel.objects.filter(research_id=researchId)
        serializer = FitoScanSerializer(fitoscans, many=True)
        return Response(data=serializer.data)
