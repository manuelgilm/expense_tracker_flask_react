from flask import Blueprint, request, jsonify

test = Blueprint(name="test", import_name = __name__)

@test.get("/")
def test_function():
    return jsonify({"msg":"Endpoint working!"})

@test.post("/")
def test_function_post():
    data = request.json
    return {"msg":"ok"}