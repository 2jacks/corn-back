from osgeo import gdal
from django.contrib.gis.gdal import DataSource
from django.conf import settings
import subprocess
import rasterio.rio.calc


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

# root = 'D:/bashInkom_GIS/web/app/_corn/media/'
# def diff_rasters(first_path=None, second_path=None, test=False):
#
#     output = os.path.join(root, "tmp/diff.tif")
#     subprocess.call(['rio calc', '(-(take a 1)(take b 1))', '--name' + " a=" + "{0}".format(first_path),
#                      '--name' + " b=" + "{0}".format(second_path)], output)
#     if test:
#         print('AAAAAAAAAAAAAAAAAAA')
#
#         cutline = DataSource(os.path.join(root, '{0}'.format('test/field.geojson')))
#
#         a = os.path.join(root, '{0}'.format('test/NDVI_22-04-2022.tif'))
#         b = os.path.join(root, '{0}'.format('test/NDVI_02-05-2022.tif'))
#
#         cropped_a = gdal.Warp(root + '\\test\\cropped_a.tif', a, cutlineDSName=cutline, dstNodata=None,
#                               cropToCutline=True)
#         cropped_b = gdal.Warp(root + '\\test\\cropped_b.tif', a, cutlineDSName=cutline, dstNodata=None,
#                               cropToCutline=True)
#
#         a_end = os.path.join(root, '{0}'.format('test/cropped_a.tif'))
#         b_end = os.path.join(root, '{0}'.format('test/cropped_b.tif'))
#
#         subprocess.check_output(['rio calc', '(-(read 1 1)(read 2 1))', a_end, b_end, output])
#
#
# if __name__ == '__main__':
#     print('AAAAAAAAAAAAAAAAAAA')
#     output = os.path.join(root, "tmp/diff.tif")
#     cutline = DataSource(os.path.join(root, '{0}'.format('test/field.geojson')))
#
#     a = os.path.join(root, '{0}'.format('test/NDVI_22-04-2022.tif'))
#     b = os.path.join(root, '{0}'.format('test/NDVI_02-05-2022.tif'))
#
#     cropped_a = gdal.Warp(root + '\\test\\cropped_a.tif', a, cutlineDSName=cutline, dstNodata=None,
#                           cropToCutline=True)
#     cropped_b = gdal.Warp(root + '\\test\\cropped_b.tif', a, cutlineDSName=cutline, dstNodata=None,
#                           cropToCutline=True)
#
#     a_end = os.path.join(root, '{0}'.format('test/cropped_a.tif'))
#     b_end = os.path.join(root, '{0}'.format('test/cropped_b.tif'))
#
#     subprocess.check_output(['rio calc', '(-(read 1 1)(read 2 1))', a_end, b_end, output])
