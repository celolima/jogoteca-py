from flask import render_template
from app.jogos import bp
from app.extensions import db
from app.models.jogo import Jogo

@bp.route('/')
def index():
    lista = Jogo.query.order_by(Jogo.id)
    return render_template('jogos/lista.html', titulo='Jogos', jogos=lista)
