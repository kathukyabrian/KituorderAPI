from config import app, db
from flask import jsonify, redirect, url_for, request
from models import Bug, Region, User
from schemas import BugSchema, RegionSchema, UserSchema
from datetime import datetime

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

@app.route('/users',methods=["GET","POST"])
def users():
    public_users_schema = UserSchema(many=True,only=('id','firstname','lastname'))
    users_schema = UserSchema(many=True)
    users = User.query.all()
    user_schema = UserSchema(only=('id','firstname','lastname'))
    if request.method == "GET":
        return jsonify(public_users_schema.dump(users))    
    elif request.method == "POST":
        data = request.get_json()
        email = data['email']
        phone = data['phone']
        firstname = data['firstname']
        lastname = data['lastname']
        region = data['region']
        password = data['password']
        user = User(email=email,phone=phone,firstname=firstname,lastname=lastname,region=region,
        date_joined=datetime.now())
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify(user_schema.dump(User.query.filter_by(id=user.id).first()))
 
if __name__ == '__main__':
    app.run(debug=True)