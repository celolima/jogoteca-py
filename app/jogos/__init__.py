from flask import Blueprint

bp = Blueprint('jogos', __name__)


from app.jogos import routes