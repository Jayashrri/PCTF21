import mysql.connector
from bcrypt import hashpw, gensalt
from stringcolor import cs, bold
from json import load
import sys

class Actions:

    def __init__(self, config_data, logger):
        db_host = config_data['db']['host']
        db_user = config_data['db']['user']
        db_password = config_data['db']['password']
        db_name = config_data['db']['database']
        db_port = config_data['db']['port']

        self.logger = logger
        self.id_table = config_data['db']['id_table']
        self.icecream_table = config_data['db']['icecream_table']
        self.admin = config_data['admin']
        self.flags = {'logged_in': False}
        try:
            self.db = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=db_port)
            self.cursor = self.db.cursor()
            self.table = self.table_name()
            self.create_table()
        except Exception as e:
            self.logger.exception(str(e))
            raise Exception('AN UNEXPECTED ERROR OCCURRED.')

    def generate_hash(self, password) -> str:
        return hashpw(password.encode(), gensalt()).decode()

    def hash_match(self, password, hashp) -> str:
        return hashpw(password.encode(), hashp.encode()).decode() == hashp

    def table_name(self) -> str:
        self.db.commit()
        cmd = f'create table if not exists {self.id_table} (id int not null auto_increment primary key);'
        self.cursor.execute(cmd)
        self.db.commit()

        cmd = f'select id from {self.id_table} order by id desc limit 1;'
        self.cursor.execute(cmd)
        id = [row[0] for row in self.cursor]
        cmd = f'insert into {self.id_table} values (0);'
        self.cursor.execute(cmd)
        self.db.commit()

        if len(id) == 0:
            id = [0]
        id = id[0] + 1
        return 'user_{:06}'.format(id)

    def create_table(self) -> None:
        try:
            self.db.commit()
            cmd = f'create table {self.table} (id int not null auto_increment, username char(20) not null, email varchar(255) not null, password varchar(255) not null, primary key (id));'
            self.cursor.execute(cmd)

            cmd = f'insert into {self.table} (username, email, password) values (\'{self.admin["username"]}\', \'{self.admin["email"]}\', \'{self.admin["password"]}\');'
            self.cursor.execute(cmd)
            self.db.commit()
        except Exception as e:
            self.logger.exception(str(e))
            raise Exception(f'CANNOT CREATE TABLE \'{self.table}\'.')

    def delete_table(self) -> None:
        try:
            self.db.commit()
            cmd = f'drop table {self.table};'
            self.cursor.execute(cmd)
            self.db.commit()
        except Exception as e:
            self.logger.exception(str(e))
            raise Exception(f'CANNOT DELETE TABLE \'{self.table}\'.')

    def exists(self, table, column, value) -> bool:
        self.db.commit()
        cmd = f'select {column} from {table} where {column} = \'{value}\';'
        self.cursor.execute(cmd)
        return len(list(self.cursor)) > 0

    def signup(self, params) -> bold:
        username, email, password = params
        if self.flags['logged_in']:
            return cs("LOGOUT FIRST.", "#ffff00").bold()
        if self.exists(self.table, 'username', username):
            return cs("USERNAME IS ALREADY IN USE.", "#ff0000").bold()
        if self.exists(self.table, 'email', email):
            return cs("EMAIL IS ALREADY IN USE.", "#ff0000").bold()
        try:
            password = self.generate_hash(password)
            self.db.commit()
            cmd = f'insert into {self.table} (username, email, password) values (\'{username}\', \'{email}\', \'{password}\');'
            self.cursor.execute(cmd)
            self.db.commit()
            return cs("SIGNUP SUCCESSFUL!", "#66ff00").bold()
        except Exception as e:
            self.logger.exception(str(e))
            return cs("SIGNUP FAILED!", "#ff0000").bold()

    def signin(self, params) -> (bool, bold):
        username, password = params
        if self.flags['logged_in']:
            return False, cs("LOGOUT FIRST.", "#ffff00").bold()
        if not self.exists(self.table, 'username', username):
            return False, cs("NO SUCH ACCOUNT EXISTS.", "#ffff00").bold()
        try:
            self.db.commit()
            cmd = f'select password from {self.table} where username = \'{username}\';'
            self.cursor.execute(cmd)
            hashes = [row[0] for row in self.cursor]

            matches = [True if self.hash_match(password, hashp) else False for hashp in hashes]
            if any(matches):
                self.flags['logged_in'] = not self.flags['logged_in']
                isadmin = (username == self.admin['username'])
                return isadmin, cs("SIGNIN SUCCESSFUL!", "#66ff00").bold()
            else:
                return False, cs("INCORRECT PASSWORD", "#ff0000").bold()
        except Exception as e:
            self.logger.exception(str(e))
            return False, cs("SIGNIN FAILED!", "#ff0000").bold()

    def signout(self) -> bold:
        if self.flags['logged_in']:
            self.flags['logged_in'] = not self.flags['logged_in']
            return cs("SIGNOUT SUCCESSFUL!", "#66ff00").bold()
        else:
            return cs("ALREADY SIGNED OUT.", "#ffff00").bold()

    def fetch_sprinkles(self, icecream) -> str:
        if not self.exists(self.icecream_table, 'icecream', icecream):
            return ''
        try:
            cmd = f'select sprinkles from {self.icecream_table} where icecream = \'{icecream}\';'
            self.cursor.execute(cmd)
            sprinkles = list(self.cursor)[0][0]
            assert all([True if sprinkle in '+x' else False for sprinkle in sprinkles])
            return sprinkles
        except Exception as e:
            self.logger.exception(str(e))
            raise Exception('AN UNEXPECTED ERROR OCCURED WHILE CHECKING THE ICECREAM.')

    def close(self, sig, frame) -> None:
        self.delete_table()
        self.cursor.close()
        self.db.close()
        print(cs("\nBYE!", "#66ff00").bold())
        sys.exit(0)
