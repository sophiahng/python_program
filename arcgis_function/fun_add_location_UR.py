import os
import fun_clip_analysis as clip
import fun_erase_analysis as erase
import fun_add_field
import fun_fill_attribute_field_with_values as fill_attribute
import fun_merge_management as merge
import fun_dbf_to_csv


def loc_ur(total_sites, urban_polygon, out_features):
    if not os.path.exists(os.path.dirname(out_features)):
        os.mkdir(os.path.dirname(out_features))
    urban_sites = os.path.join(os.path.dirname(out_features), "urban.shp")
    clip.clip_analysis(total_sites, urban_polygon,urban_sites)
    rural_sites = os.path.join(os.path.dirname(out_features), "rural.shp")
    erase.erase_analysis(total_sites, urban_sites, rural_sites)
    fun_add_field.add_field(urban_sites, "loc_ur", "TEXT", 10)
    fun_add_field.add_field(rural_sites, "loc_ur", "TEXT", 10)
    fill_attribute.fill_attribute_table(urban_sites,"loc_ur",os.path.basename(urban_sites))
    fill_attribute.fill_attribute_table(rural_sites, "loc_ur", os.path.basename(rural_sites))
    merge.merge_management([urban_sites, rural_sites], out_features)
    fun_dbf_to_csv.dbf_csv(os.path.join(out_features[:-4], ".dbf"), os.path.join(out_features[:-4], ".csv"))

if __name__ == "__main__":
    pass

