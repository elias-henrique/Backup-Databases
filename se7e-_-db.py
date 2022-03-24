#!/usr/bin/python3
import os
import time
import shutil
import pathlib
import threading
from datetime import datetime
from zipfile import ZipFile
import tarfile

try:
    import pyfiglet
except ImportError:
    os.system("pip3 install pyfiglet > /dev/null")
finally:
    import pyfiglet

try:
    import inquirer
except ImportError:
    os.system("pip3 install inquirer > /dev/null")
finally:
    import inquirer

try:
    import pysftp
except ImportError:
    os.system("pip3 install pysftp > /dev/null")
finally:
    import pysftp

try:
    from yaspin import yaspin
except ImportError:
    os.system("pip install yaspin > /dev/null")
finally:
    from yaspin import yaspin

"""
            |  | |  \ |  | |           ||   ____||   _  \     |   ____|    /   \      /      ||   ____|
            |  | |   \|  | `---|  |----`|  |__   |  |_)  |    |  |__      /  ^  \    |  ,----'|  |__   
            |  | |  . `  |     |  |     |   __|  |      /     |   __|    /  /_\  \   |  |     |   __|  
            |  | |  |\   |     |  |     |  |____ |  |\  \----.|  |      /  _____  \  |  `----.|  |____ 
            |__| |__| \__|     |__|     |_______|| _| `._____||__|     /__/     \__\  \______||_______|                                                                                      
"""


class Interface(object):
    def __init__(self):
        self.colors = ("red", "green", "yellow", "blue",
                       "magenta", "cyan", "white")

    @staticmethod
    def index():
        questions = [
            inquirer.Checkbox('interests',
                              message='Select as Options',
                              choices=['Backup', 'SFTP',
                                       'Compress Backup',
                                       'Decompress Backup',
                                       'exit'],
                              ),
        ]
        answers = inquirer.prompt(questions)
        return answers

    @staticmethod
    def backup_ui():
        questions = [
            inquirer.List('type',
                          message='Select which type of database',
                          choices=['MongoDB', 'Postgresql',
                                   'Mysql and MariaDB'],
                          ),
            inquirer.Text('host', message="What's your host"),
            inquirer.Text('user', message="What's your username"),
            inquirer.Text('port', message="What's your port"),
            inquirer.Text('databases', message="What's your databases"),
            inquirer.Text('password', message="What's your password")
        ]
        answers = inquirer.prompt(questions)
        return answers

    @staticmethod
    def sftp_ui(files):
        questions = [
            inquirer.Checkbox('interests',
                              message='Select as Options to SFTP',
                              choices=files,
                              ),
            inquirer.Text('host', message="What's your host"),
            inquirer.Text('user', message="What's your user"),
            inquirer.Text('port', message="What's your port"),
            inquirer.Text('password', message="What's your password"),
            inquirer.Text('path', message="What's your path"),
        ]
        answers = inquirer.prompt(questions)
        return answers

    @staticmethod
    def compress_ui(files):
        questions = [
            inquirer.List('type',
                          message='Select which type of compress',
                          choices=['zip', 'tar', 'gztar', 'bztar', 'xztar'],
                          ),
            inquirer.Checkbox('interests',
                              message='Select as Options',
                              choices=files,
                              ),

        ]
        answers = inquirer.prompt(questions)
        return answers

    @staticmethod
    def decompress_ui(files):
        questions = [
            inquirer.List('type',
                          message='Select which type of compress',
                          choices=['zip', 'tar', 'gztar', 'bztar', 'xztar'],
                          ),
            inquirer.Checkbox('interests',
                              message='Select which type of Decompress',
                              choices=files,
                              ),
        ]
        answers = inquirer.prompt(questions)
        return answers

    def loading(self, msg):
        with yaspin(text="Colors!") as sp:
            for color in self.colors:
                sp.color, sp.text = color, msg
                time.sleep(1)


"""
        |   _  \      /   \      /      ||  |/  / |  |  |  | |   _  \  
        |  |_)  |    /  ^  \    |  ,----'|  '  /  |  |  |  | |  |_)  | 
        |   _  <    /  /_\  \   |  |     |    <   |  |  |  | |   ___/  
        |  |_)  |  /  _____  \  |  `----.|  .  \  |  `--'  | |  |      
        |______/  /__/     \__\  \______||__|\__\  \______/  | _|      
"""


class Backup(object):
    def __init__(self, kwargs, path, cmdui):
        dt_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.name_path = f"seBackup-{str(dt_string)}7e.sql"
        self.kwargs = kwargs
        self.path = path
        self.cmdui = cmdui

        if self.kwargs['type'] == 'Mysql and MariaDB':
            self.mysql()
        elif self.kwargs['type'] == 'Postgresql':
            self.postgres()

    def mysql(self):
        cmd = "mysqldump"

        if self.kwargs['host']:
            cmd += f" --host={self.kwargs['host']}"
        if self.kwargs['password']:
            cmd += f" -p '{self.kwargs['password']}'"
        if self.kwargs['user']:
            cmd += f" -u {self.kwargs['user']}"
        if self.kwargs['port']:
            cmd += f" --port={self.kwargs['port']}"
        if self.kwargs['databases']:
            cmd += f" --databases {self.kwargs['databases']}"

        cmd += f" > {self.path}/{self.name_path}"
        load = threading.Thread(target=self.cmdui.loading, args=(
            "Gerando Backup da base de dados "
            f"{self.kwargs['databases']} em {self.path}/{self.name_path}",))
        load.start()
        load.join()

        if not load.is_alive():
            os.system(cmd)

    def postgres(self):
        if self.kwargs['password']:
            cmd = f"PGPASSWORD='{self.kwargs['password']}'"
        else:
            exit()
        cmd += ' pg_dump'
        if self.kwargs['host']:
            cmd += f" --host={self.kwargs['host']}"
        if self.kwargs['user']:
            cmd += f" -U {self.kwargs['user']}"
        if self.kwargs['port']:
            cmd += f" --port={self.kwargs['port']}"
        if self.kwargs['databases']:
            cmd += f" -d {self.kwargs['databases']}"

        cmd += f" -w > {self.path}/{self.name_path}"

        load = threading.Thread(target=self.cmdui.loading, args=(
            "Gerando Backup da base de dados "
            f"{self.kwargs['databases']} em {self.path}/{self.name_path}",))
        load.start()
        load.join()

        if not load.is_alive():
            os.system(cmd)


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


"""
            .______       __    __  .__   __. 
            |   _  \     |  |  |  | |  \ |  | 
            |  |_)  |    |  |  |  | |   \|  | 
            |      /     |  |  |  | |  . `  | 
            |  |\  \----.|  `--'  | |  |\   | 
            | _| `._____| \______/  |__| \__| 
"""


def main():
    root_path = str(pathlib.Path(__file__).parent.resolve())
    cmui = Interface()

    if 'Backup' in opt['interests']:
        quest = cmui.backup_ui()
        Backup(quest, root_path, cmui)

    if 'Compress Backup' in opt['interests']:
        list_files = os.listdir(root_path)
        quest = cmui.compress_ui(list_files)
        load = threading.Thread(target=cmui.loading, args=(
            "Comprimindo arquivos",))
        load.start()
        load.join()
        if not load.is_alive():
            compress(quest)

    if 'Decompress Backup' in opt['interests']:
        list_files = os.listdir(root_path)
        quest = cmui.decompress_ui(list_files)
        if quest:
            load = threading.Thread(target=cmui.loading, args=(
                "Descomprimindo arquivos",))
            load.start()
            load.join()
            if not load.is_alive():
                decompress(quest)

    if 'SFTP' in opt['interests']:
        list_files = os.listdir(root_path)
        quest = cmui.sftp_ui(list_files)
        if quest:
            load = threading.Thread(target=cmui.loading, args=(
                "Enviado arquivos via SFTP",))
            load.start()
            load.join()
            if not load.is_alive():
                sftpExample(root_path, quest)

    if 'exit' in opt['interests']:
        exit()


if __name__ == '__main__':
    try:
        figlet = pyfiglet.figlet_format("7Backup Databases", font="bulbhead")
        print(figlet)
        while True:
            cmui = Interface()
            opt = cmui.index()
            main()
    except (TypeError, KeyboardInterrupt):
        exit()
