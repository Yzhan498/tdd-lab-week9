# src/api/users.py 
from flask import Blueprint, request 
from flask_restx import Resource, Api, fields
from src import db 
from src.api.models import User
users_blueprint = Blueprint('users', __name__) 
api = Api(users_blueprint)
user = api.model('User', { 
    'id': fields.Integer(readOnly=True), 
    'username': fields.String(required=True), 
    'email': fields.String(required=True), 
    'created_date': fields.DateTime, 
})
class Users(Resource): 
    @api.marshal_with(user) 
    def get(self, user_id): 
        user = User.query.filter_by(id=user_id).first() 
        if not user: 
            api.abort(404, f"User {user_id} does not exist") 
        return user, 200
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            api.abort(404, f"User {user_id} does not exist")

        db.session.delete(user)
        db.session.commit()
        return {"message": f"User {user_id} has been deleted"}, 200
api.add_resource(Users, '/users/<int:user_id>')

class UsersList(Resource): 
    @api.marshal_with(user, as_list=True) 
    def get(self): 
        return User.query.all(), 200
    @api.expect(user, validate=True)
    def post(self): 
        post_data = request.get_json() 
        username = post_data.get('username') 
        email = post_data.get('email') 
        response_object = {}
        user = User.query.filter_by(email=email).first() 
        if user: 
            response_object['message'] = 'Sorry. That email already exists.' 
            return response_object, 400
        db.session.add(User(username=username, email=email)) 
        db.session.commit() 
        response_object = { 'message': f'{email} was added!' } 
        return response_object, 201 
api.add_resource(UsersList, '/users')

class UpdateUsers(Resource): 
    @api.marshal_with(user) 
    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            post_data = request.get_json()
            new_username = post_data.get('username')
            new_email = post_data.get('email')

            # Check if both username and email are provided in the request
            if new_username is None or new_email is None:
                return {'message': 'Both username and email must be provided'}, 400

            # Update user information
            user.username = new_username
            user.email = new_email
            db.session.commit()
            return user, 200
        else:
            api.abort(404, f"User {user_id} does not exist")




