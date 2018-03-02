from marshmallow import fields
from .. import ma

from ..models.user import User

from ..models.post import Post
from ..schemas.post import post_schema, posts_schema

# nesting schema docs = https://marshmallow.readthedocs.io/en/latest/nesting.html

class UserSchema(ma.ModelSchema):

    id = fields.Int()
    username = fields.String()
    email = fields.String()
    upvoted_posts = fields.Nested(posts_schema, many=True)
    posts = fields.Nested(posts_schema, many=True)
    following = fields.Nested('self', only=('id','username'), many=True)
    followers = fields.Nested('self', only=('id','username'), many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
