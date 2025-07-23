from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for users
# Format: {user_id: {"name": ..., "email": ...}}
users = {}
next_id = 1  # Auto-incrementing user ID

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# POST - Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()
    
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and Email required"}), 400

    users[next_id] = {
        "name": data["name"],
        "email": data["email"]
    }
    response = {"id": next_id, "user": users[next_id]}
    next_id += 1
    return jsonify(response), 201

# PUT - Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    users[user_id].update({
        "name": data.get("name", users[user_id]["name"]),
        "email": data.get("email", users[user_id]["email"])
    })
    return jsonify(users[user_id]), 200

# DELETE - Remove a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]
    return jsonify({"message": f"User {user_id} deleted"}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
