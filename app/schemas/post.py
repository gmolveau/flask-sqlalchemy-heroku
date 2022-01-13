from marshmallow import fields, EXCLUDE
from ..marshmallow import ma

from ..models.post import Post
from ..models.user import User

class PostSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Post
        unknown = EXCLUDE


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
