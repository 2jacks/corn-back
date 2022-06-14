from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Farmer, Field, Research, AOI, Indexes, FitoScan


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ('name', 'phone', 'date_of_birth')


class FieldSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Field
        geo_field = 'geom'
        fields = ('id', 'name', 'owner', 'area')


class IndexesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indexes
        fields = ('id', 'ndvi_png', 'ndvi_tiff', 'ndwi_png', 'ndwi_tiff', 'research_id')


class ResearchSerializer(serializers.ModelSerializer):
    indexes = IndexesSerializer()

    class Meta:
        model = Research
        fields = ('id', 'date', 'bounds', 'rgb', 'field_id', 'indexes')


class AOISerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AOI
        geo_field = 'geom'
        fields = ('id', 'area', 'min_index', 'max_index', 'mean_index', 'research')


class FitoScanSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = FitoScan
        geo_field = 'location'
        fields = ('id', 'research_id', 'n', 'p', 'k', 's', 'ca', 'mg', 'b', 'cu', 'zn', 'mn', 'fe', 'mo', 'co', 'j')

