from flask import render_template, redirect, url_for, flash, session, request
from app.jogos import bp
from app.extensions import db
from app.models.jogo import Jogo
from app.models.usuario import Usuario

LOGADO = 'usuario_logado'

@bp.route('/')
def index():
    lista = Jogo.query.order_by(Jogo.id)
    return render_template('jogos/lista.html', titulo='Jogos', jogos=lista)

@bp.route('/novo')
def novo():
    is_not_user_logged = LOGADO not in session or session[LOGADO] is None
    if is_not_user_logged:
        return redirect(url_for('jogos.login', proxima='jogos.novo'))
    return render_template('jogos/novo.html', titulo='Novo Jogo')


@bp.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existente!', 'danger')
        return redirect(url_for('jogos.index'))

    novo_jogo = Jogo(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    # Para não ficar na página '/criar'
    return redirect(url_for('jogos.index'))

@bp.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('jogos.login', proxima=url_for('jogos.editar', id=id)))
    jogo = Jogo.query.filter_by(id=id).first()
    return render_template('jogos/editar.html', titulo='Editando Jogo', jogo=jogo)

@bp.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogo.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()
    
    flash('Jogo atualizado com sucesso!', 'success')

    return redirect(url_for('jogos.index'))

@bp.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Jogo.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso!', 'success')

    return redirect(url_for('jogos.index'))

@bp.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('jogos/login.html', proxima=proxima)


@bp.route('/logout')
def logout():
    session[LOGADO] = None
    flash('Logout efetuado com sucesso', 'success')
    return redirect(url_for('jogos.login'))


@bp.route('/autenticar', methods=['POST'])
def autenticar():
    autenticado = False
    nickname = request.form['usuario']
    senha = request.form['senha']
    print(f'usuario: {nickname}')
    usuario = Usuario.query.filter_by(nickname=nickname).first()
    if usuario:
        if usuario.senha == senha:
            autenticado = True
            session[LOGADO] = usuario.nickname
            flash('Usuário {} logado com sucesso!'.format(usuario.nome), 'success')
            proxima_pagina = request.form['proxima']
            print(proxima_pagina)
            return redirect(proxima_pagina)
    if not autenticado:
        flash('Não foi possível logar com o usuário {}'.format(nickname), 'danger')
        return redirect(url_for('jogos.login'))
