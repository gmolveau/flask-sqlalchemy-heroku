from flask import jsonify, request

from . import api
from .. import db, bcrypt

from ..models.post import Post
from ..schemas.post import post_schema, posts_schema
from ..models.user import User
from ..schemas.user import user_schema, users_schema

@api.route('/users/signup', methods=['POST'])
def signup_user():
    datas = request.get_json()
    username=datas.get('username','')
    if username is '':
        return jsonify(error="username is empty"),400
    email=datas.get('email','')
    if email is '':
        return jsonify(error="email is empty"),400
    password=datas.get('password','')
    if password is '':
        return jsonify(error="password is empty"),400

    u = User()
    u.username = username
    u.email = email
    u.password = bcrypt.generate_password_hash(password)

    db.session.add(u)
    db.session.commit()
    return user_schema.jsonify(u),200


@api.route('/users/login', methods=['POST'])
def login_username_or_email():
    datas = request.get_json()

    password=datas.get('password','')
    if password is '':
        return jsonify(error="password is empty"),400

    username=datas.get('username','')
    if username is '':
        return jsonify(error="username is empty"),400

    user = User.query.filter(User.username.ilike(username)).first()
    if user is not None:
        if bcrypt.check_password_hash(user.password, password):
            # pour les token, regarder du coté des JSON Web Token
            # librairie : itsdangerous
            return jsonify(token="token par exemple pour passer à l'API"),200
        return jsonify(error="username, mail or password is incorrect"),300

    email=datas.get('email','')
    if email is '':
        return jsonify(error="email is empty"),400

    user = User.query.filter(User.email.ilike(email)).first()
    if user is not None:
        if bcrypt.check_password_hash(user.password, password):
            return jsonify(token="token par exemple pour passer à l'API"),200
    return jsonify(error="username, mail or password is incorrect"),300


@api.route('/users/<string:username>', methods=['GET'])
def get_user(username):
    user = User.query.filter(User.username.ilike(username)).first()
    if user is not None:
        return user_schema.jsonify(user),200
    return jsonify(error="user not found"),404


@api.route('/users/<int:user_id>/posts', methods=['POST'])
def create_post(user_id):
    datas = request.get_json()

    url = datas.get('url', '')
    if url is '':
        return jsonify(error="url is empty"),400

    description = datas.get('description', '')
    if description is '':
        return jsonify(error="description is empty"),400

    post = Post()
    post.url = url
    post.description = description
    post.user_id = user_id

    db.session.add(post)
    db.session.commit()
    return post_schema.jsonify(post),200


@api.route('/users/<int:user_id>/upvotes/<int:post_id>', methods=['POST'])
def upvote_post(user_id, post_id):
    user = User.query.get(user_id)
    if user is not None:
        post = Post.query.get(post_id)
        if post is not None:
            user.upvoted_posts.append(post)
            db.session.commit()
            return jsonify(state="ok"),200
        return jsonify(error="post not found"),404
    return jsonify(error="user not found"),404


@api.route('/users/<int:user_id>/following/<int:follow_id>', methods=['POST'])
def follow_user(user_id, post_id):
    user = User.query.get(user_id)
    if user is not None:
        follow = User.query.get(user_id)
        if post is not None:
            user.upvoted_posts.append(post)
            db.session.commit()
            return jsonify(state="ok"),200
        return jsonify(error="post not found"),404
    return jsonify(error="user not found"),404


@api.route('/users/<int:user_id>/following/<int:follow_id>', methods=['DELETE'])
def unfollow_user(user_id, post_id):
    user = User.query.get(user_id)
    if user is not None:
        follow = User.query.get(user_id)
        if post is not None:
            user.upvoted_posts.remove(post)
            db.session.commit()
            return jsonify(state="ok"),200
        return jsonify(error="post not found"),404
    return jsonify(error="user not found"),404
