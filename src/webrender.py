from flask import Flask, render_template
from flask import redirect, url_for, request, jsonify
from dbmanager import DatabaseManager
from dblogging import *

app = Flask(__name__)
school = "Chinese University of Hong Kong (Shenzhen)"
dbm = DatabaseManager()
user = "visitor"
userid = -1
default_db = "student_club_database"

def log(info):
    print(f"[WEBRENDER]{info}")

@app.route('/')
def index():
    return render_template('index.html', school=school)

@app.route('/click_login')
def button_login():
    return redirect(url_for('login'))

@app.route('/click_register')
def button_register():
    return redirect(url_for('register'))

@app.route('/logout')
def logout():
    global user
    user = "visitor"
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html', school=school, note="")

@app.route('/login/note=<note>')
def login_note(note):
    return render_template('login.html', school=school, note=note)

@app.route('/login/click_enter', methods = ['POST'])
def login_enter():
    global user, userid
    user = request.values.get("username")
    passwd = request.values.get("passwd")
    log(f"{LOG_INFO} Login: username = {user} password = {passwd}")
    try :
        userid, priority = dbm.query_user_priority(user, passwd)
        log(f"{LOG_INFO} Login: username = {user} userid = {userid} with priority {priority}.")
        if (priority == "admin"):
            return redirect(url_for('admin', user_name = user))
        elif (priority == "club-admin"):
            return redirect(url_for('club_profile', club = user))
        elif (priority == "user"):
            return redirect(url_for('profile', user_name = user))
        elif (priority == None and userid == -1):
            user, userid = "visitor", -1
            return redirect(url_for('login_note', note = "Fail to login. Username or password is wrong.")) 
        else :
            user, userid = "visitor", -1
            return redirect(url_for('login_note', note = "Your account meets some error incurring undefined priority.")) 
    except:
        user, userid = "visitor", -1
        return redirect(url_for('login_note', note = "Your account meets some unknown error.")) 

@app.route('/register')
def register():
    return render_template('register.html', school=school, note = "")

@app.route('/register/note=<note>')
def register_note(note):
    return render_template('register.html', school=school, note = note)

@app.route('/register/click_enter', methods = ['POST'])
def register_enter():
    user = request.values.get("username")
    passwd = request.values.get("passwd")
    log(f"{LOG_INFO} Register: username = {user} password = {passwd}")
    try :
        userid, priority = dbm.query_user_priority(user, passwd)
        print(userid, priority)
        if (priority == None and userid == -1):
            dbm.insert_userlist(user, passwd)
            log(f"{LOG_INFO} Register successfully. username = {user} password = {passwd}")
            return redirect(url_for('login_note', note = "Register successfully."))
        else :
            log(f"{LOG_INFO} Register failed. Username {user} already exists.")
            return redirect(url_for('register_note', note = "Fail to register. Username already exists.")) 
    except:
        return redirect(url_for('register_note', note = "Your account meets some unknown error.")) 

@app.route('/profile/<user_name>')
def profile(user_name):
    return render_template('profile.html', school=school, user=user_name, note = "")

@app.route('/profile/<user_name>/note=<note>')
def profile_note(user_name, note):
    return render_template('profile.html', school=school, user=user_name, note = note)

@app.route('/profile/<user_name>/display', methods = ["GET"])
def profile_display(user_name):
    user_info = dbm.query_user(userid)
    log(f"{LOG_INFO} Query user profile {user_info}.")
    return render_template('profile-display.html', school=school, user=user_name, info = user_info)

@app.route('/profile/<user_name>/update')
def profile_update(user_name):
    global userid, user
    user_info = dbm.query_user(userid)
    log(f"{LOG_INFO} Query user profile {user_info}.")
    return render_template('profile-update.html', school=school, user=user_name, info = user_info)

@app.route('/profile/<user_name>/update/complete', methods = ['POST'])
def profile_complete(user_name):
    global userid, user
    user_info = request.values
    dbm.update_user(user, userid, user_info)
    log(f"{LOG_INFO} Update user profile {user_info}.")
    return redirect(url_for('profile_display', user_name=user_name))

@app.route('/admin')
def admin():
    global user
    return render_template('admin/admin.html', school=school, user = user)

@app.route('/admin/note=<note>')
def admin_note(note):
    global user
    return render_template('admin/admin.html', school=school, user = user, note=note)

@app.route('/admin/createclub')
def admin_create_club():
    global user
    return render_template('admin/create-club.html', school=school, user = user)

@app.route('/admin/createclub/complete', methods = ["POST"])
def club_creation_complete():
    user = request.values.get("username")
    clubname = request.values.get("clubname")
    passwd = request.values.get("passwd")
    log(f"{LOG_INFO} Club Register: username = {user} password = {passwd}")
    try :
        userid, priority = dbm.query_user_priority(user, passwd)
        print(userid, priority)
        if (priority == None and userid == -1):
            assert(dbm.create_club(user, clubname, passwd))
            log(f"{LOG_INFO} Club {clubname} Register successfully. username = {user} password = {passwd}")
            return redirect(url_for('admin_note', note = f"The club {clubname} register successfully."))
        else :
            log(f"{LOG_INFO} Register failed. Clubname {user} already exists.")
            return redirect(url_for('admin_note', note = "Fail to register the club. Clubname already exists.")) 
    except:
        return redirect(url_for('admin_note', note = "The club account meets some unknown error.")) 

@app.route('/clubs/profile/<club>')
def club_profile(club):
    assert(user == club)
    club_info = dbm.query_club(club = club)
    print(club_info)
    club_name = club_info["clubname"]
    club_desc = club_info["club_desc"]
    club_desc = club_desc if club_desc is not None and len(club_desc) > 4 else "Temporarily Empty ~"
    return render_template('club-admin/profile.html', school=school, user = club, club_name = club_name, club_desc = club_desc)

@app.route('/clubs/profile/<club>/note=<note>')
def club_profile_note(club, note):
    assert(user == club)
    club_info = dbm.query_club(club = club)
    print(club_info)
    club_name = club_info["clubname"]
    club_desc = club_info["club_desc"]
    club_desc = club_desc if club_desc is not None and len(club_desc) > 4 else "Temporarily Empty ~"
    return render_template('club-admin/profile.html', school=school, user = club, club_name = club_name, club_desc = club_desc, note = note)

@app.route('/clubs/profile/<club>/display')
def club_profile_display(club):
    assert(user == club)
    club_info = dbm.query_club(club = club)
    club_name = club_info["clubname"]
    club_desc = club_info["club_desc"]
    club_desc = club_desc if club_desc is not None and len(club_desc) > 4 else "Temporarily Empty ~"
    log(f"{LOG_INFO} Query user profile {club_info}.")
    return render_template('club-admin/profile-display.html', school=school, user=club, club_name = club_name, club_desc = club_desc, info = club_info)

@app.route('/clubs/profile/<club>/update')
def club_profile_update(club):
    assert(user == club)
    club_info = dbm.query_club(club = club)
    club_name = club_info["clubname"]
    club_desc = club_info["club_desc"]
    club_desc = club_desc if club_desc is not None and len(club_desc) > 4 else "Temporarily Empty ~"
    log(f"{LOG_INFO} Query user profile {club_info}.")
    return render_template('club-admin/profile-update.html', school=school, user=club, club_name = club_name, club_desc = club_desc, info = club_info)

@app.route('/clubs/profile/<club>/update/complete', methods = ['POST'])
def club_profile_complete(club):
    assert(user == club)
    club_info = request.values
    dbm.update_club(club, club_info)
    log(f"{LOG_INFO} Update club profile {club_info}.")
    return redirect(url_for('club_profile_display', club = club))

@app.route('/clubs/<club>/createevent')
def club_create_event(club):
    assert(user == club)
    club_info = dbm.query_club(club = club)
    club_name = club_info["clubname"]
    return render_template('club-admin/create-event.html', school=school, user = club, club_name = club_name)

@app.route('/clubs/<club>/createevent/complete', methods = ["POST"])
def event_creation_complete(club):
    assert(user == club)
    try :
        club_info = dbm.query_club(club = club)
        club_name = club_info["clubname"]
        event_info = request.values
        event_name = dbm.create_event(club, club_name, event_info)
        log(f"{LOG_INFO} event name = {event_name}")
        if event_name is not None :
            log(f"{LOG_INFO} Club {club_name} create an event {event_name} successfully. ")
            eventid = dbm.query_event_id(club, event_name)
            log(f"{LOG_INFO} eventid = {eventid}")
            return redirect(url_for('event_profile', club = club, eventid = eventid))
        else :
            log(f"{LOG_INFO} Register failed. Clubname {club_name} already created event {event_name}.")
            return redirect(url_for('club_profile_note', club = club, note = "Fail to create the event. Same event of the same club already exists.")) 
    except:
        log(f"{LOG_ERROR} The event creation or event id query meets some unknown error.")
        return redirect(url_for('club_profile_note', club = club, note = "The event creation meets some unknown error.")) 

@app.route('/clubs/<club>/events/profile/eventid=<eventid>')
def event_profile(club, eventid):
#    assert(user == club)
    club_info = dbm.query_club(club = club)
    log(f"{LOG_INFO} Query club profile {club_info}.")
    club_name = club_info["clubname"]
    club_desc = club_info["club_desc"]
    club_desc = club_desc if club_desc is not None and len(club_desc) > 4 else "Temporarily Empty ~"
    event_info = dbm.query_event(eventid = eventid)
    log(f"{LOG_INFO} Query event profile {event_info}.")
    event_name = event_info["event"]
    event_desc = event_info["event_desc"]
    event_desc = event_desc if event_desc is not None and len(event_desc) > 4 else "Temporarily Empty ~"
    return render_template('event/profile.html', school=school, user = club, club_name = club_name, eventid = eventid, event_name = event_name, club_desc = club_desc, event_desc = event_desc)

@app.route('/clubs/<club>/events/profile/eventid=<eventid>/display')
def event_profile_display(club, eventid):
#    assert(user == club)
    event_info = dbm.query_event(eventid = eventid)
    club_name = event_info["clubname"]
    log(f"{LOG_INFO} Query event profile {event_info}.")
    return render_template('event/profile-display.html', school=school, user=club, club_name = club_name, eventid = eventid, info = event_info)

@app.route('/clubs/<club>/events/profile/eventid=<eventid>/update')
def event_profile_update(club, eventid):
#    assert(user == club)
    event_info = dbm.query_event(eventid = eventid)
    club_name = event_info["clubname"]
    log(f"{LOG_INFO} Query event profile {event_info}.")
    return render_template('event/profile-update.html', school=school, user=club, club_name = club_name, eventid = eventid, info = event_info)

@app.route('/clubs/<club>/events/profile/eventid=<eventid>/update/complete', methods = ['POST'])
def event_profile_complete(club, eventid):
#    assert(user == club)
    event_info = request.values
    print(event_info)
    dbm.update_event(club, eventid, event_info)
    log(f"{LOG_INFO} Update event profile {event_info}.")
    return redirect(url_for('event_profile_display', club = club, eventid = eventid))

@app.route('/clubs/profile/<club>/events')
def club_profile_events(club):
    global user
    club_info = dbm.query_club(club = club)
    log(f"{LOG_INFO} Query club profile {club_info}.")
    club_name = club_info["clubname"]
    club_desc = club_info["club_desc"]
    club_desc = club_desc if club_desc is not None and len(club_desc) > 4 else "Temporarily Empty ~"
    events = dbm.query_events(club = club)
    log(f"{LOG_INFO} Query all events of the club: {events}.")
    return render_template('club-admin/events.html', school=school, user = user, club=club, club_name = club_name, club_desc = club_desc, events=events)

@app.route('/clubs')
def clubs():
    global user
    clubs = dbm.query_clubs()
    return render_template("clubs.html", school=school, user = user, clubs = clubs)

@app.route('/clubs/<club>')
def club(club):
    global user
    club_info = dbm.query_club(club)
    return render_template("club.html", school=school, user = user, club = club, info=club_info, note="")

@app.route('/clubs/<club>/note=<note>')
def club_note(club, note):
    global user
    club_info = dbm.query_club(club)
    return render_template("club.html", school=school, user = user, club = club, info=club_info, note=note)

@app.route('/clubs/<club>/joinclub/user=<user_name>')
def club_join(club, user_name):
    # Make Sure User Login
    print(user_name, club)
    try:
        global user
        if user_name != user:
            log(f"{LOG_WARNING} User {user_name} not exist or just visitor.")
            return redirect(url_for('login_note', note = f"User {user_name} not stable in the network."))
        user_info = dbm.query_user_byname(user_name)
        userid = user_info["userid"]
        user_info = dbm.query_user(userid)
        print(f"{LOG_INFO} Get user information {user_info}.")
        if user_info is None:
            log(f"{LOG_WARNING} User {user_name} not exist or just visitor.")
            return redirect(url_for('login_note', note = f"User {user_name} not exist or just visitor."))
        clubs = dbm.query_user_clubs(user_name)
        assert(clubs != -1)
        for c in clubs:
            if c["club"] == club:
                log(f"{LOG_WARNING} User {user_name} already joined the club with club-admin {club}.")
                return redirect(url_for('club_note', club = club, note = "You already joined the event."))
        club_info = dbm.query_club(club)
        club_name = club_info["clubname"]
        assert(club_info)
        assert(dbm.join_club(user_name, club, user_info, club_info))
        print(club_info)
        log(f"{LOG_INFO} User {user_name} succeeded to join the club {club_name}.")
        return redirect(url_for('profile_clubs', user_name = user_name))
    except Exception as ex:
        log(f"{LOG_ERROR} User {user_name} failed to join the club: {ex}")
        return redirect(url_for('club_note', club = club, note = "Fail to join with unknown reason."))

@app.route('/profile/<user_name>/clubs')
def profile_clubs(user_name):
    user_clubs = dbm.query_user_clubs(user_name)
    return render_template('profile-clubs.html', school=school, user=user_name, clubs = user_clubs)

@app.route('/events')
def events():
    global user
    events = dbm.query_all_events()
    return render_template("events.html", school=school, user = user, events = events)

@app.route('/clubs/<club>/events')
def profile_club_events(club):
    global user
    events = dbm.query_events(club = club)
    return render_template("events.html", school=school, user = user, events = events)

@app.route('/clubs/<club>/events/eventid=<eventid>')
def event(club, eventid):
    global user
    event_info = dbm.query_event(eventid = eventid)
    club_name = event_info["clubname"]
    log(f"{LOG_INFO} Query event profile {event_info}.")
    return render_template('event.html', school=school, user=user, club = club, club_name = club_name, eventid = eventid, info = event_info)

@app.route('/clubs/<club>/events/eventid=<eventid>/note=<note>')
def event_note(club, eventid, note):
    global user
    event_info = dbm.query_event(eventid = eventid)
    club_name = event_info["clubname"]
    log(f"{LOG_INFO} Query event profile {event_info}.")
    return render_template('event.html', school=school, user=user, club = club, club_name = club_name, eventid = eventid, info = event_info, note = note)

@app.route('/clubs/<club>/events/eventid=<eventid>/joinevent/user=<user_name>')
def event_join(club, eventid, user_name):
    # Make Sure User Login
    try:
        global userid
        user_info = dbm.query_user(userid)
        print(f"{LOG_INFO} Get user information {user_info}.")
        if user_info is None:
            log(f"{LOG_WARNING} User {user_name} not exist or just visitor.")
            return redirect(url_for('login_note', note = f"User {user_name} not exist or just visitor."))
        events = dbm.query_user_events(user_name)
        for e in events:
            if e["eventid"] == eventid:
                log(f"{LOG_WARNING} User {user_name} already joined the event with eventid = {eventid}.")
                return redirect(url_for('event_note', club = club, eventid = eventid, note = "You already joined the event."))
        event_info = dbm.query_event(eventid)
        assert(event_info)
        num_students = event_info["num_students"] if event_info["num_students"] else 0
        if num_students < event_info["lim_students"]:
            assert(dbm.join_event(user_name, eventid, user_info, event_info))
            log(f"{LOG_INFO} User {user_name} succeeded to join the event with eventid = {eventid}.")
            return redirect(url_for('profile_events', user_name = user_name))
        else :
            log(f"{LOG_WARNING} User {user_name} failed to join the event with eventid = {eventid} since there's no quota left.")
            return redirect(url_for('event_note', club = club, eventid = eventid, note = "Fail to join. There's no quota left."))
    except Exception as ex:
        log(f"{LOG_ERROR} User {user_name} failed to join the event with eventid = {eventid}: {ex}")
        return redirect(url_for('event_note', club = club, eventid = eventid, note = "Fail to join with unknown reason."))

@app.route('/profile/<user_name>/events')
def profile_events(user_name):
    try:
        user_events = dbm.query_user_events(user_name)
        log(f"{LOG_INFO} User {user_name} succeeded to query events: {user_events}")
        assert(user_events != -1)
        return render_template('profile-events.html', school=school, user=user_name, events = user_events)
    except Exception as ex:
        log(f"{LOG_ERROR} User {user_name} failed to query events: {ex}")
        return redirect(url_for('profile_note', user_name = user_name, note = f"User {user_name} failed to query events: {ex}"))

'''
@app.route('/clubs/<club>/events')
def profile_club_events(club):
    global user
    club_info = dbm.query_club(club = club)
    log(f"{LOG_INFO} Query club profile {club_info}.")
    club_name = club_info["clubname"]
    club_desc = club_info["club_desc"]
    club_desc = club_desc if club_desc is not None and len(club_desc) > 4 else "Temporarily Empty ~"
    events = dbm.query_events(club = club)
    log(f"{LOG_INFO} Query all events of the club: {events}.")
    return render_template('club-events.html', school=school, user = user, club=club, club_name = club_name, club_desc = club_desc, events=events)
'''

#@app.route('/clubs/<club>/students')
#def query_club_students(club):
#    return redirect(url_for('club_profile_display', club = club))

@app.route('/clubs/profile/<club>/students')
def club_profile_students(club):
    try:
        club_info = dbm.query_club(club = club)
        clubname = club_info["clubname"]
        log(f"{LOG_INFO} Query club profile {club_info}.")
        student_info = dbm.query_club_students(club)
        assert(student_info != -1)
        query1, query2 = student_info
        print(student_info)
        log(f"{LOG_INFO} Query club student profile {student_info}.")
        return render_template('club-admin/students.html', club=club, club_name=clubname, q1=query1, q2=query2)
    except Exception as ex:
        log(f"{LOG_ERROR} Query club student profile: {ex}.")
        return redirect(url_for('club_profile_note', club = club, note = f"Fail to query club student profile {ex}."))

if __name__ == '__main__':
    app.run(debug=True)
