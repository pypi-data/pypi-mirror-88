from os import path, makedirs
from shutil import rmtree
from time import sleep

from nonaybay.configuration.variables import project_base_dir, project_temp_dir


def createdirectory():
    if not path.exists(project_base_dir):
        print('O caminho {} ainda não foi criado.\nCRIANDO...'.format(project_base_dir))
        sleep(2)
        makedirs(project_base_dir)
        makedirs(project_temp_dir)

    else:
        print('O caminho {} já existe.\nREMOVENDO...'.format(project_base_dir))
        sleep(2)
        rmtree(project_base_dir)

        createdirectory()
