import zipfile
import requests
import tempfile
from clint.textui import progress
import os
import sys

def download_zip(url, download_path=None):
    if download_path is None:
        download_path = tempfile.NamedTemporaryFile(suffix='.zip').name
    r = requests.get(url, stream=True)
    print('Downloading url --> %s\nto --> %s' % (url, download_path))
    with open(download_path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024),
                                  expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    return download_path
    

def run(data_folder=None):
    print("__file__")
    current_folder = os.sep.join(__file__.split(os.sep)[:-1])
    # path = os.path.abspath(sys.modules['__main__'].__file__)
    # current_folder = os.sep + os.path.join(*path.split(os.sep))
    print("current_folder = %s" % current_folder)
    zip_file_url = 'https://www.dropbox.com/s/56gqn3poc3gsvux/Duke_data.zip?dl=1'
    download_path = os.path.join(current_folder, 'Duke_data.zip')
    if not os.path.exists(download_path):
        temp = download_zip(zip_file_url, download_path=download_path)
    if data_folder is None:
        data_folder = os.path.join(current_folder, 'Duke_data')
    print('current_folder = %s' % current_folder)
    if not os.path.exists(data_folder):
        z = zipfile.ZipFile(download_path)
        print("extracting to --> %s" % current_folder)
        files = [f.filename for f in z.filelist
                 if (not f.filename.split(os.path.sep)[-1].startswith('.')
                 and f.filename.endswith(".npy"))]
        for f in files:
            z.extract(f, path=current_folder)

    
if __name__ == "__main__":
    run()
