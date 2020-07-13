from config import app, db
from flask import jsonify, redirect, url_for, request, render_template
from models import Bug, Region, User
from schemas import BugSchema, RegionSchema, UserSchema
from datetime import datetime
from flask_cors import cross_origin
from utils import confirm_token, generate_confirmation_token, send_mail

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/region',methods=['GET','POST'])
def regions():
    regions_schema = RegionSchema(many=True)
    region_schema = RegionSchema()
    regions = Region.query.all()
    if request.method == "POST":
        data = request.get_json()
        region_name = data['region_name'].capitalize()
        region = Region(name=region_name)
        db.session.add(region)
        db.session.commit()
        return jsonify(region_schema.dump(region))
    return jsonify(regions_schema.dump(regions))

@app.route('/region/<int:id>',methods=['GET','PUT','DELETE'])
def regiondetail(id):
    region_schema = RegionSchema()
    region = Region.query.filter_by(id=id).first()

    if request.method == "GET":
        if region:
            return jsonify(region_schema.dump(region))
        else:
            return jsonify({'error' : 'a region with the specified id was not found'}),404
    elif request.method == "DELETE":
        if region:
            db.session.delete(region)
            db.session.commit()
            return jsonify({'success':'bug was successfully removed'})
        else:
            return jsonify({'error' : 'a region with the specified id was not found'}),404
    elif request.method == "PUT":
        if region:
            data = request.get_json()
            region_name = data['region_name'].capitalize()
            region.name = region_name
            db.session.commit()
            return jsonify(region_schema.dump(region))
        else:
            return jsonify({'error' : 'a region with the specified id was not found'}),404  
    
@app.route('/register',methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def register():
    registered_user_schema = UserSchema(only=('id','email'))
    if request.method == "POST":
        data = request.get_json()
        email = data['email']
        phone = data['phone']
        password = data['password']
        validate_email = User.query.filter_by(email=email).first()
        validate_phone = User.query.filter_by(phone=phone).first()
        if (validate_email or validate_phone):
            return jsonify({'error':'email or phone already taken'})
        else:
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


if __name__ == '__main__':
    app.run(debug=True)