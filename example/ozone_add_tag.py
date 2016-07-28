# -*- coding: UTF-8 -*-
# File: ozone_add_tag
# Time: 7/17/2016 -> 3:27 PM
import os
import csv
from collections import Counter
import glob
import arcpy
from arcpy import env
from arcpy.sa import ExtractValuesToPoints, ExtractByMask, CellStatistics

env.overwriteOutput = True
arcpy.CheckOutExtension('Spatial')

OZONE_CSV_SUBDIR = os.path.normcase("D:\Dian\Data\Ozone\Raw")
NIGHT_RASTER_SUBDIR = os.path.normcase("D:\Dian\Spatial_Files\Night_Image")
UNITED_STATE_MASK = os.path.normcase("D:\Dian\Spatial_Files\United_States_2000/background/newstates.shp")
UNITED_STATE_REGION_MASK_SUBDIR = os.path.normcase("D:\Dian\Spatial_Files\United_States_2010\climate_region")
SPATIAL_REFERENCE = os.path.normcase("D:\Dian\Spatial_Files\United_States_2000/background/Coordinate.prj")


def get_night_images():
    directory, dir_names, _ = os.walk(NIGHT_RASTER_SUBDIR).next()
    dir_names = [dir_name for dir_name in dir_names if ".geotiff" in dir_name]
    night_images = []
    for dir_name in dir_names:
        sub_dir = os.path.join(directory, dir_name)
        filenames = os.listdir(sub_dir)
        night_images.extend(
            [os.path.join(sub_dir, filename) for filename in filenames if filename.endswith(".avg_vis.tif")])
    return night_images


def night_images_extract(night_images):
    def extract(night_image):
        return ExtractByMask(night_image, UNITED_STATE_MASK)
    return map(extract, night_images)


def night_image_mean():
    """
    从多年的night images生成一张均值image的栅格文件
    """
    env.workspace = "G:\yang\ozone_process/night_images"
    out_raster_name = "night_mean.tif"
    if not os.path.exists(os.path.join(env.workspace, out_raster_name)):
        night_images = get_night_images()
        out_rasters = night_images_extract(night_images)
        out_raster = CellStatistics(out_rasters, "MEAN", "DATA")
        out_raster.save(out_raster_name)
    return os.path.join(env.workspace, out_raster_name)
    # if os.path.exists(os.path.join(env.workspace, "night_NE.tif")):
    #     return
    # name_map_dict = {"Northwest": 'NW', "West North Central": 'WNC', "West": 'W', "Southwest": 'SW',
    #                  "East North Central": 'ENC', "Central": 'C', "South": 'S', "Southeast": 'SE', "Northeast": 'NE'}
    # region_masks = glob.glob(os.path.join(UNITED_STATE_REGION_MASK_SUBDIR, "*.shp"))
    # for region_mask in region_masks:
    #     region_shp = ExtractByMask(out_raster_name, region_mask)
    #     out_raster_name = "night_{}.tif".format(name_map_dict[os.path.basename(region_mask)[:-4]])
    #     region_shp.save(out_raster_name)


def ozone_points_create():
    """
    从多个ozone数据csv文件中提取融合的臭氧点，生成了一个新的csv文件，仅仅包含其坐标信息，最后csv文件转化话要素点文件
    """
    env.workspace = "G:\yang\ozone_process\ozone_data"
    ozone_union_csv = os.path.join(env.workspace, "hourly_ozone_sites.csv")
    if not os.path.exists(ozone_union_csv):
        ozone_csvs = [os.path.join(OZONE_CSV_SUBDIR, "hourly_44201_{}.csv".format(year)) for year in range(1990, 2015)]
        location_set = set()
        for ozone_csv in ozone_csvs:
            locations = []
            with open(ozone_csv, 'rb') as csvfile:
                reader = csv.reader(csvfile)
                fields = reader.next()
                longi_ind = fields.index("Longitude")
                lat_ind = fields.index("Latitude")
                for line in reader:
                    longi = line[longi_ind]
                    lat = line[lat_ind]
                    locations.append("{}_{}".format(str(longi), str(lat)))
            location_set.update(locations)

        with open(ozone_union_csv, 'wb') as csvfd:
            writer = csv.writer(csvfd)
            writer.writerow(["longitude", "latitude"])
            for location in list(location_set):
                line = [float(item) for item in location.split("_")]
                writer.writerow(line)

    ozone_shp = os.path.join(env.workspace,"ozone_points.shp")
    if not os.path.exists(ozone_shp):
        arcpy.MakeXYEventLayer_management(ozone_union_csv, "longitude", "latitude", os.path.basename(ozone_shp)[:-4],
                                          SPATIAL_REFERENCE)
        arcpy.FeatureToPoint_management(os.path.basename(ozone_shp)[:-4], ozone_shp)
    return ozone_shp


if __name__ == "__main__":
    night_mean_file = night_image_mean()
    ozone_shp_file = ozone_points_create()

    env.workspace = os.path.normcase("G:\yang\ozone_process/night_images")
    if not os.path.exists(os.path.join(env.workspace, "night_mean.shp")):
        arcpy.RasterToPoint_conversion(night_mean_file, "night_mean.shp")
    # env.workspace = os.path.normcase("G:\yang\ozone_process")
    # if not os.path.exists(os.path.join(env.workspace, "ozone_night.shp")):
    #     arcpy.SpatialJoin_analysis(ozone_shp_file, "G:\yang\ozone_process/night_images/night_mean.shp",
    #                                 "ozone_night.shp", "JOIN_ONE_TO_ONE", "KEEP_ALL", field_mapping="CLOSEST", search_radius="1000 meters")

    # landuse_rasters = ["D:\Dian\Spatial_Files\Land_Use/nlcd_2001_landcover_2011_edition_2014_10_10/nlcd_2001_landcover_2011_edition_2014_10_10.img",
    #                    "D:\Dian\Spatial_Files\Land_Use\nlcd_2006_landcover_2011_edition_2014_10_10/nlcd_2006_landcover_2011_edition_2014_10_10.img",
    #                    "D:\Dian\Spatial_Files\Land_Use\nlcd_2011_landcover_2011_edition_2014_10_10/nlcd_2011_landcover_2011_edition_2014_10_10.img"]
    # env.workspace = "G:\yang\ozone_process\land_use"
    # for landuse_raster in landuse_rasters:
    #     landuse_points = "landuse_{}.shp".format(os.path.basename(landuse_raster)[5:9])
    #     if not os.path.exists(os.path.join(env.workspace, landuse_points)):
    #         arcpy.RasterToPoint_conversion(landuse_raster, landuse_points)

    dem_raster = "D:\Dian\Spatial_Files\US_DEM/US_dem.tif"
    env.workspace = "G:\yang\ozone_process\dem"
    dem_points = "dem.shp"
    if not os.path.exists(os.path.join(env.workspace, dem_points)):
        arcpy.RasterToPoint_conversion(dem_raster, dem_points)

    # ExtractValuesToPoints(ozone_shp_file, night_mean_file, "ozone_night.shp", "INTERPOLATE", "VALUE_ONLY")












