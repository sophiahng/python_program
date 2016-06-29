import os
import glob
import time

SELECTED_BANDS = '"0 1 0 0 0 0 0 0 0 0 0 0"'

if __name__ == "__main__":
    data_dir = 'G:/NDVI download'
    dest_dir = 'G:/EVI'
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    hdf_files_path = os.path.normcase(os.path.join(dest_dir, 'hdf_files.txt'))
    mosaic_file_path = os.path.normcase(os.path.join(dest_dir, 'mosaic.hdf'))
    parameter_file_path = os.path.normcase(os.path.join('../', 'parameter.prm'))

    for year in xrange(2000, 2015):
        hdf_sub_dir = os.path.normcase(os.path.join(data_dir, str(year)))
        os.chdir(hdf_sub_dir)
        hdf_paths = glob.glob(os.path.join(hdf_sub_dir, '*.hdf'))
        date_set = set()
        for hdf_path in hdf_paths:
            date_set.add(int(os.path.split(hdf_path)[-1].split('.')[1][-3:]))

        for date in date_set:
            hdf_date_paths = [hdf_path for hdf_path in hdf_paths if int(os.path.split(hdf_path)[-1].split('.')[1][-3:]) == date]
            tif_file_path = os.path.normcase(os.path.join(dest_dir, "US" + str(year) + str(date) + ".tif"))
            tif_actual_file_path = os.path.normcase(os.path.join(dest_dir, "US" + str(year) + str(date) + '.250m_16_days_EVI' + ".tif"))
            if os.path.exists(tif_actual_file_path):
                continue
            if os.path.exists(hdf_files_path):
                os.remove(hdf_files_path)
            with open(hdf_files_path, 'w') as fd:
                for hdf_date_path in hdf_date_paths:
                    fd.write(os.path.split(hdf_date_path)[-1] + '\n')
            time.sleep(0.5)
            cmd = "mrtmosaic -i {0} -s {1} -o {2}".format(hdf_files_path, SELECTED_BANDS, mosaic_file_path)
            os.system(cmd)
            time.sleep(0.5)
            cmd = "resample -p {0}".format(parameter_file_path)
            cmd = cmd + " -i {0} -o {1}".format(mosaic_file_path, tif_file_path)
            os.system(cmd)
            time.sleep(0.5)
            if os.path.exists(hdf_files_path):
                os.remove(hdf_files_path)
            if os.path.exists(mosaic_file_path):
                os.remove(mosaic_file_path)








