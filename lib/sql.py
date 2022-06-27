from datetime import datetime
import threading
import os

"""
        |   _  \      /   \      /      ||  |/  / |  |  |  | |   _  \  
        |  |_)  |    /  ^  \    |  ,----'|  '  /  |  |  |  | |  |_)  | 
        |   _  <    /  /_\  \   |  |     |    <   |  |  |  | |   ___/  
        |  |_)  |  /  _____  \  |  `----.|  .  \  |  `--'  | |  |      
        |______/  /__/     \__\  \______||__|\__\  \______/  | _|      
"""


class Dump(object):
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
