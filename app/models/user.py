from ..database import db

# many to many entre 2 models différents
upvote_post =   db.Table('upvote_post',
                    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)

# many to many entre meme model
follow = db.Table('follow',
            db.Column('user1_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
            db.Column('user2_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

# relationship docs = http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)

    # one to many -> se retrouve grâce à la clef etrangère dans le model Post
    posts = db.relationship("Post", backref="user")

    # many to many models différents
    upvoted_posts = db.relationship("Post",
                        secondary=upvote_post,
                        backref=db.backref(
                            "upvoted_by",
                            lazy="dynamic"
                        )
                    )

    # many to many model avec lui meme
    following = db.relationship('User',
                    secondary=follow,
                    primaryjoin=(follow.c.user1_id == id),
                    secondaryjoin=(follow.c.user2_id == id),
                    backref=db.backref(
                        'followers',
                        lazy='dynamic'
                    ),
                    lazy='dynamic'
                )
