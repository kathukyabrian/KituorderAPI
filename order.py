from config import app, db
from flask import jsonify, redirect, url_for, request
from models import Bug, Region
from schemas import BugSchema, RegionSchema

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/region',methods=['GET','POST'])
def regions():
    regions_schema = RegionSchema(many=True)
    regions = Region.query.all()
    if request.method == "POST":
        data = request.get_json()
        region_name = data['region_name'].capitalize()
        region = Region(name=region_name)
        db.session.add(region)
        db.session.commit()
        return jsonify({'success':'region addition was successful'})
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
            return jsonify({'success':'region details successfully updated'})
        else:
            return jsonify({'error' : 'a region with the specified id was not found'}),404
 
if __name__ == '__main__':
    app.run(debug=True)