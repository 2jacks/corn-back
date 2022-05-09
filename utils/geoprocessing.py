from osgeo import gdal
from django.contrib.gis.gdal import DataSource
from django.conf import settings

# OUTPUT: arr[min, max, mean, std_dev]
def calc_stats(aoi, raster):
    print(aoi)
    aoi = DataSource(aoi)
    # print(aoi.area)
    rst = gdal.Open(raster)
    tmp_rst_path = settings.MEDIA_ROOT + '\\ndvi_clipped.tif'

    warped = gdal.Warp(tmp_rst_path, rst, cutlineDSName=aoi, dstNodata=None, cropToCutline=True)
    stats = warped.GetRasterBand(1).GetStatistics(0, 1)
    return stats
