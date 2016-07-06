import os
import fun_clip_analysis as clip
import fun_erase_analysis as erase
import fun_add_field
import fun_fill_attribute_field_with_values as fill_attribute
import fun_merge_management as merge
import fun_dbf_to_csv


def loc_ur(total_site, urban_polygon, out_features):
    """"""
    if not os.path.exists(os.path.dirname(out_features)):
        os.mkdir(os.path.dirname(out_features))
    if os.path.exists(out_features[:-4] + ".csv"):
        return
    urban_sites = os.path.join(os.path.dirname(out_features), "urban.shp")
    clip.clip_analysis(total_site, urban_polygon, urban_sites)
    rural_sites = os.path.join(os.path.dirname(out_features), "rural.shp")
    erase.erase_analysis(total_site, urban_sites, rural_sites)
    fun_add_field.add_field(urban_sites, "loc_ur", "TEXT", 10)
    fun_add_field.add_field(rural_sites, "loc_ur", "TEXT", 10)
    fill_attribute.fill_attribute_table(urban_sites, "loc_ur", os.path.basename(urban_sites[:-4]))
    fill_attribute.fill_attribute_table(rural_sites, "loc_ur", os.path.basename(rural_sites[:-4]))
    merge.merge_management([urban_sites, rural_sites], out_features)
    fun_dbf_to_csv.dbf_csv(out_features[:-4] + ".dbf", out_features[:-4] + ".csv")

if __name__ == "__main__":
    pass

