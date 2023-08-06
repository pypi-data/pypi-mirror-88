import pkg_resources

from dr_files.utilities import dr_to_csv, dr_to_tdms, dr_to_values, dr_to_wav


def version():
    pkg_resources.get_distribution("dr_files").version
