import sys
import os
import subprocess
import shutil
import glob
from dsmpy.definitions import ROOT_DIR

# set global paths
rootdsm_sh = os.path.join(
    ROOT_DIR, 'src_f90/tish/example/dsm_accuracy_check/')
rootdsm_psv = os.path.join(
    ROOT_DIR, 'src_f90/tipsv/examples/')
root_sac = os.path.join(ROOT_DIR, '../tests/sac_files/')
root_resources = os.path.join(ROOT_DIR, 'resources/')
