from marshmallow import fields
from .. import ma

from ..models.post import Post
from ..models.user import User

class PostSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Post


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
