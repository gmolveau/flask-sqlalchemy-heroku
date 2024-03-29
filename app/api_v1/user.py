from functools import wraps

from flask import jsonify, request, g
from flask_expects_json import expects_json
from marshmallow import ValidationError

from . import api
from ..database import db
from ..bcrypt import b_crypt

from ..models.post import Post
from ..schemas.post import PostSchema, post_schema, posts_schema
from ..models.user import User
from ..schemas.user import user_schema, users_schema

schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['username', 'email', 'password']
}

@api.post('/register')
@expects_json(schema) # example of a decorator to fail if the request is not JSON
def register():
    u = User()
    u.username = g.data.get('username')
    u.email = g.data.get('email')
    u.password = b_crypt.generate_password_hash(g.data.get('password'))
    db.session.add(u)
    db.session.commit()
    return user_schema.jsonify(u),200

@api.post('/login')
@expects_json() # example of a decorator to fail if the request is not JSON
def login_with_username_or_email():
    datas = request.get_json()

    password=datas.get('password','')
    if password == "":
        return jsonify(error="password is empty"),400

    username=datas.get('username','')
    if username == "":
        return jsonify(error="username is empty"),400

    user = User.query.filter(User.username.ilike(username)).first()
    if user is not None:
        if b_crypt.check_password_hash(user.password, password):
            # pour les token, regarder du coté des JSON Web Token
            # librairie : itsdangerous
            return jsonify(token="token par exemple pour passer à l'API"),200
        return jsonify(error="username, mail or password is incorrect"),300

    email=datas.get('email','')
    if email == "":
        return jsonify(error="email is empty"),400

    user = User.query.filter(User.email.ilike(email)).first()
    if user is not None:
        if b_crypt.check_password_hash(user.password, password):
            return jsonify(token="token par exemple pour passer à l'API"),200
    return jsonify(error="username, mail or password is incorrect"),300


@api.get('/users/<string:username>')
def get_user(username):
    user = User.query.filter(User.username.ilike(username)).first()
    if user is not None:
        return user_schema.jsonify(user),200
    return jsonify(error="user not found"),404

def required_params(schema):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                schema.load(request.get_json())
            except ValidationError as err:
                error = {
                    "status": "error",
                    "messages": err.messages
                }
                return jsonify(error), 400
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@api.post('/posts')
@required_params(post_schema)
def create_post():
    datas = request.get_json()
    post = Post()
    post.url = datas.get('url')
    post.description = datas.get('description')
    post.user_id = datas.get('user_id')

    db.session.add(post)
    db.session.commit()
    return post_schema.jsonify(post),200


@api.post('/posts/<int:post_id>/upvote')
def upvote_post(post_id):
    datas = request.get_json()
    user_id = datas.get('user_id', '')
    if user_id == "":
        return jsonify(error="user_id is empty"),400

    user = User.query.get(user_id)
    if user is not None:
        post = Post.query.get(post_id)
        if post is not None:
            user.upvoted_posts.append(post)
            db.session.commit()
            return jsonify(state="ok"),200
        return jsonify(error="post not found"),404
    return jsonify(error="user not found"),404


@api.post('/follow/<follow_id>')
def follow_user(follow_id):
    datas = request.get_json()
    user_id = datas.get('user_id', '')
    if user_id == "":
        return jsonify(error="user_id is empty"),400

    user = User.query.get(user_id)
    if user is not None:
        follow = User.query.get(follow_id)
        if follow is not None:
            user.following.append(follow_id)
            db.session.commit()
            return jsonify(state="ok"),200
        return jsonify(error="user to follow not found"),404
    return jsonify(error="user not found"),404


@api.delete('/follow/<int:follow_id>')
def unfollow_user(follow_id):
    datas = request.get_json()
    user_id = datas.get('user_id', '')
    if user_id == "":
        return jsonify(error="user_id is empty"),400

    user = User.query.get(user_id)
    if user is not None:
        follow = User.query.get(follow_id)
        if follow is not None:
            user.following.remove(follow_id)
            db.session.commit()
            return jsonify(state="ok"),200
        return jsonify(error="follow user not found"),404
    return jsonify(error="user not found"),404
