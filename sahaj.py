from flask import Flask, request, jsonify
import redis
import json

app = Flask(_name_)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Endpoint to retrieve an employee by ID
@app.route('/employees/<employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee_data = redis_client.get(employee_id)
    if employee_data:
        return jsonify(json.loads(employee_data))
    else:
        return "Employee not found", 404

# Endpoint to create a new employee
@app.route('/employees', methods=['POST'])
def create_employee():
    try:
        data = request.get_json()
        employee_id = data.get('id')
        if not employee_id:
            return "Employee ID is required", 400

        # Check if the employee already exists
        if redis_client.get(employee_id):
            return "Employee already exists", 400

        redis_client.set(employee_id, json.dumps(data))
        return "Employee created", 201
    except Exception as e:
        return str(e), 500

# Endpoint to update an existing employee
@app.route('/employees/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        data = request.get_json()
        if redis_client.get(employee_id):
            redis_client.set(employee_id, json.dumps(data))
            return "Employee updated"
        else:
            return "Employee not found", 404
    except Exception as e:
        return str(e), 500

# Endpoint to delete an employee
@app.route('/employees/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    if redis_client.delete(employee_id):
        return "Employee deleted"
    else:
        return "Employee not found", 404

if _name_ == '_main_':
    app.run(debug=True)