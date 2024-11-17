userlist_schema = {
    "userid": "int auto_increment", 
    "username": "varchar(20) not null",
    "passwd": "varchar(20)",
    "priority": "varchar(10)",
    "regdate": "varchar(20)", 
}

userinfo_schema = {
    "userid": "int", 
    "gender": "varchar(30)", 
    "affilication": "varchar(30)",
    "stuid": "varchar(20)",
    "grade": "varchar(4)", 
    "school": "varchar(30)",
    "major": "varchar(20)",
    "interest": "varchar(20)",
    "username": "varchar(20), FOREIGN KEY(username) REFERENCES userlist(username)"
}

usercontact_schema = {
    "userid": "int", 
    "username": "varchar(20) FOREIGN KEY(username) REFERENCES userlist(username)",
    "email": "varchar(30)",
    "phone": "varchar(20)",
    "wechat": "varchar(20)",
    "address": "varchar(100)", 
    "postal": "varchar(10)"
}

clublist_schema = {
    "clubid": "int auto_increment", 
    "club": "varchar(20) not null", 
    "clubname": "varchar(30)",
    "affilication": "varchar(30)",
    "school": "varchar(30)",
    "num_students": "int", 
    "num_events": "int", 
    "annual_budget": "int", 
    "last_year_expense": "float", 
    "type": "varchar(30)",
    "field": "varchar(30)",
    "club_info": "varchar(100)",
    "club_desc": "varchar(1000)"
}

eventlist_schema = {
    "eventid": "int auto_increment",
    "event": "varchar(50)",
    "club": "varchar(20) not null",
    "clubname": "varchar(30)",
    "num_students": "int", 
    "lim_students": "int", 
    "event_date": "varchar(20)", 
    "location": "varchar(100)",
    "join_ddl": "varchar(20)",
    "completed": "bool",
    "out_campus": "bool",
    "transportation": "bool", 
    "type": "varchar(30)",
    "budget": "int",
    "event_info": "varchar(100)",
    "event_desc": "varchar(1000)",
}

club_student_schema = {
    "cspairid": "int auto_increment", 
    "club": "varchar(20) not null FOREIGN KEY REFERENCES clublist(club)", 
    "clubid": "int FOREIGN KEY REFERENCES clublist(clubid)",
    "clubname": "varchar(30) FOREIGN KEY REFERENCES clublist(clubname)", 
    "studentid": "int FOREIGN KEY REFERENCES userlist(userid)", 
    "student": "varchar(20) not null FOREIGN KEY REFERENCES userlist(username)"
}

event_student_schema = {
    "espairid": "int auto_increment",
    "event": "varchar(50) FOREIGN KEY REFERENCES eventlist(event)", 
    "eventid": "int FOREIGN KEY REFERENCES eventlist(eventid)", 
    "studentid": "int FOREIGN KEY REFERENCES userlist(userid)", 
    "student": "varchar(20) not null FOREIGN KEY REFERENCES FOREIGN KEY REFERENCES userlist(username)"
}

studentlist_schema = {
    "userid": "int", 
    "username": "varchar(20) not null",
    "gender": "varchar(30)", 
    "affilication": "varchar(30)",
    "stuid": "varchar(20)",
    "grade": "varchar(4)", 
    "school": "varchar(30)",
    "major": "varchar(20)",
    "interest": "varchar(20)",
    "email": "varchar(30)",
    "phone": "varchar(20)",
    "wechat": "varchar(20)",
    "address": "varchar(100)", 
    "postal": "varchar(10)"
}

schema_list = {
    "userlist": userlist_schema,
    "userinfo": userinfo_schema,
    "usercontact": usercontact_schema,
    "clublist": clublist_schema,
    "eventlist": eventlist_schema,
    "club_student": club_student_schema,
    "event_student": event_student_schema,
    "studentlist": studentlist_schema
}
