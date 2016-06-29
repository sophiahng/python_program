import os
import fun_clip_analysis as clip
import fun_create_buffer as buffer
import fun_erase_analysis as erase
import fun_add_field
import fun_fill_attribute_field_with_values as fill_attribute
import fun_merge_management as merge
import fun_dbf_to_csv


def loc_urc(total_sites, urban_polygon, cast_sites, out_features):
    if not os.path.exists(os.path.dirname(out_features)):
        os.mkdir(os.path.dirname(out_features))
    urban_sites = os.path.join(os.path.dirname(out_features), "urban.shp")
    clip.clip_analysis(total_sites, urban_polygon,urban_sites)
    clean_sites = os.path.join(os.path.dirname(out_features), "clean.shp")
    cast_buffer = os.path.join(os.path.dirname(out_features), "cast_buffer.shp")
    buffer.make_buffer(cast_sites, cast_buffer, "1000 Meters")
    clip.clip_analysis(total_sites, cast_buffer, clean_sites)
    urban_rural_combine = os.path.join(os.path.dirname(out_features), "urcombine.shp")
    erase.erase_analysis(total_sites, clean_sites, urban_rural_combine)
    rural_sites = os.path.join(os.path.dirname(out_features), "rural.shp")
    erase.erase_analysis(urban_rural_combine, urban_sites, rural_sites)
    fun_add_field.add_field(urban_sites, "loc_urc", "TEXT", 10)
    fun_add_field.add_field(rural_sites, "loc_urc", "TEXT", 10)
    fun_add_field.add_field(clean_sites, "loc_urc", "TEXT", 10)
    fill_attribute.fill_attribute_table(urban_sites,"loc_urc",os.path.basename(urban_sites))
    fill_attribute.fill_attribute_table(rural_sites, "loc_urc", os.path.basename(rural_sites))
    fill_attribute.fill_attribute_table(clean_sites, "loc_urc", os.path.basename(clean_sites))
    merge.merge_management([urban_sites, rural_sites, clean_sites], out_features)
    fun_dbf_to_csv.dbf_csv(os.path.join(out_features[:-4], ".dbf"), os.path.join(out_features[:-4], ".csv"))

if __name__ == "__main__":
    pass













