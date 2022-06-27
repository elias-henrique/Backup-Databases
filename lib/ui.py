from yaspin import yaspin
import inquirer
import time


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
