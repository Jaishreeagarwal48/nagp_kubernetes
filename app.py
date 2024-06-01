from flask import Flask
from flask import jsonify,make_response,request
from models import app, Employee, db_obj
from marshmallow import Schema,fields

class EmployeeSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    salary = fields.Integer()
    department = fields.String()

single_employee = EmployeeSchema()
multi_employee = EmployeeSchema(many=True)

@app.route("/employee",methods=["GET"])
def get_employee_details():
    try:
        query = Employee.query.all()
        data = multi_employee.dump(query)
        if len(data)>0:
            return make_response(jsonify({"message":"Employee List","Data":data}),200)
        return make_response(jsonify({"message": "No data found"}), 204)
    except Exception as e:
        print("exception:",str(e))
        return make_response(jsonify({"message":"error occured while getting data "+str(e)}),500)


@app.route("/add",methods=["POST"])
def add_employee():
    try:
        if request.get_json():
            data=request.get_json()
        elif request.form:
            data=request.form
        elif request.args:
            data=request.args
        else:
            return make_response(jsonify({"message": "data is missing"}), 400)
        invalidate_employee=single_employee.validate(data)
        print(invalidate_employee)
        if invalidate_employee:
            return make_response(jsonify({"message":invalidate_employee}),400)
        emp=Employee()
        emp.name=data["name"]
        emp.email=data["email"]
        emp.salary=data["salary"] if "salary" in data else None
        emp.department=data["department"] if "department" in data else None
        db_obj.session.add(emp)
        db_obj.session.commit()
        return make_response(jsonify({"message":"employee added successfully"}),200)
    except Exception as e:
        print("exception:",str(e))
        return make_response(jsonify({"message":"error occured while adding employee data "+str(e)}),500)

@app.route("/",methods=["GET"])
def get_details():
    try:
        return make_response(jsonify({"message": "service is running"}), 200)
    except Exception as e:
        print("exception:",str(e))
        return make_response(jsonify({"message":"error occured while running service "+str(e)}),500)


if __name__ == "__main__":
    with app.app_context():
        db_obj.create_all()
    app.run(debug=True,port=2000,host='0.0.0.0')
