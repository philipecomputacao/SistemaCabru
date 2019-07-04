from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Aluno
from dao import AlunoDao, UsuarioDao
import time
from helpers import deleta_arquivo, recupera_imagem
from cabrueira import db, app

aluno_dao = AlunoDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    lista = aluno_dao.listar()
    return render_template('lista.html', titulo='Alunos', alunos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Aluno')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    sexo = request.form['sexo']
    telefone = request.form['telefone']
    email = request.form['email']
    data_nascimento = request.form['data_nascimento']
    data_matricula = request.form['data_matricula']
    turma_fk = request.form['turma_fk']
    desconto = request.form['desconto']
    aluno = Aluno(nome, sexo, telefone, email, data_nascimento, data_matricula, turma_fk, desconto)
    aluno = aluno_dao.salvar(aluno)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{aluno.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    aluno = aluno_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Aluno', aluno=aluno
                           , capa_aluno=nome_imagem or 'capa_padrao.jpg')


@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    sexo = request.form['sexo']
    telefone = request.form['telefone']
    email = request.form['email']
    data_nascimento = request.form['data_nascimento']
    data_matricula = request.form['data_matricula']
    turma_fk = request.form['turma_fk']
    desconto = request.form['desconto']
    aluno = Aluno(nome, sexo, telefone, email, data_nascimento, data_matricula, turma_fk, desconto, id=request.form['id'])

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(aluno.id)
    arquivo.save(f'{upload_path}/capa{aluno.id}-{timestamp}.jpg')
    aluno_dao.salvar(aluno)
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    aluno_dao.deletar(id)
    flash('O aluno foi removido com sucesso!')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente denovo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
