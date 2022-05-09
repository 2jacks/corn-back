from django.contrib.gis.db import models
from accounts.models import User
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.file_management import user_directory_path, user_research_path, user_indexes_path, user_field_path


class Farmer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)
    date_of_birth = models.DateField(blank=True, null=True)


class Culture(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Field(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=256)
    geom = models.PolygonField()
    area = models.FloatField(blank=True, null=True)

    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Soil(models.Model):
    field = models.OneToOneField(Field, on_delete=models.CASCADE)
    savi = models.FileField(upload_to=user_field_path)


class Research(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    date = models.DateField()
    bounds = models.JSONField(default=dict(corner1=dict(lat=54.43, lng=55.55), corner2=dict(lat=54.43, lng=55.55)))

    rgb = models.FileField(upload_to=user_research_path)

    def __str__(self):
        return str(self.date)


class Indexes(models.Model):
    research = models.OneToOneField(Research, on_delete=models.CASCADE)

    ndvi_tiff = models.FileField(upload_to=user_indexes_path)
    ndvi_png = models.FileField(upload_to=user_indexes_path)

    ndwi_tiff = models.FileField(upload_to=user_indexes_path)
    ndwi_png = models.FileField(upload_to=user_indexes_path)


class FitoScan(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)

    location = models.PointField()

    n = models.FloatField(null=True, blank=True)
    p = models.FloatField(null=True, blank=True)
    k = models.FloatField(null=True, blank=True)
    s = models.FloatField(null=True, blank=True)
    ca = models.FloatField(null=True, blank=True)
    mg = models.FloatField(null=True, blank=True)
    b = models.FloatField(null=True, blank=True)
    cu = models.FloatField(null=True, blank=True)
    zn = models.FloatField(null=True, blank=True)
    mn = models.FloatField(null=True, blank=True)
    fe = models.FloatField(null=True, blank=True)
    mo = models.FloatField(null=True, blank=True)
    co = models.FloatField(null=True, blank=True)
    j = models.FloatField(null=True, blank=True)

    def ___str__(self):
        return str(self.location)


class AOI(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE, null=True, blank=False)

    geom = models.PolygonField()
    area = models.FloatField()
    min_index = models.FloatField()
    max_index = models.FloatField()
    mean_index = models.FloatField()

    def ___str__(self):
        return str(self.id)

    class Meta:
        db_table = 'geo_areas_of_interest'
