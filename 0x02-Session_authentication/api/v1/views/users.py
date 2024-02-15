#!/usr/bin/env python3
"""Users views.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/
    JSON body:
      - email.
      - password.
      - last_name (optional).
      - first_name (optional).
    Return:
      - User object JSON rep.
      - 400 error creating new User.
    """
    req_j = None
    error_msg = None
    try:
        req_j = request.get_json()
    except Exception as e:
        req_j = None
    if req_j is None:
        error_msg = "Wrong format"
    if error_msg is None and req_j.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and req_j.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = req_j.get("email")
            user.password = req_j.get("password")
            user.first_name = req_j.get("first_name")
            user.last_name = req_j.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Return:
      - list of all User objects in JSON
    """
    users = [user.to_json() for user in User.all()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/:id
    Path parameter:
      - User_ID.
    Return:
      - User object JSON rep
      - 404 if User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        else:
            return jsonify(request.current_user.to_json())
    returned_user = User.get(user_id)
    if returned_user is None:
        abort(404)
    return jsonify(returned_user.to_json())


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id
    Path parameter:
      - User_ID.
    JSON body:
      - last_name (optional).
      - first_name (optional).
    Return:
      - User object JSON rep
      - 404 User ID doesn't exist.
      - 400 can't update the User.
    """
    if user_id is None:
        abort(404)
    returned_user = User.get(user_id)
    if returned_user is None:
        abort(404)
    req_j = None
    try:
        req_j = request.get_json()
    except Exception as e:
        req_j = None
    if req_j is None:
        return jsonify({'error': "Wrong format"}), 400
    if req_j.get('first_name') is not None:
        returned_user.first_name = req_j.get('first_name')
    if req_j.get('last_name') is not None:
        returned_user.last_name = req_j.get('last_name')
    returned_user.save()
    return jsonify(returned_user.to_json()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id
    Path parameter:
      - User_ID.
    Return:
      - empty JSON means User has been  deleted.
      - 404 User_ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200
