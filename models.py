from config import db

class Bug(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    subject = db.Column(db.String,nullable=False)
    body = db.Column(db.String,nullable=False)

    def __repr__(self):
        return "<Bug {}>".format(self.subject)