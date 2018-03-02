from flask import Blueprint

api = Blueprint('api_v1', __name__, template_folder='app/templates')

# Import any endpoints here to make them available
from . import hello
from . import user
from . import webhook
