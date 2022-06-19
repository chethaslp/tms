from operator import attrgetter
from jsonic import serialize, deserialize
from flask import Flask, redirect, render_template, send_from_directory, request, session
from flask_session import Session
import pymongo
from func import *
import uuid
from model import Subject


client = pymongo.MongoClient("mongodb+srv://db:db@cluster.ntzhw.mongodb.net/?retryWrites=true&w=majority")

app = Flask(__name__ )
app.debug = True
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "mongodb"
app.config["SESSION_MONGODB"] = client
app.config["SESSION_MONGODB_DB"] = 'tms'
app.config["SESSION_MONGODB_COLLECT"] = 'sessions'
Session(app)

@app.route("/css/<path:path>")
def css(path):
    return send_from_directory('css',path)

@app.route("/timetable")
def timetable_main():
    return redirect(f"/timetable/{str(uuid.uuid4())[:4]}")

@app.route("/timetable/<key>")
def timetable(key): 
    genKey(key)
    try: t_sub = deserialize(session['t_sub'])
    except: return redirect("/sub_select")
    
    try: pref = session['pref']
    except: return redirect("/pref")

    try: clss = deserialize(session['cls'])
    except: return redirect("/cls_select")

    return render_template("timetable.html" , clsr=gen_tt(pref,clss,t_sub)[0], key= key)

@app.route("/timetable_faculty/<key>")
def timetable_faculty(key): 
    genKey(key)
    try: t_sub = deserialize(session['t_sub'])
    except: return redirect("/sub_select")
    
    try: pref = session['pref']
    except: return redirect("/pref")

    try: clss = deserialize(session['cls'])
    except: return redirect("/cls_select")

    return render_template("timetable_faculty.html" , sbs=gen_tt(pref,clss,t_sub)[1], key= key)


@app.route("/cls_select",methods=['GET','POST'])
def cls_select():
    try: pref = session['pref']
    except: return redirect("/pref")

    try: t_sub = deserialize(session['t_sub'])
    except: return redirect("/sub_select")

    if request.form.get("a") == "ad":
        if request.form.get("cls_sub") != "0":
            cls_sub = [c for c in t_sub if str(c.sub_code) == str(request.form.get("cls_sub"))][0]
        else:
            cls_sub = None
        c = Classroom(request.form.get("cls_name"),request.form.get("cls_code"),primary_sub=cls_sub)
        a = deserialize(session['cls'])
        a.append(c)
        session['cls'] = serialize(a)
    elif request.form.get("a") == "rm":
        a = deserialize(session['cls'])
        a = [x for x in a if x.cls_code != request.form.get("cls_code")]
        session['cls'] = serialize(a)
    # elif request.form.get("a") == "ed":
    #     a = deserialize(session['cls'])
    #     for c in a:
    #         if c.sub_code == int(request.form.get("sub_code")):
    #             c.sub_priority = int(request.form.get("sub_priority"))
    #             c.is_practical = bool(request.form.get("sub_prac") == "on")
    #             break
    #     session['t_sub'] = serialize(a)

    try: clss = deserialize(session['cls'])
    except: 
        clss = generateClass(pref)
        session['cls'] = serialize(clss)
    return render_template("cls_select.html",clss=clss,t_sub=t_sub)

@app.route("/sub_select", methods=['GET','POST'])
def root2():
    try: pref = session['pref']
    except: return redirect("/pref")

    if request.method == "POST":
        if request.form.get("a") == "as":
            c = Subject(str(request.form.get("sub_code")), request.values.get("sub_title"), int(request.values.get("sub_priority")), is_practical = bool(request.form.get("sub_prac") == "on"))
            a = deserialize(session['t_sub'])
            a.append(c)
            session['t_sub'] = serialize(a)
        elif request.form.get("a") == "rm":
            a = deserialize(session['t_sub'])
            a = [x for x in a if x.sub_code != str(request.form.get("sub_code"))]
            session['t_sub'] = serialize(a)
        elif request.form.get("a") == "ed":
            a = deserialize(session['t_sub'])
            for c in a:
                if c.sub_code == str(request.form.get("sub_code")):
                    c.sub_priority = int(request.form.get("sub_priority"))
                    c.is_practical = bool(request.form.get("sub_prac") == "on")
                    break
            session['t_sub'] = serialize(a)

    try:
        t_sub = deserialize(session['t_sub'])
    except:
        t_sub=[ Subject(12,"Maths",8),
            Subject(13,"English",6),
            Subject(14,"Computer",8),
            Subject(15,"Physics",8),
            Subject(16,"Chemistry",8),
            Subject(17,"PET",6),
            Subject(65,"Chemistry Lab",2,is_practical=True),
            Subject(67,"Physics Lab",2,is_practical=True) ]
        session['t_sub'] = serialize(t_sub)
    t_sub.sort(key=attrgetter("sub_priority"),reverse=True)
    return render_template("sub_select.html",t_sub = t_sub,pref = pref)

@app.route('/about')
def aboutPage():
    return render_template("about.html")

@app.route('/pref', methods=['GET','POST'])
def prefPage():
    show_success = False
    try: pref = session['pref']
    except:
        pref = {'t_day': 6,'t_period_pd': 8}
        session['pref'] = pref
    if request.method == "POST":
        pref = {'t_day': request.form.get("pref_t_days",type=int) ,'t_period_pd': request.form.get("pref_period_pd", type=int)}
        session['pref'] = pref
        show_success = True
    return render_template("pref.html", pref=pref,show_success=show_success)

@app.route('/')
def rootPage():
    return render_template("index.html")
import os
if os.environ.get('PORT'):
    app.run(port=os.environ['PORT'],host='0.0.0.0')
else:
    app.run()