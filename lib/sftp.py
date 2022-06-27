import pysftp

"""
                 _______. _______ .___________..______   
                /       ||   ____||           ||   _  \  
               |   (----`|  |__   `---|  |----`|  |_)  | 
                \   \    |   __|      |  |     |   ___/  
            .----)   |   |  |         |  |     |  |      
            |_______/    |__|         |__|     | _|     
"""


def sftpExample(local_path, kwargs):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(
            kwargs['host'],
            username=kwargs['user'],
            password=kwargs['password'],
            port=int(kwargs['port']),
            cnopts=cnopts
    ) as sftp:
        for path in kwargs['interests']:
            sftp.put(local_path + "/" + path,
                     kwargs['path'] + "/" + path
                     )  # upload file to public/ on remote
        sftp.close()
