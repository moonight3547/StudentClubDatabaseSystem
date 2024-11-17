from dbmanager import DatabaseManager, default_conn_params
from datetime import date

conn_params = default_conn_params.copy()

def create_admin():
    global conn_params
    db = DatabaseManager(conn_params, True)
    user_name = input("Please input the admin user name: ")
    passwd = input("Please input the admin password: ")
    db.create_user(user_name=user_name, passwd=passwd, is_admin = True, connection_params=conn_params)
    conn_params["user"] = user_name
    conn_params["passwd"] = passwd
    database = "student_club_database"
    db.create_database(database_name=database, connection_params=conn_params)
    conn_params["db"] = database
    db.create_table(table_name = "userlist", schema = "userlist", connection_params=conn_params)
    data = {
        "username": user_name,
        "passwd": passwd,
        "priority": "admin",
        "regdate": date.today().strftime("%Y-%m-%d")
    }
    db.insert_data(table_name = "userlist", data = data, connection_params=conn_params)
    db.log("[Info] Admin user created successfully.")
    choice = input('Are you just testing the backend and need to remove infos? [y/n]')
    if choice == 'n': 
        db.create_table(table_name = "userinfo", schema = "userinfo", connection_params=conn_params)
        db.create_table(table_name = "usercontact", schema = "usercontact", connection_params=conn_params)
        db.create_table(table_name = "clublist", schema = "clublist", connection_params=conn_params)
        db.create_table(table_name = "eventlist", schema = "eventlist", connection_params=conn_params)
        db.create_table(table_name="club_student", schema = "club_student", connection_params=conn_params)
        db.create_table(table_name="event_student", schema = "event_student", connection_params=conn_params)
        return None
    db.drop_table(table_name = "userlist", connection_params=conn_params)
    conn_params["db"] = default_conn_params["db"]
    db.drop_database(database_name=database, connection_params=conn_params)
    db.drop_user(user_name = user_name, connection_params=default_conn_params)
    conn_params = default_conn_params
    db.log("[Info] Drop all information for testing")

def create_visitor():
    pass

if __name__ == "__main__":
    create_admin()
    create_visitor()
