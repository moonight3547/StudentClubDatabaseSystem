import dbcursor
from timeit import default_timer
from datetime import date

from dbschema import *
from dblogging import *

default_conn_params = {"host": "localhost", "port": 0, "user": "root", "passwd": "", "db": None, "curclass": dbcursor.DatabaseCursor}
default_database = "student_club_database"

def get_date() :
    return date.today().strftime("%Y-%m-%d")

class Table(object):
    def __init__(self, name, schema, primary_key = None, auto_increment = None):
        self._name = name
        self._schema = list(schema.items())
        self._primary_key = self._schema[0][0] if len(self._schema) > 0 else None
        self._primary_key = primary_key if primary_key is not None else self._primary_key
    
    def __str__(self):
        info = [f" {key} {datatype}" for key, datatype in self._schema]
        for i, item in enumerate(self._schema):
            if item[0] == self._primary_key:
                info[i] += " PRIMARY KEY"
        str = ",".join(info)
        str = f"{self._name}({str})"
        return str

class DatabaseManager(object):
    def __init__(self, connection_params = default_conn_params, log_time = True):
        self._connection_params = connection_params
        self._log_time = log_time

    def log(self, info):
        log = f"[DBMANAGER]"
        if self._log_time :
            time = default_timer()
            log += f"[Time:]{time}"
        log += info
        print(log)
    
    def login(self, user_name, passwd):
        self._connection_params["user"] = user_name
        self._connection_params["passwd"] = passwd
        try:
            with dbcursor.DatabaseCursor(self._connection_params) as db:
                pass
            return True
        except Exception as ex:
            self.log(f"{LOG_ERROR} Login MySQL user: {ex}")
            self._connection_params = default_conn_params
            return False
    
    def logout(self):
        self._connection_params = default_conn_params

    def create_user(self, user_name = None, passwd = "", is_admin = False, user_ipaddr = "localhost", connection_params = default_conn_params):
        if user_name == None:
            self.log(f"{LOG_WARNING} You cannot create user without username")
            return None
        try:
            with dbcursor.DatabaseCursor(connection_params) as db:
                assert(db.execute(sql = f"CREATE USER '{user_name}'@'{user_ipaddr}' IDENTIFIED BY '{passwd}';"))
                if is_admin: 
                    assert(db.execute(sql = f"GRANT ALL PRIVILEGES ON *.* TO '{user_name}'@'{user_ipaddr}';"))
            return user_name
        except Exception as ex:
            self.log(f"{LOG_ERROR} Create MySQL user {user_name}: {ex}")

    def create_clubuser(self, user_name = None, passwd = "", db_name = "", user_ipaddr = "localhost", connection_params = default_conn_params):
        if user_name == None:
            self.log(f"{LOG_WARNING} You cannot create club user without username")
            return None
        try:
            with dbcursor.DatabaseCursor(connection_params) as db:
                assert(db.execute(sql = f"CREATE USER '{user_name}'@'{user_ipaddr}' IDENTIFIED BY '{passwd}';"))
                assert(db.execute(sql = f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{user_name}'@'{user_ipaddr}';"))
            return user_name
        except Exception as ex:
            self.log(f"{LOG_ERROR} Create MySQL user {user_name}: {ex}")

    #! NOTE THAT THIS FUNCTION IS NOT PROTECTING USER FROM VALIDATION
    def drop_user(self, user_name = None, user_ipaddr = "localhost", connection_params = default_conn_params):
        if user_name == None:
            self.log(f"{LOG_WARNING} You cannot drop user without login")
            return None
        try:
            with dbcursor.DatabaseCursor(connection_params) as db:
                db.cursor.execute(f"DROP USER '{user_name}'@'{user_ipaddr}';")
        except Exception as ex:
            self.log(f"{LOG_ERROR} Drop MySQL user: {ex}")

    def create_database(self, database_name = None, connection_params = default_conn_params):
        if database_name == None:
            self.log(f"{LOG_WARNING} You cannot create database without a name")
            return None
        connection_params["db"] = None
        try:
            with dbcursor.DatabaseCursor(connection_params) as db:
                assert(db.execute(sql = f"CREATE DATABASE {database_name};"))
            return database_name
        except Exception as ex:
            self.log(f"{LOG_ERROR} Create MySQL database: {ex}")
    
    def drop_database(self, database_name = None, connection_params = default_conn_params):
        if database_name == None:
            self.log(f"{LOG_WARNING} You cannot drop database without its name")
            return None
        connection_params["db"] = None
        try:
            with dbcursor.DatabaseCursor(connection_params) as db:
                assert(db.execute(sql = f"DROP DATABASE {database_name};"))
            return database_name
        except Exception as ex:
            self.log(f"{LOG_ERROR} Create MySQL database: {ex}")
    
    def create_table(self, table_name = None, schema = None, columns_dict = None, connection_params = default_conn_params):
        if table_name == None or schema == None :
            self.log(f"{LOG_WARNING} You cannot create table without name and schema")
            return None
        table = Table(table_name, schema_list[schema], columns_dict)
        table_info = table.__str__()
        try:
            with dbcursor.DatabaseCursor(connection_params) as db:
                assert(db.execute(sql = f"CREATE TABLE {table_info};"))
            self.log(f"{LOG_INFO} Create MySQL table {table_info} successfully")
            return table_name
        except Exception as ex:
            self.log(f"{LOG_ERROR} Create MySQL table: {ex}")
    
    def drop_table(self, table_name = None, connection_params = default_conn_params):
        if table_name == None:
            self.log(f"{LOG_WARNING} You cannot drop table without name")
            return None
        try:
            with dbcursor.DatabaseCursor(connection_params) as db:
                assert(db.execute(sql = f"DROP TABLE {table_name};"))
            self.log(f"{LOG_INFO} Drop MySQL table {table_name} successfully")
        except Exception as ex:
            self.log(f"{LOG_ERROR} Drop MySQL table: {ex}")
    
    def insert_data(self, table_name = None, data = None, connection_params = default_conn_params):
        if table_name == None or data == None:
            self.log(f"{LOG_WARNING} You cannot insert data without table name and data")
            return None
        try:
            keys, values = data.keys(), data.values()
            values = [f"'{value}'" if isinstance(value, str) else value.__str__() for value in values]
            data_keys = f"({','.join(keys)})"
            data_values = f"({','.join(values)})"
            with dbcursor.DatabaseCursor(connection_params) as db:
                assert(db.execute(sql = f"INSERT INTO {table_name} {data_keys} VALUES {data_values};"))
            self.log(f"{LOG_INFO} Insert data {data} into MySQL table {table_name} successfully")
            return table_name
        except Exception as ex:
            self.log(f"{LOG_ERROR} Insert data {data} into MySQL table {table_name}: {ex}")
    
    def query_user_byname(self, username, connection_params = default_conn_params):
        try:
            connection_params["db"] = default_database
            with dbcursor.DatabaseCursor(connection_params) as db:
                assert(db.execute(sql = f"SELECT * FROM userlist WHERE username = '{username}';"))
                user_info = db.cursor.fetchone()
                self.log(f"{LOG_INFO} Query user {username} and get information {user_info} in MySQL database successfully")
                return user_info
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query user info by name in MySQL database: {ex}")

    def query_user_priority(self, user, passwd, connection_params = default_conn_params):
        try:
            connection_params["db"] = default_database
            userid, priority = -1, None
            with dbcursor.DatabaseCursor(connection_params) as db:
                print("connected!")
                assert(db.execute(sql = f"SELECT * FROM userlist WHERE username = '{user}';"))
                user_info = db.cursor.fetchone()
                print(user_info)
                if user_info != None and user_info["passwd"] == passwd:
                    userid, priority = user_info["userid"], user_info["priority"]                    
            self.log(f"{LOG_INFO} Query user {user} has priority {priority} in MySQL database successfully")
            return userid, priority
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query user priority in MySQL database: {ex}")
    
    def query_user(self, userid, connection_params = default_conn_params):
        try:
            connection_params["db"] = default_database
            user_info = dict()
            with dbcursor.DatabaseCursor(connection_params) as db:
                for key, value in userlist_schema.items(): user_info[key] = "-"
                for key, value in userinfo_schema.items(): user_info[key] = "-"
                for key, value in usercontact_schema.items(): user_info[key] = "-"
                user_info["userid"] = userid
                assert(db.execute(sql = f"SELECT * FROM userlist WHERE userid = {userid};"))
                query = db.cursor.fetchone()
                for key, value in query.items(): user_info[key] = value if value is not None else "-"
                assert(db.execute(sql = f"SELECT * FROM userinfo WHERE userid = {userid};"))
                query = db.cursor.fetchone()
                if query != None:
                    for key, value in query.items(): user_info[key] = value if value is not None else "-"
                assert(db.execute(sql = f"SELECT * FROM usercontact WHERE userid = {userid};"))
                query = db.cursor.fetchone()
                if query != None:
                    for key, value in query.items(): user_info[key] = value if value is not None else "-"
            username = user_info["username"]
            self.log(f"{LOG_INFO} Query user {username} and get information {user_info} in MySQL database successfully")
            return user_info
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query user information in MySQL database: {ex}")
            return None
    
    def update_user(self, user, userid, user_info, connection_params = default_conn_params):
        try:
            connection_params["db"] = default_database
            userlist_data = dict()
            userinfo_data = dict()
            usercontact_data = dict()
            for key, value in user_info.items():
                if value is None: continue
                if key in userlist_schema.keys(): 
                    userlist_data[key] = f"'{value}'" if isinstance(value, str) else value.__str__()
                if key in userinfo_schema.keys(): 
                    userinfo_data[key] = f"'{value}'" if isinstance(value, str) else value.__str__()
                if key in usercontact_schema.keys(): 
                    usercontact_data[key] = f"'{value}'" if isinstance(value, str) else value.__str__()
            if len(userlist_data):
                userlist_update = ','.join([f"{key} = {value} " for key, value in userlist_data.items()])
            if len(userinfo_data):
                userinfo_update = ','.join([f"{key} = {value} " for key, value in userinfo_data.items()])
            if len(usercontact_data):
                usercontact_update = ','.join([f"{key} = {value} " for key, value in usercontact_data.items()])
            with dbcursor.DatabaseCursor(connection_params) as db:
                if len(userlist_data):
                    assert(db.execute(f"UPDATE userlist SET {userlist_update} WHERE userid = {userid};"))
                if len(userinfo_data):
                    assert(db.execute(f"UPDATE userinfo SET {userinfo_update} WHERE userid = {userid};"))
                if len(usercontact_data):
                    assert(db.execute(f"UPDATE usercontact SET {usercontact_update} WHERE userid = {userid};"))
            self.log(f"{LOG_INFO} Update user {user}(userid = {userid}) profile with information {user_info} in MySQL database successfully")
            return user
        except Exception as ex:
            self.log(f"{LOG_ERROR} Update user information in MySQL database: {ex}")
        
    def insert_userlist(self, user, passwd, priority = "user", connection_params = default_conn_params):
        try:
            data = {
                "username": user,
                "passwd": passwd,
                "priority": priority,
                "regdate": get_date()
            }
            connection_params["db"] = default_database
            self.insert_data(table_name = "userlist", data = data, connection_params = connection_params)
            userid, priority = self.query_user_priority(user, passwd)
            data = {key:"" for key, value in userinfo_schema.items()}
            data["userid"] = userid
            data["username"] = user
            self.insert_data(table_name = "userinfo", data = data, connection_params = connection_params)
            data = {key:"" for key, value in usercontact_schema.items()}
            data["userid"] = userid
            data["username"] = user
            self.insert_data(table_name = "usercontact", data = data, connection_params = connection_params)
            self.log(f"{LOG_INFO} Insert the user {user} into userlist in MySQL database successfully")
            return user
        except Exception as ex:
            self.log(f"{LOG_ERROR} Insert a user into userlist in MySQL database: {ex}")
                
    def create_club(self, user_name, club_name, passwd):
        try:
            #* Create database
            database_name = user_name.lower()+"_database"
            print(database_name)
            assert(self.create_database(database_name = database_name))
            #* Create user
            assert(self.create_clubuser(user_name = user_name, passwd = passwd, db_name = database_name))
            assert(self.insert_userlist(user = user_name, passwd = passwd, priority = "club-admin"))
            conn_params = default_conn_params.copy()
            conn_params["db"] = default_database
            club_data = {
                "club": user_name,
                "clubname": club_name,
                "num_students": 0,
                "num_events": 0
            }
            assert(self.insert_data(table_name="clublist", data = club_data, connection_params=conn_params))
            conn_params["user"] = user_name
            conn_params["passwd"] = passwd
            conn_params["db"] = database_name
            assert(self.create_table(table_name = "studentlist", schema = "studentlist", connection_params = conn_params))
            assert(self.create_table(table_name = "eventlist", schema = "eventlist", connection_params = conn_params))
            return club_name
        except Exception as ex:
            self.log(f"{LOG_ERROR} Create club {club_name} in MySQL database: {ex}")

    def query_club(self, club, connection_params = default_conn_params):
        try:
            connection_params["db"] = default_database
            club_info = dict()
            with dbcursor.DatabaseCursor(connection_params) as db:
                for key, value in clublist_schema.items(): club_info[key] = "-"
                club_info["club"] = club
                assert(db.execute(sql = f"SELECT * FROM userlist WHERE username = '{club}';"))
                query = db.cursor.fetchone()
                club_info["passwd"] = query["passwd"]
                club_info["priority"] = query["priority"]
                club_info["regdate"] = query["regdate"]
                assert(db.execute(sql = f"SELECT * FROM clublist WHERE club = '{club}';"))
                query = db.cursor.fetchone()
                for key, value in query.items(): club_info[key] = value if value is not None else "-"
            clubname = club_info["clubname"]
            self.log(f"{LOG_INFO} Query club {clubname} and get information {club_info} in MySQL database successfully")
            return club_info
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query user information in MySQL database: {ex}")
            return None

    def query_user_clubs(self, user):
        try:
            conn_params = default_conn_params.copy()
#            conn_params["db"] = default_database
            with dbcursor.DatabaseCursor(conn_params) as db:
                assert(db.execute(sql = f"SELECT * FROM {default_database}.clublist WHERE club IN (SELECT club FROM {default_database}.club_student WHERE student = '{user}');"))
                self.log(f"{LOG_INFO} Query the clubs of user {user}.")
                query = db.cursor.fetchall()
                self.log(f"{LOG_INFO} Query the clubs of user {user} and get information {query}.")
                return query
            return -1
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query the club information of user {user} in MySQL database: {ex}")
            return -1

    def query_clubs(self, connection_params = default_conn_params):
        try:
            connection_params["db"] = default_database
            with dbcursor.DatabaseCursor(connection_params) as db:
                assert(db.execute(sql = f"SELECT * FROM clublist ORDER BY clubname;"))
                query = db.cursor.fetchall()
                self.log(f"{LOG_INFO} Query all clubs and get information {query} in MySQL database successfully")
                return query
            return None
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query user information in MySQL database: {ex}")
            return None

    def update_club(self, club, club_info, connection_params = default_conn_params):
        try:
            connection_params["db"] = default_database
            userlist_data = dict()
            clublist_data = dict()
            club_info = dict(club_info)
            for key, value in club_info.items():
                if value == "": continue
                val = eval(value) if key == "last_year_expense" or key == "annual_budget" else value
                val = f"'{value}'" if isinstance(value, str) else value.__str__()
                if key in userlist_schema.keys(): userlist_data[key] = val
                if key in clublist_schema.keys(): clublist_data[key] = val
#            print(userlist_data, clublist_data)
            if len(userlist_data):
                userlist_update = ','.join([f"{key} = {value} " for key, value in userlist_data.items()])
            if len(clublist_data):
                clublist_update = ','.join([f"{key} = {value} " for key, value in clublist_data.items()])
            with dbcursor.DatabaseCursor(connection_params) as db:
                if len(userlist_data):
                    assert(db.execute(sql = f"UPDATE userlist SET {userlist_update} WHERE username = '{club}';"))
                if len(clublist_data):
                    assert(db.execute(sql = f"UPDATE clublist SET {clublist_update} WHERE club = '{club}';"))
            self.log(f"{LOG_INFO} Update club-admin user {club} profile with information {club_info} in MySQL database successfully")
            return club
        except Exception as ex:
            self.log(f"{LOG_ERROR} Update club information in MySQL database: {ex}")

    def create_event(self, club, club_name, event_info):
        try:
            #* Create database
            database_name = club.lower()+"_database"
            print(database_name)
            event_info = dict(event_info)
            event_info["club"] = club
            event_info["clubname"] = club_name
            event_info["num_students"] = 0
            event = event_info['event']
            conn_params = default_conn_params.copy()
            conn_params["db"] = database_name
            with dbcursor.DatabaseCursor(conn_params) as db:
                assert(db.execute(sql = f"SELECT * FROM eventlist WHERE event = '{event}';"))
                query = db.cursor.fetchone()
                if query is not None:
                    self.log(f"{LOG_ERROR} Create event {event} in MySQL database: Event already exists")
                    return None
            assert(self.insert_data(table_name="eventlist", data = event_info, connection_params=conn_params))
            conn_params["db"] = default_database
            assert(self.insert_data(table_name="eventlist", data = event_info, connection_params=conn_params))
            return event
        except Exception as ex:
            self.log(f"{LOG_ERROR} Create event {event} in MySQL database: {ex}")

    def query_event_id(self, club, event):
        try:
            conn_params = default_conn_params.copy()
            conn_params["db"] = default_database
            with dbcursor.DatabaseCursor(conn_params) as db:
                assert(db.execute(sql = f"SELECT * FROM eventlist WHERE club = '{club}' and event = '{event}';"))
                query = db.cursor.fetchone()
                self.log("Query Event Id and get the event {query}")
                return query["eventid"]
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query event {event} id in MySQL database: {ex}")
    
    def query_event(self, eventid):
        try:
            conn_params = default_conn_params.copy()
            conn_params["db"] = default_database
            with dbcursor.DatabaseCursor(conn_params) as db:
                assert(db.execute(sql = f"SELECT * FROM eventlist WHERE eventid = {eventid};"))
                query = db.cursor.fetchone()
                return query
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query the event information of eventid = {eventid} in MySQL database: {ex}")

    def query_events(self, club):
        try:
            conn_params = default_conn_params.copy()
            conn_params["db"] = default_database #club.lower()+"_database"
            with dbcursor.DatabaseCursor(conn_params) as db:
                assert(db.execute(sql = f"SELECT * FROM eventlist WHERE club = '{club}' ORDER BY event_date DESC;"))
                query = db.cursor.fetchall()
                return query
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query the events information of club with username {club} in MySQL database: {ex}")

    def query_user_events(self, user):
        try:
            conn_params = default_conn_params.copy()
#            conn_params["db"] = default_database
            with dbcursor.DatabaseCursor(conn_params) as db:
                assert(db.execute(sql = f"SELECT * FROM {default_database}.eventlist WHERE eventid IN (SELECT eventid FROM {default_database}.event_student WHERE student = '{user}');"))
                self.log(f"{LOG_INFO} Query the events of username {user}.")
                query = db.cursor.fetchall()
                self.log(f"{LOG_INFO} Query the events of username {user} and get information {query}.")
                return query
            return -1
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query the event information of username {user} in MySQL database: {ex}")
            return -1

    def query_all_events(self, connection_params = default_conn_params):
        try:
            connection_params["db"] = default_database
            with dbcursor.DatabaseCursor(connection_params) as db:
                assert(db.execute(sql = f"SELECT * FROM eventlist ORDER BY event_date;"))
                query = db.cursor.fetchall()
                self.log(f"{LOG_INFO} Query all clubs and get information {query} in MySQL database successfully")
                return query
            return None
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query user information in MySQL database: {ex}")
            return None

    def update_event(self, club, eventid, event_info):
        try:
            #* Create database
            database_name = club.lower()+"_database"
#            event_info = dict(event_info)
            eventlist_data = dict()
            for key, value in event_info.items():
                if value == "": continue 
                print(key, value, type(value))
                eventlist_data[key] = f"'{value}'" if isinstance(value, str) else value.__str__()
            if len(eventlist_data) == 0:
                return eventid
            eventlist_update = ','.join([f" {key} = {value}" for key, value in eventlist_data.items()])
            print(eventlist_update)
            conn_params = default_conn_params.copy()
            conn_params["db"] = database_name
            with dbcursor.DatabaseCursor(conn_params) as db:
                assert(db.execute(sql = f"UPDATE eventlist SET {eventlist_update} WHERE eventid = {eventid};"))
            conn_params["db"] = default_database
            with dbcursor.DatabaseCursor(conn_params) as db:
                assert(db.execute(sql = f"UPDATE eventlist SET {eventlist_update} WHERE eventid = {eventid};"))
            return eventid
        except Exception as ex:
            self.log(f"{LOG_ERROR} Update event with eventid={eventid} in MySQL database: {ex}")
    
    def join_event(self, user_name, event_id, user_info, event_info):
        try:
            conn_params = default_conn_params.copy()
            conn_params["db"] = default_database
            data = {
                "eventid": event_id, 
                "event": event_info["event"], 
                "studentid": user_info["userid"], 
                "student": user_name
            }
            assert(self.insert_data(table_name="event_student", data=data, connection_params=conn_params))
            self.log(f"{LOG_INFO} Join event with eventid={event_id} in MySQL database successfully.")
            num_students = event_info["num_students"]+1 if event_info["num_students"] else 1
            assert(num_students <= event_info["lim_students"])
            assert(self.update_event(club = event_info["club"], eventid = event_id, event_info = {"num_students": num_students}))
            self.log(f"{LOG_INFO} Update event with eventid={event_id} in MySQL database successfully.")
            return event_id
        except Exception as ex:
            self.log(f"{LOG_ERROR} Join event with eventid={event_id} in MySQL database: {ex}")

    def join_club(self, user_name, club, user_info, club_info):
        try:
            conn_params = default_conn_params.copy()
            conn_params["db"] = default_database
            club_name = club_info["clubname"]
            data = {
                "clubid": club_info["clubid"],
                "club": club,
                "clubname": club_name,
                "studentid": user_info["userid"],
                "student": user_name 
            }
            assert(self.insert_data(table_name="club_student", data=data, connection_params=conn_params))
            self.log(f"{LOG_INFO} Join club {club_name} in MySQL database successfully.")
            num_students = club_info["num_students"]+1 if isinstance(club_info["num_students"], int) else 1
            assert(self.update_club(club=club, club_info={"num_students": num_students}, connection_params=conn_params))
            self.log(f"{LOG_INFO} Update the club {club_name} in MySQL database successfully.")
            conn_params["db"] = club.lower() + "_database"
            student_data = {key : user_info[key] for key in studentlist_schema.keys()} 
            print(student_data)
            assert(self.insert_data(table_name="studentlist", data=student_data, connection_params=conn_params))
            self.log(f"{LOG_INFO} Add student infos into student list of club {club_name} in MySQL database successfully.")
            return club
        except Exception as ex:
            self.log(f"{LOG_ERROR} Join club with club-admin {club} in MySQL database: {ex}")

    #todo
    def query(self, query, connection_params = default_conn_params):
        try:
            with dbcursor.DatabaseCursor(connection_params) as db:
                assert(db.execute(sql = query))
            return db.cursor.fetchall()
        except Exception as ex:
            log(f"{LOG_ERROR} Query MySQL database: {ex}")
    
    def query_club_students(self, club):
        try:
            conn_params = default_conn_params.copy()
            conn_params["db"] = default_database
            query1 = None
            with dbcursor.DatabaseCursor(conn_params) as db:
                sql = f"SELECT student, major, clubname, eventlist.event as eventt, event_date, location FROM eventlist INNER JOIN (SELECT event, eventid, student, major FROM event_student INNER JOIN userinfo ON student = username) AS tmp_table ON eventlist.eventid = tmp_table.eventid WHERE eventlist.club = '{club}' ORDER BY event_date;"
                assert(db.execute(sql = sql))
                query1 = db.cursor.fetchall()
            conn_params["db"] = club.lower() + "_database"
            query2 = None
            with dbcursor.DatabaseCursor(conn_params) as db:
                sql = "SELECT * FROM studentlist;"
                assert(db.execute(sql = sql))
                query2 = db.cursor.fetchall()
            return (query1, query2)
        except Exception as ex:
            self.log(f"{LOG_ERROR} Query students in MySQL database: {ex}")
            return -1

#if __name__ == "__main__":
#    DBM = DatabaseManager()
#    DBM.create_club(club_name = "StatisticsAlliance")
