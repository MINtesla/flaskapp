from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
port = int(os.environ.get('PORT', 5000))
import pymysql

app = Flask(__name__, template_folder="templates")

conn = "mysql+pymysql://root:PASSWORD@127.0.0.1:3306/FlaskProject"
# cloud string

app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

engine = create_engine(conn)
connection = engine.raw_connection()
cursor = connection.cursor()

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
    qno = 0
    whole_quiz = []
    questions = []
    questions = engine.execute("select * from que").fetchall()
    # print(questions);
    # myFile=open("questions.txt" , "r")
    # ques = myFile.read().splitlines()
    # myFile.close()

    # for element in ques:
    #     print(element)
    # print(len(questions))
    for element in questions:
        qno += 1
        # print(element[0])
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

    qno = 0
    return render_template("quiz.html", array=whole_quiz)

@app.route("/")
def ba():
    return render_template("index.html")

@app.route("/<name>")
def bas(name):
    return render_template("index.html")



@app.route("/{}")
def basic():
    return render_template("index.html")

@app.route("/index")
def home():
    global email
    global password

    if email == "admin@host.local" and password == "12789":
        return render_template("admin.html")
    elif verify(email, password):
        emailsave.emailid = email
        return render_template("user.html", var=authentic)
    return render_template("index.html")


# return render_template("showProd.html" , list= objects_list)


class regi(db.Model):  # regi table
    email = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=False)
    password = db.Column(db.String(20), nullable=False, unique=False)
    marks = db.Column(db.String(20), nullable=False)
    attempt = db.Column(db.String(20), nullable=False)

    def __int__(self, email, name, password, marks, attempt):
        self.email = email
        self.name = name
        self.password = password
        self.marks = marks
        self.attempt = attempt


@app.route("/onsignup", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        # 'add entry to DB'
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        entry = regi(email=email, name=name, password=password, marks=0, attempt=0)
        db.session.add(entry)
        db.session.commit()
        # complete = str(name) + "," + str(email) + "," + str(password) + "," + "0" + "," + "0" + "," + "0"
        # myFile=open("dataCSV.txt" , "a")
        # print(complete , file= myFile , sep="\n")
        # myFile.close()

    return render_template("index.html")

    # global email
    # global password
    # global name
    #
    # name=request.form.get('name')
    # email=request.form.get('email')


#  # password=request.form.get('password')
# complete= str(name)+ "," +str(email)+ "," +str(password)+ "," +"0"+","+"0"+","+"0"


# ashu : i have to put database here
# myFile=open("dataCSV.txt" , "a")
# print(complete , file= myFile , sep="\n")
# myFile.close()
# try:
#     db.execute('INSERT INTO ashu (name,username, password) VALUES (?, ?)', (self.username, self.password))
# except:
#     db.execute('CREATE TABLE users (id INTEGER PRIMARY KEY , username TEXT, password TEXT)')
#     raise UserNotFoundError('The table `users` did not exist, but it was created. Run the registration again.')
# finally:
#     connection.commit()
#     connection.close()

@app.route("/onlogin", methods=["POST", "GET"])
def userVerify():
    global email
    global password
    global wholeCredentials
    global authentic
    email = request.form.get('email')
    password = request.form.get('password')

    # myFile=open("dataCSV.txt" , "r")
    # wholeCredentials = myFile.read().splitlines()
    # myFile.close()

    if verify(email, password):
        # cursor =mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        emailsave.emailid = email
        return render_template("user.html", var=authentic)

    elif email == "admin@host.local" and password == "12789":
        return render_template("admin.html")
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

    # emailList = []
    # passwordList = []
    # global authentic
    #
    # wholeCredentials = []
    #
    # myFile=open("dataCSV.txt" , "r")
    # wholeCredentials = myFile.read().splitlines()
    # myFile.close()
    #
    # for idx in range(0, len(wholeCredentials)):
    #     emailList.append(getField( wholeCredentials[idx] , 1 ))
    #     passwordList.append(getField( wholeCredentials[idx] , 2 ))
    #
    # print(len(wholeCredentials))
    # print(len(emailList))
    # print(len(passwordList))
    #
    # for idx in range( 0 , len(emailList)):
    #     if email == emailList[idx] and pw == passwordList[idx]:
    #         authentic = getField( wholeCredentials[idx] , 0 )
    #         print(authentic)
    #         return True
    # return False


@app.route("/showall", methods=["POST", "GET"])
def showll():
    objects_list = []
    whole = []
    data = engine.execute("select name, email , marks from regi").fetchall()
    print(data)
    num = 0
    for element in data:
        print(element)
        obj = making_marks(element)
        objects_list.append(obj)

    return render_template("showall.html", list=objects_list)


class que(db.Model):
    Quid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Ques = db.Column(db.String(100), unique=False, nullable=False)
    Option1 = db.Column(db.String(100), unique=False, nullable=False)
    Option2 = db.Column(db.String(100), unique=False, nullable=False)
    Option3 = db.Column(db.String(100), unique=False, nullable=False)
    Option4 = db.Column(db.String(100), unique=False, nullable=False)
    CorrAns = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, Ques, Option1, Option2, Option3, Option4, CorrAns):
        self.Ques = Ques
        self.Option1 = Option1
        self.Option2 = Option2
        self.Option3 = Option3
        self.Option4 = Option4
        self.CorrAns = CorrAns


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
    question = que(Ques=ques, Option1=op1, Option2=op2, Option3=op3, Option4=op4, CorrAns=cor)
    db.session.add(question)
    db.session.commit()
    #
    # complete = ques + "," + op1 + "," + op2 + "," + op3 + "," + op4 + "," + cor
    # myFile = open("questions.txt", "a")
    # print(complete, file=myFile, sep="\n")
    # myFile.close()
    return render_template("admin.html")


@app.route("/submit", methods=["POST", "GET"])
def submit_quiz():
    global email
    wholeCredentials = []

    attempts = []
    score = 0
    whole_quiz = []
    number = 0
    questions = engine.execute("select * from que").fetchall()
    # print(questions);
    # myFile=open("questions.txt" , "r")
    # ques = myFile.read().splitlines()
    # myFile.close()

    # for element in ques:
    #     print(element)
    # print(len(questions))
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

    # myFile=open("questions.txt" , "r")
    # questions = myFile.read().splitlines()
    # myFile.close()
    # number=0
    # for element in questions:
    #     print(element)
    #     print(number)
    #     obj= making_objects(element , number)
    #     whole_quiz.append(obj)

    for idx in range(0, len(whole_quiz)):
        mcq = "mcq" + str(idx + 1)
        attempts.append(request.form.get(mcq))

    for udx in attempts:
        print(udx)

    for idx in range(0, len(whole_quiz)):
        if whole_quiz[idx].correct == attempts[idx]:
            score += 1

    # myFile=open("dataCSV.txt" , "r")
    # wholeCredentials = myFile.read().splitlines()
    # myFile.close()
    #
    # for idx in range(0,len(wholeCredentials)):
    #     if email==getField(wholeCredentials[idx],1):
    #         wholeCredentials[idx]= str(getField(wholeCredentials[idx],0))+ ","+str(getField(wholeCredentials[idx],1))+ "," +str(getField(wholeCredentials[idx],2))+ "," +str(score)+ "," +str(len(attempts))+ "," +str(len(whole_quiz))
    #
    # myFile=open("dataCSV.txt" , "w")
    # for record in wholeCredentials:
    #     print(record , file= myFile , sep="\n")
    #
    # myFile.close()
    data = engine.execute('select attempt from regi where email = %s', [emailsave.emailid]).fetchone()
    print(emailsave.emailid)
    print(data)
    engine.execute('Update regi set marks =%s where email =%s', [score, emailsave.emailid])
    engine.execute('Update regi set attempt =%s where email =%s', [data[0] + 1, emailsave.emailid])
    print("Your score is:", score)
    return render_template("user.html")


@app.route("/login", methods=["POST", "GET"])
def validation():
    return render_template("login.html")


@app.route("/show", methods=["POST", "GET"])
def results():
    # global email
    # wholeCredentials = []
    # attempts = 0
    # myFile=open("dataCSV.txt" , "r")
    # wholeCredentials = myFile.read().splitlines()
    # myFile.close()
    #
    # score = 0
    # print(email)
    # for result in wholeCredentials:
    #     check = getField(result, 1)
    #     if email == check:
    #         score = str(getField(result, 3))
    #         attempts = str(getField(result, 4))
    data = engine.execute('select marks,attempt from regi where email = %s', [emailsave.emailid]).fetchone()
    print(data)
    return render_template("result.html", var1=data[0], var2=data[1])


@app.route("/register", methods=["POST", "GET"])
def register():
    return render_template("register.html")


@app.route("/quizstrt", methods=["POST", "GET"])
def strt():
    return render_template("quizstrt.html")


@app.route("/contact", methods=["POST", "GET"])
def get_social():
    return render_template("contact.html")


@app.route("/add", methods=["POST", "GET"])
def add():
    return render_template("addques.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    global email
    global password
    email = ""
    password = ""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",  port=port)