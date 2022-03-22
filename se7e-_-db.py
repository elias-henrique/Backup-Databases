import argparse
import os
import pathlib
import pysftp
from datetime import datetime

'''                                                                                                         
              db                                                                              mm                      
             ;MM:                                                                             MM                      
            ,V^MM.    `7Mb,od8  .P"Ybmmm `7MM  `7MM  `7MMpMMMb.pMMMb.   .gP"Ya  `7MMpMMMb.  mmMMmm   ,pW"Wq.  ,pP"Ybd 
           ,M  `MM      MM' "' :MI  I8     MM    MM    MM    MM    MM  ,M'   Yb   MM    MM    MM    6W'   `Wb 8I   `" 
           AbmmmqMA     MM      WmmmP"     MM    MM    MM    MM    MM  8M""""""   MM    MM    MM    8M     M8 `YMMMa. 
          A'     VML    MM     8M          MM    MM    MM    MM    MM  YM.    ,   MM    MM    MM    YA.   ,A9 L.   I8 
        .AMA.   .AMMA..JMML.    YMMMMMb    `Mbod"YML..JMML  JMML  JMML. `Mbmmd' .JMML  JMML.  `Mbmo  `Ybmd9'  M9mmmP' 
                               6'     dP                                                                              
                               Ybmmmd'                                                                                
'''


def arguments():
    parser = argparse.ArgumentParser(
        description='Backup de banco de dados e restauraçao')
    parser.add_argument(
        '-t',
        '--type',
        required=True,
        help='Use paramentro -t ou --type mongo|postgres|mysql '
    )
    parser.add_argument(
        '--host',
        required=False,
        help='Especificar qual ip do banco de dados'
    )
    parser.add_argument(
        '--port',
        required=False,
        help='Especificar a porta do banco de dadoss'
    )
    parser.add_argument(
        '-d',
        '--db',
        required=False,
        help='Especificar um unico banco de dados'
    )
    parser.add_argument(
        '-md',
        '--mdb',
        required=False,
        help='Passe apenas "true" se contem o arquivo "databases" no mesmo local do se7e-_-db.py apenas: MYSQL, MARIADB'
    )
    parser.add_argument(
        '-u',
        '--user',
        required=True,
        help='Especificar qual usuario do banco de dados'
    )
    parser.add_argument(
        '-p',
        '--password',
        required=False,
        help='Especifcar qual é a senha do banco de dados'
    )
    parser.add_argument(
        '-s',
        '--sftp',
        required=False,
        help='Passe os acessos dessa maneira user:senha@127.0.0.1:/desktop/destination'
    )
    args = parser.parse_args()
    return args


'''
                     `7MM"""Yp, `7MMF' `YMM' `7MM"""Mq.
                      MM    Yb   MM   .M'     MM   `MM.
                      MM    dP   MM .d"       MM   ,M9 
                      MM"""bg.   MMMMM.       MMmmdM9  
                      MM    `Y   MM  VMA      MM       
                      MM    ,9   MM   `MM.    MM       
                    .JMMmmmd9  .JMML.   MMb..JMML.     
                                                                                                
'''


class Backup(object):
    def __init__(self, database='', host='', port='', username='', password='', dst=''):
        dt_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.database = database
        self.username = username
        self.password = password
        self.host = host
        self.name_path = f"seBackup-{str(dt_string)}7e.sql"
        self.dst = dst

    def bkp_mysql(self):
        print(
            f"  -- Gerando Backup da base de dados {self.database} em {self.dst}/{self.name_path} ...")
        os.system(
            f"mysqldump --databases {self.database} -u{self.username} -p"
            f"'{self.password}' > {self.dst}/{self.name_path}"
        )
        return f"{self.dst}/{self.name_path}", self.name_path

    def bkp_postgres(self):
        print(
            f"  -- Gerando Backup da base de dados {self.database} "
            f"em {self.dst}/{self.name_path} ..."
        )
        os.system(
            f"PGPASSWORD='{self.password}' pg_dump -U {self.username} -h "
            f"{self.host} -w > {self.dst}/{self.name_path}"
        )
        return f"{self.dst}/{self.name_path}", self.name_path


'''                                  
                                          ,...                   
                             .M"""bgd   .d' ""  mm               
                            ,MI    "Y   dM`     MM               
                            `MMb.      mMMmm  mmMMmm  `7MMpdMAo. 
                              `YMMNq.   MM      MM      MM   `Wb 
                            .     `MM   MM      MM      MM    M8 
                            Mb     dM   MM      MM      MM   ,AP 
                            P"Ybmmd"  .JMML.    `Mbmo   MMbmmd'  
                                                        MM       
                                                      .JMML.  
'''


def sftpArgs(arg):
    output = arg.split("@")
    if len(output) > 1:
        out = output[1].split(":")
        out2 = output[0].split(":")
        if len(out2) > 1:
            user, passw = out2[0], out2[1]
        else:
            raise ValueError("Error: verifique se o paramentro foram passado corretamente\n"
                             "Use: --help para mais infomaçoes")
        if len(out) > 1:
            ip, dst = out[0], out[1]
        else:
            raise ValueError("Error: verifique se o paramentro foram passado corretamente\n"
                             "Use: --help para mais infomaçoes")
    else:
        raise ValueError("Error: verifique se o paramentro foram passado corretamente\n"
                         "Use: --help para mais infomaçoes")

    return user, passw, ip, dst


def sftpExample(local_path, remote_pah, host, user, password, port=22):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(
            host,
            username=user,
            password=password,
            port=port,
            cnopts=cnopts
    ) as sftp:
        sftp.put(str(local_path),
                 str(remote_pah))  # upload file to public/ on remote
        sftp.close()


if __name__ == '__main__':
    path = str(pathlib.Path(__file__).parent.resolve())
    args = arguments()
    databases = ""

    if args.mdb:
        if args.mdb.lower() == "true":
            try:
                with open(path + "/databases", "r") as roi:
                    r = str(roi.read()).replace("\n", " ")
                databases = r
            except FileNotFoundError:
                raise NotADirectoryError("crie o arquivo 'databases' nesse diretorio")
    else:
        databases = args.db

    bkp = Backup(
        database=databases,
        host=args.host,
        port=args.port,
        username=args.user,
        password=args.password,
        dst=path
    )
    if args.type.lower() == "mysql":
        path, name = bkp.bkp_mysql()
    elif args.type.lower() == "postgres":
        path, name = bkp.bkp_postgres()
    elif args.type.lower() == "mongo":
        pass
    else:
        raise ValueError("Parametros nao passado corretamente\nUse: --help para mais informaçao")

    if args.sftp:
        user, passw, ip, dst = sftpArgs(args.sftp)

        sftpExample(
            path,
            dst+"/"+name,
            ip,
            user,
            passw
        )
