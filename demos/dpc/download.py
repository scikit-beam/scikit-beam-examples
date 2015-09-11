import zipfile
import requests
import tempfile
from clint.textui import progress
import os

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
    
def run(unzip_path=None):
    current_folder = os.sep.join(__file__.split(os.sep)[:-1])
    print('current_folder = %s' % current_folder)
    zip_file_url = 'https://www.dropbox.com/s/ntvk7866h23jdpr/SOFC.zip?dl=1'
    download_path = os.path.join(current_folder, 'SOFC.zip')
    if not os.path.exists(download_path):
        temp = download_zip(zip_file_url, download_path=download_path)
        
    if unzip_path is None:
        unzip_path = os.path.join(current_folder, 'SOFC')
    if not os.path.exists(unzip_path):
        z = zipfile.ZipFile(download_path)
        print("extracting to --> %s" % unzip_path)
        z.extractall()
    else:
        print('%s does not exist' % unzip_path)


if __name__ == "__main__":
    run()
