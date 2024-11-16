from bson import ObjectId
import logging
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.environ.get('MONGO_URI'))
db = client.auth_db
users_collection = db.users

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

@app.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    profile = data.get('profile')

    if users_collection.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400

    users_collection.insert_one({"username": username, "profile": profile})
    return jsonify({"message": "User profile created successfully"}), 201

@app.route('/profile', methods=['GET'])
def get_profile():
    logged_in_username = request.headers.get('X-Logged-In-UserName')
    if not logged_in_username:
        logging.debug("X-Logged-In-User header is missing")
        return jsonify({"message": "X-Logged-In-User header is missing"}), 400

    logging.debug(f"Looking for user with ID: {logged_in_username}")
    user = users_collection.find_one({"username": logged_in_username}, {"_id": 0})
    logging.debug(f"User found : {str(user)}")

    # Log all users in the database for debugging
    all_users = list(users_collection.find())
    logging.debug(f"All users in the database: {all_users}")

    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/send-request/<r_username>', methods=['POST'])
def send_request(r_username):
    logged_in_username = request.headers.get('x-logged-in-username')
    if not logged_in_username:
        logging.debug("X-Logged-In-User header is missing")
        return jsonify({"error": "X-Logged-In-User header is missing"}), 400

    logging.debug(f"Logged in user ID: {logged_in_username}")
    logging.debug(f"Recipient user ID: {r_username}")

    try:
        update_result_1 = users_collection.update_one(
            {"username": logged_in_username},
            {"$addToSet": {"sent_requests": r_username}}
        )
        logging.debug(f"Update result for logged in user: {update_result_1.raw_result}")

        update_result_2 = users_collection.update_one(
            {"username": r_username},
            {"$addToSet": {"received_requests": logged_in_username}}
        )
        logging.debug(f"Update result for recipient user: {update_result_2.raw_result}")

        return jsonify({"message": "Request sent successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating user requests: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/accept-request/<r_username>', methods=['POST'])
def accept_request(r_username):
    logged_in_username = request.headers.get('x-logged-in-username')
    if not logged_in_username:
        return jsonify({"error": "X-Logged-In-UserName header is missing"}), 400

    users_collection.update_one(
        {"username": logged_in_username},
        {"$pull": {"received_requests": r_username}, "$addToSet": {"friends": r_username}}
    )
    users_collection.update_one(
        {"username": r_username},
        {"$pull": {"sent_requests": logged_in_username}, "$addToSet": {"friends": logged_in_username}}
    )

    return jsonify({"message": "Request accepted successfully"}), 200

@app.route('/withdraw-request/<r_username>', methods=['POST'])
def withdraw_request(r_username):
    logged_in_username = request.headers.get('x-logged-in-username')
    users_collection.update_one(
        {"username": logged_in_username},
        {"$pull": {"sent_requests": r_username}}
    )
    users_collection.update_one(
        {"username": r_username},
        {"$pull": {"received_requests": logged_in_username}}
    )
    return jsonify({"message": "Request withdrawn"}), 200

@app.route('/friends', methods=['GET'])
def get_friends():
    logged_in_username = request.headers.get('X-Logged-In-UserName')
    if not logged_in_username:
        return jsonify({"message": "X-Logged-In-User header is missing"}), 400

    user = users_collection.find_one({"username": logged_in_username}, {"_id": 0, "friends": 1})
    logging.debug(f"User found: {user}")
    if user:
        friends = user.get('friends', [])
        friends_data = list(users_collection.find({"username": {"$in": friends}}, {"_id": 0, "username": 1, "name": 1}))
        return jsonify(friends_data), 200
    else:
        return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)