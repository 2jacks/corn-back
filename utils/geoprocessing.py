import os.path

from osgeo import gdal
from django.contrib.gis.gdal import DataSource
from django.conf import settings
import uuid
import rioxarray


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


def clip_and_subtract(r_1, r_2, mask):
    geom = [mask]

    ds_1 = rioxarray.open_rasterio(r_1, masked=True).squeeze()
    ds_2 = rioxarray.open_rasterio(r_2, masked=True).squeeze()

    print('--------------', geom, '\n', ds_1, '\n', ds_2)
    print('======CRS=======', ds_1.rio.crs, ds_2.rio.crs)

    ds_1_clipped = ds_1.rio.clip(geom, crs='4326')
    ds_2_clipped = ds_2.rio.clip(geom, crs='4326')

    # print('ds_1_clipped', ds_1_clipped)
    # print('ds_2_clipped', ds_2_clipped)

    dss_repr_match = ds_2_clipped.rio.reproject_match(ds_1_clipped)
    # print('repr_match', dss_repr_match)
    dss_repr_match = dss_repr_match.assign_coords({
        "x": ds_1_clipped.x,
        "y": ds_1_clipped.y,
    })
    res = ds_1_clipped - dss_repr_match

    pre_res = res.rio.clip(geom, crs='4326')
    subtract_tif_path = os.path.join(settings.MEDIA_ROOT, 'tmp/' + str(uuid.uuid4()) + '.tif')
    out = pre_res.rio.to_raster(subtract_tif_path)
    output_filename = os.path.join(settings.MEDIA_ROOT, 'tmp/' + str(uuid.uuid4()) + '.tif')
    gdal.DEMProcessing(output_filename, subtract_tif_path, processing='color-relief', colorFilename='D:\\bashInkom_GIS\\web\\app\\_corn\\utils\\subtract_colormap.txt',
                       computeEdges=True, addAlpha=True, format='GTiff',
                       creationOptions=['QUALITY=100', 'LOSSLESS=True'])
    output_end_filename = os.path.join(settings.MEDIA_ROOT, 'tmp/' + str(uuid.uuid4()) + '.png')

    end = rioxarray.open_rasterio(output_filename, masked=True).squeeze()
    end_clipped = end.rio.clip(geom, crs='4326')
    end_end = end_clipped.rio.to_raster(output_end_filename)
    return output_end_filename
