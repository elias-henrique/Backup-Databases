# Se7e Backup Databases
> Fazer backup de banco de dados Postgresql, MYSQL e MARIADB
###


<img align="left" width="200" height="200" src="https://user-images.githubusercontent.com/55928280/159481331-5ee9d7fc-bc0a-4267-8747-1a9dbbb28108.png">

<br><br><br><br><br><br><br><br><br>
_Esse serviço não pode ser comercializado Autor_ - _Elias Henrique_
<br>

## Instalações
### Requerimentos
  * `python3`
  * install the libraries with `pip3 install pysftp`


## How to run 

for all information `python3 se7e-_-db.py -h or --help`


## Arguments to use
### optional arguments
    -t TYPE, --type TYPE Use paramete -t or --type mongo|postgres|mysql
    --host HOST Specify which database ip
    --port PORT Specify the database port
    -d DB, --db DB Specify a single database
    -md MDB, --mdb MDB Pass only "true" if it contains the file "databases" in the same location as se7e-_-db.py only: MYSQL, MARIADB
    -u USER, --user USER Specify which database user
    -p PASSWORD, --password PASSWORD Specify what the database password is
    -s SFTP, --sftp SFTP Pass accesses like this user:password@127.0.0.1:/desktop/destination


## Release History
* 0.0.2
    * backup mongod (in progress)
    * restore both backups (in progress)
* 0.0.1
   * backup databases postgresql, mysql, mariadb
* 0.0.1
    * Trabalho em processo

## Meta

Elias Henrique – [eliashenrique.pyc@gmail.com](https://mail.google.com/mail/u/0/#inbox?compose=new)


## Authors
 
* **Elias Henrique**: @elias-henrique (https://github.com/elias-henrique)
