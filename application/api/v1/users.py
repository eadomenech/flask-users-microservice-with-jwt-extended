from flask import Blueprint, request, jsonify
from apifairy import response, body, other_responses
from sqlalchemy import exc

from application import db
from application.api.schemes import (
    UserSchema, ResponseUserSchema,
    ResponseListUsersSchema, LoginSchema, ResponseLoginSchema)
from application.api.models import User


api = Blueprint('users', __name__)


@api.route('/user/<user_id>', methods=['GET'])
@response(ResponseUserSchema)
@other_responses({400: 'Invalid request.', 404: 'User not fount'})
def get_user(user_id):
    """
    Get user

    This endpoint get single user details.
    """
    response_object = {
        'status': 'fail',
        'msg': 'User does not exist',
        'data': {},
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return response_object, 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'password': user.password,
                    'active': user.active
                }
            }
            return response_object, 200
    except ValueError:
        return response_object, 404


@api.route('/users', methods=['GET'])
@response(ResponseListUsersSchema)
def get_all_users():
    """
    Get all users

    This endpoint get all users.
    """
    response_object = {
        'status': 'success',
        'msg': '',
        'data': [user.to_json() for user in User.query.all()]
    }
    # return response_object, 200
    return response_object, 200
