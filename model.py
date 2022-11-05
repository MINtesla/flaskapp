from __main__ import db


class regi(db.Model):  # regi table
    EMAIL = db.Column(db.String(50), primary_key=True)
    NAME = db.Column(db.String(20), nullable=False, unique=False)
    PASSWORD = db.Column(db.String(20), nullable=False, unique=False)
    MARKS = db.Column(db.String(20), nullable=False)
    ATTEMPT = db.Column(db.String(20), nullable=False)

    def __int__(self, EMAIL, NAME , PASSWORD, MARKS, ATTEMPT):
        self.EMAIL = EMAIL
        self.NAME= NAME
        self.PASSWORD = PASSWORD
        self.MARKS = MARKS
        self.ATTEMPT = ATTEMPT


class que(db.Model):
    QUID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    QUES = db.Column(db.String(100), unique=False, nullable=False)
    OPTION1 = db.Column(db.String(100), unique=False, nullable=False)
    OPTION2 = db.Column(db.String(100), unique=False, nullable=False)
    OPTION3 = db.Column(db.String(100), unique=False, nullable=False)
    OPTION4 = db.Column(db.String(100), unique=False, nullable=False)
    CORRANS = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, QUES, OPTION1, OPTION2, OPTION3, OPTION4, CORRANS):
        self.QUES = QUES
        self.OPTION1 = OPTION1
        self.OPTION2 = OPTION2
        self.OPTION3 = OPTION3
        self.OPTION4 = OPTION4
        self.CORRANS = CORRANS
