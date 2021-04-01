import mysql.connector

class Actions:

    def __init__(self, db_data):
        db_host = db_data['host']
        db_user = db_data['user']
        db_password = db_data['password']
        db_name = db_data['database']
        db_port = db_data['port']

        self.icecream_table = db_data['icecream_table']
        try:
            self.db = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=db_port)
            self.cursor = self.db.cursor()
            self.create_table()
        except Exception as e:
            raise

    def create_table(self) -> None:
        cmd = f'create table if not exists {self.icecream_table} (id int not null auto_increment primary key, icecream varchar(64) not null, sprinkles varchar(1024) not null);'
        self.cursor.execute(cmd)
        self.db.commit()

    def exists(self, table, column, value) -> bool:
        self.db.commit()
        cmd = f'select {column} from {table} where {column} = \'{value}\';'
        self.cursor.execute(cmd)
        return len(list(self.cursor)) > 0

    def save(self, icecream, sprinkles) -> bool:
        if self.exists(self.icecream_table, 'icecream', icecream):
            return False
        cmd = f'insert into {self.icecream_table} (icecream, sprinkles) values (\'{icecream}\', \'{sprinkles}\');'
        self.cursor.execute(cmd)
        self.db.commit()
        return True
