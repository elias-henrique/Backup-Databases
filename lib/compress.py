from zipfile import ZipFile
import tarfile
import shutil

"""
             /      | /  __  \  |   \/   | |   _  \  |   _  \     |   ____|    /       |    /       |
            |  ,----'|  |  |  | |  \  /  | |  |_)  | |  |_)  |    |  |__      |   (----`   |   (----`
            |  |     |  |  |  | |  |\/|  | |   ___/  |      /     |   __|      \   \        \   \    
            |  `----.|  `--'  | |  |  |  | |  |      |  |\  \----.|  |____ .----)   |   .----)   |   
             \______| \______/  |__|  |__| | _|      | _| `._____||_______||_______/    |_______/   
"""


def compress(kwargs):
    for path in kwargs['interests']:
        shutil.make_archive(path, kwargs['type'], './', path)


def decompress(kwargs):
    if kwargs['type'] == "zip":
        for path in kwargs['interests']:
            z = ZipFile(path, 'r')
            z.extractall()
            z.close()
    else:
        for path in kwargs['interests']:
            t = tarfile.open(path)
            t.extractall()
