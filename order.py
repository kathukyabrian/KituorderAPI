from config import app, db
from flask import jsonify, redirect, url_for, request
from models import Bug
from schemas import BugSchema

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/',methods=['GET','POST'])
def bug():
    bugs = Bug.query.all()
    bugs_schema = BugSchema(many=True)
    if request.method == 'POST':
        data = request.get_json()
        subject = data['subject']
        body = data['body']
        bug = Bug(subject=subject,body=body)
        db.session.add(bug)
        db.session.commit()
        return jsonify({"success":"bug successfully posted"})
    return jsonify(bugs_schema.dump(bugs))
    

if __name__ == '__main__':
    app.run(debug=True)