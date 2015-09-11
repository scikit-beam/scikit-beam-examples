import sys
import os
import importlib
import subprocess
import zipfile
import requests
import tempfile
from clint.textui import progress
import importlib
demo_data_folder = 'data'


if __name__ == "__main__":
    path = os.path.abspath(sys.modules['__main__'].__file__)
    current_folder = os.sep + os.path.join(*path.split(os.sep)[:-1])
    folders = [folder for folder in os.listdir(current_folder) if os.path.isdir(folder)]
    # download stuff
    for folder in folders:
        files = os.listdir(folder)
        if 'download.py' in files:
            module = importlib.import_module('%s.%s' % (folder, 'download'))
            module.run(unzip_path=folder)
    # unzip stuff
    for folder in folders:
        files = os.listdir(folder)
        for f in files:
            if f.endswith('.zip'):
                zippath = os.path.join(folder, f)
                print('zippath = %s' % zippath)
                z = zipfile.ZipFile(zippath)
                z.extractall(path=folder)
    
    # print(os.getcwd())
    # path = os.path.abspath(sys.modules['__main__'].__file__)
    # current_folder = os.sep + os.path.join(*path.split(os.sep)[:-1])
    # print(current_folder)
    # print(os.path.join(os.getcwd(), __file__))
    # print(os.listdir(current_folder))
    #
