#!/usr/bin/python3
import os
import pathlib
import pyfiglet
import threading
from lib import (
    compress,
    decompress,
    sftpExample,
    Dump,
    Interface
)

"""
            .______       __    __  .__   __. 
            |   _  \     |  |  |  | |  \ |  | 
            |  |_)  |    |  |  |  | |   \|  | 
            |      /     |  |  |  | |  . `  | 
            |  |\  \----.|  `--'  | |  |\   | 
            | _| `._____| \______/  |__| \__| 
"""


def run_interface():
    root_path = str(pathlib.Path(__file__).parent.resolve())
    cmui = Interface()

    if 'Backup' in opt['interests']:
        quest = cmui.backup_ui()
        Dump(quest, root_path, cmui)

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
        while True:
            cmui = Interface()
            opt = cmui.index()
            run_interface()
    except (TypeError, KeyboardInterrupt):
        exit()
