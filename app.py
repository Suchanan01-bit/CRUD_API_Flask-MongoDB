from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/mydatabase" # เชื่อมต่อกับ container mongo
mongo = PyMongo(app)

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    item_id = mongo.db.items.insert_one(data).inserted_id
    return jsonify({"_id": str(item_id)}), 201

@app.route('/items', methods=['GET'])
def get_items():
    items = list(mongo.db.items.find())
    for item in items:
        item["_id"] = str(item["_id"])
    return jsonify(items)

@app.route('/items/<id>', methods=['GET'])
def get_item(id):
    item = mongo.db.items.find_one({"_id": ObjectId(id)})
    if item:
        item["_id"] = str(item["_id"])
        return jsonify(item)
    return jsonify({"message": "Item not found"}), 404

@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    data = request.json
    result = mongo.db.items.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "Item updated successfully"})
    return jsonify({"message": "Item not found"}), 404

@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    result = mongo.db.items.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Item deleted successfully"})
    return jsonify({"message": "Item not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085, debug=True)