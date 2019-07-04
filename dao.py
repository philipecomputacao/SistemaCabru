from models import Aluno, Usuario

SQL_DELETA_ALUNO = 'delete from aluno where id = %s'
SQL_ALUNO_POR_ID = 'SELECT id, nome, sexo, telefone, email, data_nascimento, data_matricula, turma_fk, desconto from aluno where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_ALUNO = 'UPDATE aluno SET  nome = %s, sexo=%s, telefone=%s, email=%s, data_nascimento=%s, data_matricula=%s, turma_fk=%s, desconto= %s from aluno where id = %s'
SQL_BUSCA_ALUNO = 'SELECT id, nome, sexo, telefone, email, data_nascimento, data_matricula, turma_fk, desconto from aluno'
SQL_CRIA_ALUNO = 'INSERT into aluno (nome, sexo, telefone, email, data_nascimento, data_matricula, turma_fk, desconto ) values (%s, %s, %s, %s, %s, %s, %s, %s)'


class AlunoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, aluno):
        cursor = self.__db.connection.cursor()

        if (aluno.id):
            cursor.execute(SQL_ATUALIZA_ALUNO, (aluno.nome, aluno.sexo, aluno.telefone, aluno.email. aluno.data_nascimento, aluno.data_matricula, aluno.turma_fk, aluno.desconto, aluno.id))
        else:
            cursor.execute(SQL_CRIA_ALUNO, (aluno.nome, aluno.sexo, aluno.telefone, aluno.email. aluno.data_nascimento, aluno.data_matricula, aluno.turma_fk, aluno.desconto))
            aluno.id = cursor.lastrowid
        self.__db.connection.commit()
        return aluno

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_ALUNO)
        alunos = traduz_alunos(cursor.fetchall())
        return alunos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_ALUNO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Aluno ( tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_ALUNO, (id,))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_alunos(alunos):
    def cria_aluno_com_tupla(tupla):
        return Aluno(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], id=tupla[0])
    return list(map(cria_aluno_com_tupla, alunos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
