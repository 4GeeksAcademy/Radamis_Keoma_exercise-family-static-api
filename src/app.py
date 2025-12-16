"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

members = [
    {
        "id": 0,
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    },
    {
        "id": 1,
        "first_name": "Jane",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    },
    {
        "id": 2,
        "first_name": "Jimmy",
        "age": 5,
        "lucky_numbers": [1]
    }
]



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route("/members", methods=["GET"])
def get_members():
    return jsonify(members), 200

@app.route("/members/<int:id>", methods=["GET"])
def get_single_member(id):
    for member in members:
        if member["id"] == id:
            return jsonify(member), 200

    return jsonify({"error": "Member not found"}), 404


@app.route("/members", methods=["POST"])
def add_member():
    body = request.json

    new_member = {
        "id": len(members),
        "first_name": body["first_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"]
    }

    members.append(new_member)
    return jsonify(new_member), 200

@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    for index, member in enumerate(members):
        if member["id"] == id:
            members.pop(index)
            return jsonify({"done": True}), 200

    return jsonify({"done": False}), 404

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
