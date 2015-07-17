
import zipfile
import requests
from clint.textui import progress
import tempfile

def download_zip(url, path):
    r = requests.get(url, stream=True)
    temp = tempfile.NamedTemporaryFile(suffix='.zip')
    print('Downloading url --> %s\nto --> %s' % (url, temp.name))
    with open(temp.name, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    z = zipfile.ZipFile(temp)
    print("extracting to --> %s" % path)
    z.extractall(path=path)


if __name__ == "__main__":
    path = '/home/edill/Downloads/'
    url = 'https://www.dropbox.com/s/963c4ymfmbjg5dm/SOFC.zip?dl=1'
    download_zip(url, path)
