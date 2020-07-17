from config import app, db
from flask import jsonify, redirect, url_for, request, render_template
from models import Bug, Region, User
from schemas import UserSchema
from datetime import datetime
from flask_cors import cross_origin
from utils import confirm_token, generate_confirmation_token, send_mail
from marshmallow import ValidationError

@app.before_first_request
def create_tables():
    db.create_all()  
    
@app.route('/register',methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def register():
    registered_user_schema = UserSchema(only=('id','email','phone'))
    if request.method == "POST":
        data = request.get_json()
        email = data['email']
        phone = data['phone']
        password = data['password']
        try:
            registered_user_schema.load(data,partial=True)
            user = User(email=email,phone=phone,date_joined=datetime.now())
            user.set_password(password)
            confirm_token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm_email',token=confirm_token,_external=True)
            html = render_template('activate.html',confirm_url=confirm_url)
            subject = "Email Confirmation"
            db.session.add(user)
            db.session.commit()
            send_mail(subject,user.email,html)
            return jsonify(registered_user_schema.dump(user))
        except ValidationError as error:
            return jsonify(error.messages)

@app.route('/register/<token>')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def confirm_email(token):
    try:
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            return jsonify({'user':'user is already confirmed, proceed to login'})
        else:
            user.confirmed = True
            user.confirmed_at = datetime.now()
            db.session.commit()
            return jsonify({'success':'user account was confirmed, proceed to login!'})
    except:
        return jsonify({'error':'The confirmation link is invalid or expired'})
    

@app.route('/login',methods=["POST"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                return jsonify({'token':auth_token.decode()})
            else:
                return jsonify({'error':'something went wrong, try again'})
        else:
            return jsonify({'error':'invalid credentials'})

@app.route('/users')
def public_users():
    users = User.query.all()
    registered_user_schema = UserSchema(only=('id','email'))
    if users:
        return jsonify(registered_user_schema.dump(users,many=True))

if __name__ == '__main__':
    app.run(debug=True)