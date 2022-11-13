from flask import Flask, render_template, request,session,redirect,url_for
from model import  db,engine,regi,que,app
from werkzeug.security import generate_password_hash, check_password_hash
import os
port = int(os.environ.get('PORT', 4000))

q = 0
qq = 0


class emailsave:
    emailid = "__@GMAIL.COM"


emailList = []
passwordList = []
wholeCredentials = []
email = ""
password = ""
name = ""
authentic = ""


class Question:
    question = ""
    option1 = ""
    option2 = ""
    option3 = ""
    option4 = ""
    correct = ""
    qnum = ""


class Score:
    name = ""
    email = ""
    score = ""

def current_user():
    user=None
    user=session['name']
    return user

# function to spearate username and password
def getField(line, field):  # separating username and password field

    storedField = ""
    c = ''
    idx = 0
    commaFound = 0
    # storing the particular field in "storedField"
    # after certain existing commas
    while (commaFound < field + 1 and idx < len(line)):

        c = line[idx]

        if c == ',':
            commaFound += 1
        elif commaFound == field:
            storedField = storedField + c
        idx += 1
    return storedField


def making_objects(listElement, number):
    p = Question()
    p.question = getField(listElement, 0)
    p.option1 = getField(listElement, 1)
    p.option2 = getField(listElement, 2)
    p.option3 = getField(listElement, 3)
    p.option4 = getField(listElement, 4)
    p.correct = getField(listElement, 5)
    p.qnum = number

    return p


def making_marks(listElement):
    s = Score()
    print(listElement[0])
    print(listElement[1])
    print(listElement[2])
    s.name = str(listElement[0])
    s.email = str(listElement[1])
    s.score = str(listElement[2])
    return s


@app.route("/quiz", methods=["POST", "GET"])
def quiz():
    try:
        if(session['name']):
            questions = engine.execute("select * from que").fetchall()
            str = ""
            whole_quiz=[]
            qno = 0
            for element in questions:
                qno += 1
                str = element[1]
                str += ","
                str += element[2]
                str += ","
                str += element[3]
                str += ","
                str += element[4]
                str += ","
                str += element[5]
                str += ","
                if element[6] == 1:
                    str += element[2]
                elif element[6] == 2:
                    str += element[3]
                elif element[6] == 3:
                    str += element[4]
                else:
                    str += element[5]

                print(str)
                obj = making_objects(str, qno)
                whole_quiz.append(obj)

                return render_template("quiz.html",user=session['name'], array=whole_quiz)
    except:
        return render_template("login.html")
@app.route("/")
def ba():
    try:
        if current_user() == "admin":
            return render_template("admin.html", user=current_user())
        elif current_user():
            return render_template("user.html", user=current_user())
        else:
            return render_template("login.html")
    except:
        return render_template("login.html")

@app.route("/<name>")
def bas(name):
    return render_template("index.html")



@app.route("/{}")
def basic():
    return render_template("index.html")

@app.route("/index")
def home():
    try:
        if current_user() == "admin":
            return render_template("admin.html", user=current_user())
        elif current_user():
            return render_template("user.html", user=current_user())
        else:
            return render_template("login.html")
    except:
        return render_template("index.html")


# class regi(db.Model):  # regi table
#     EMAIL = db.Column(db.String(50), primary_key=True)
#     NAME = db.Column(db.String(20), nullable=False, unique=False)
#     PASSWORD = db.Column(db.String(20), nullable=False, unique=False)
#     MARKS = db.Column(db.String(20), nullable=False)
#     ATTEMPT = db.Column(db.String(20), nullable=False)
#
#     def __int__(self, EMAIL, NAME , PASSWORD, MARKS, ATTEMPT):
#         self.EMAIL = EMAIL
#         self.NAME= NAME
#         self.PASSWORD = PASSWORD
#         self.MARKS = MARKS
#         self.ATTEMPT = ATTEMPT


@app.route("/onsignup", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        n = request.form.get('name')
        name = n.strip()
        e = request.form.get('email')
        email= e.strip()
        p = request.form.get('password')
        password = p.strip()
        entry = regi(EMAIL=email, NAME= name, PASSWORD=password, MARKS=0, ATTEMPT=0)
        db.session.add(entry)
        db.session.commit()

    return render_template("index.html")

@app.route("/onlogin", methods=["POST", "GET"])
def userVerify():
    email = request.form.get('email')
    password = request.form.get('password')

    if verify(email, password):
        emailsave.emailid = email
        session['email'] = email
        name = engine.execute("select name from regi where email= %s",[email]).fetchone()
        print(name)
        session['name']= name[0].upper()
        return render_template("user.html", user = current_user())

    elif email == "admin@host.local" and password == "12789":
        e= "admin@host.local"
        session['email'] = e
        session['name']= "admin".upper()
        return render_template("admin.html" , user =current_user())
    return render_template("invalid.html")


def verify(email, pw):
    try:
        data = engine.execute("SELECT * FROM regi where email =%s and password = %s", [email, pw]).fetchone()
        print(data)
        if data:
            print("OK")
            return True;
    except:
        return False


@app.route("/showall", methods=["POST", "GET"])
def showll():
    try:
        if (session['name']):
            objects_list=[]
            data = engine.execute("select name, email , marks from regi").fetchall()
            for element in data:
                obj = making_marks(element)
                objects_list.append(obj)

            return render_template("showall.html", user=session['name'], list=objects_list)
    except:
        return render_template("login.html")



# class que(db.Model):
#     QUID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     QUES = db.Column(db.String(100), unique=False, nullable=False)
#     OPTION1 = db.Column(db.String(100), unique=False, nullable=False)
#     OPTION2 = db.Column(db.String(100), unique=False, nullable=False)
#     OPTION3 = db.Column(db.String(100), unique=False, nullable=False)
#     OPTION4 = db.Column(db.String(100), unique=False, nullable=False)
#     CORRANS = db.Column(db.Integer, unique=False, nullable=False)
#
#     def __init__(self, QUES, OPTION1, OPTION2, OPTION3, OPTION4, CORRANS):
#         self.QUES = QUES
#         self.OPTION1 = OPTION1
#         self.OPTION2 = OPTION2
#         self.OPTION3 = OPTION3
#         self.OPTION4 = OPTION4
#         self.CORRANS = CORRANS


@app.route("/addquestion", methods=["POST", "GET"])
def add_question():
    ques = request.form.get('question')
    op1 = request.form.get('op1')
    op2 = request.form.get('op2')
    op3 = request.form.get('op3')
    op4 = request.form.get('op4')
    cor = request.form.get('corop')
    complete = ques + "," + op1 + "," + op2 + "," + op3 + "," + op4 + "," + cor
    print(complete)
    question = que(QUES=ques, OPTION1=op1, OPTION2=op2, OPTION3=op3, OPTION4=op4, CORRANS=cor)
    db.session.add(question)
    db.session.commit()
    return render_template("admin.html")


@app.route("/submit", methods=["POST", "GET"])
def submit_quiz():
    try:
        if(session['name']):
            global email
            wholeCredentials = []

            attempts = []
            score = 0
            whole_quiz = []
            number = 0
            questions = engine.execute("select * from que").fetchall()

            for element in questions:
                # print(element[0])
                s = element[1]
                s += ","
                s += element[2]
                s += ","
                s += element[3]
                s += ","
                s += element[4]
                s += ","
                s += element[5]
                s += ","
                if element[6] == 1:
                    s += element[2]
                elif element[6] == 2:
                    s += element[3]
                elif element[6] == 3:
                    s += element[4]
                else:
                    s += element[5]

                print(s)
                obj = making_objects(s, number)
                whole_quiz.append(obj)

            for idx in range(0, len(whole_quiz)):
                mcq = "mcq" + str(idx + 1)
                attempts.append(request.form.get(mcq))

            for udx in attempts:
                print(udx)

            for idx in range(0, len(whole_quiz)):
                if whole_quiz[idx].correct == attempts[idx]:
                    score += 1

            data = engine.execute('select attempt from regi where email = %s', [emailsave.emailid]).fetchone()
            print(emailsave.emailid)
            print(data)
            engine.execute('Update regi set marks =%s where email =%s', [score, emailsave.emailid])
            engine.execute('Update regi set attempt =%s where email =%s', [data[0]+ 1, emailsave.emailid])
            print("Your score is:", score)
            return render_template("user.html",user=current_user())
    except:
        return render_template("login.html")
@app.route("/login", methods=["POST", "GET"])
def validation():
    return render_template("login.html")


@app.route("/show", methods=["POST", "GET"])
def results():
    try:
        if current_user():
            data = engine.execute('select marks,attempt from regi where email = %s', [session['email']]).fetchone()
            print(data)
            return render_template("result.html", user=current_user() ,var1=data[0], var2=data[1])
    except:
        return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    session.clear()
    return render_template("register.html")


@app.route("/quizstrt", methods=["POST", "GET"])
def strt():
    try:
        if current_user():
           return render_template("quizstrt.html", user=session['name'])
    except:
        return render_template("login.html")


@app.route("/contact", methods=["POST", "GET"])
def get_social():
    try:
        if current_user():
           return render_template("contact.html", user=session['name'])
    except:
        return render_template("contact.html")


@app.route("/delete/<int:queid>", methods=["POST", "GET"])
def delete(queid):
    engine.execute("delete from que where quid=%s",[queid])
    return redirect(url_for('editques'))
@app.route("/editsingle/<int:queid>", methods=["POST", "GET"])
def editsingle(queid):
    print(1)
    print(queid)
    questions = engine.execute('select * from que where quid=%s',(queid,))
    str = []
    print(questions)
    for element in questions:
        str.append(element[0])
        str.append(element[1])
        str.append(element[2])
        str.append(element[3])
        str.append(element[4])
        str.append(element[5])
        str.append(element[6])

    print(str)
    #     return
    return render_template("editsingle.html",user=current_user(),queid=str)

@app.route("/edit" , methods=["POST", "GET"])
def edit():
    if request.method== "POST":
        queid =request.form['queid']
        question=request.form['question']
        op1 = request.form['op1']
        op2 = request.form['op2']
        op3 = request.form['op3']
        op4 = request.form['op4']
        correct= request.form['correct']

        engine.execute("update que set ques=%s, option1= %s , option2= %s, option3= %s, option4=%s, CORRANS=%s where quid=%s" ,[question,op1,op2,op3,op4,correct,queid]);
    return redirect(url_for('editques'))
@app.route("/add", methods=["POST", "GET"])
def add():
    try:
        if current_user():
            return render_template("addques.html", user=current_user())
    except:
        return render_template("login.html")



@app.route("/editques", methods=["POST", "GET"])
def editques():
        if current_user():
            questions = engine.execute("select * from que").fetchall()
            whole_quiz = []
            qno = 0
            print(questions)
            for element in questions:
                qno += 1
                str=[]
                str.append(element[0])
                str.append(element[1])
                str.append(element[2])
                str.append(element[3])
                str.append(element[4])
                str.append(element[5])
                str.append(element[6])

                print(str)
                obj = [str, qno]
                whole_quiz.append(obj)
            return render_template("editques.html", user=current_user(),que=whole_quiz)
    # except:
    #     return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",  port=port)