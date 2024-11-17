import pymysql
import cryptography
from timeit import default_timer
from dblogging import *

def get_database_connection(host = "localhost", port = 0, user = None, passwd = "", db = None, curclass = pymysql.cursors.DictCursor, connection_params = None):
    if connection_params is not None:
        host = connection_params["host"]
        port = connection_params["port"]
        user = connection_params["user"]
        passwd = connection_params["passwd"]
        db = connection_params["db"]
        curclass = connection_params["curclass"]
    connection = pymysql.connect(host = host, port = port, user = user, password = passwd, database = db, cursorclass = curclass)
    return connection

def put_database_connection(connection):
    connection.close()

class DatabaseCursor(object):
    def __init__(self, connection_params, commit = True, log_user = True, log_time = True):
        """
        param commit:       whether commit at last
        param log_time:     whether print time
        param time_label:   label for time log
        """
        self._host = connection_params["host"]
        self._port = connection_params["port"]
        self._user = connection_params["user"]
        self._password = connection_params["passwd"]
        self._database = connection_params["db"]
        self._curclass = connection_params["curclass"]
        self._commit = commit
        self._log_user = log_user
        self._log_time = log_time

    def __enter__(self):
        self.log(f"{LOG_INFO} login")
        connection = get_database_connection(self._host, self._port, self._user, self._password, self._database, self._curclass)
        connection.autocommit = False
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        self._connection = connection
        self._cursor = cursor
        return self
    
    def __exit__(self, *exc_info):
        if self._commit:
            self._connection.commit()
        self._cursor.close()
        put_database_connection(self._connection)
        self.log(f"{LOG_INFO} logout")
    
    @property
    def cursor(self):
        return self._cursor
    
    def execute(self, sql):
        try:
            self.log(f"{LOG_EXECUTE_SQL} {sql}")
            self._cursor.execute(sql)
            self.log(f"{LOG_EXECUTE_SQL} Finished.")
            return True
        except Exception as ex:
            self.log(f"{LOG_ERROR} {ex}")
            return False

    def log(self, info):
        log = f"[DBCURSOR][Database:]{self._database}"
        if self._log_user :
            log += f"[User:]{self._user}"
        if self._log_time :
            time = default_timer()
            log += f"[Time:]{time}"
        log += info
        print(log)

def get_database_cursor(connection_params):
    with DatabaseCursor(connection_params) as db:
        return db.cursor
