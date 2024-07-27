import mysql.connector

#================================#
# CONFIGURAÇÃO DO BANCO DE DADOS #
#================================#

config = {
    'user': 'root',
    'password': '12345',
    'host': 'localhost',
    'database': 'registro_frequencia',
    'raise_on_warnings': True
}

#=====================================#
# INICIA CONEXÃO COM O BANCO DE DADOS #
#=====================================#

conn = mysql.connector.connect(**config)
cursor = conn.cursor(buffered=True)

#===================================#
# FUNÇÕES DE CADASTRO DE FREQUENCIA #
#===================================#

#busca dados da tabela alunos onde matricula e sennha são iguais as recebidas
#retorna uma lista com os resultados
def validaLogin(matricula,senha):
    cursor.execute("SELECT * FROM alunos WHERE matricula=%s AND senha=%s", (matricula, senha,))
    result = cursor.fetchone()
    return result

#busca a data mais recente do aluno pela matricula e retorna a data para o controle.py
def buscaDataRecente(matricula):
    cursor.execute("SELECT MAX(data) FROM frequencia WHERE matricula=%s",(matricula,))
    dataRecente = cursor.fetchone()
    return dataRecente

#cadastra a frequencia do aluno e retorna uma lista com as frequencias registradas dele
def cadastraFrequencia(matricula,curso):
    cursor.execute("INSERT INTO frequencia (matricula, data, hora, curso) VALUES (%s, CURDATE(), CURTIME(), %s)", (matricula, curso))
    conn.commit()
    cursor.execute("SELECT * FROM frequencia WHERE matricula=%s", (matricula,))
    frequencias = cursor.fetchall()
    return frequencias

#busca o curso do aluno na tabela alunos atraves da matricula dele
def buscaCurso(matricula):
    cursor.execute("SELECT curso FROM alunos WHERE matricula = %s",(matricula,))
    result = cursor.fetchone()
    result = result[0]
    return result

#============================#
# FUNÇÕES DE RECUPERAR SENHA #
#============================#

#busca email no banco de dados e retorna o resultado
def validaEmail(email):
    cursor.execute("SELECT email,senha FROM alunos WHERE email=%s",(email,))
    result = cursor.fetchone()
    return result

#=====================#
# FUNÇÕES DE CADASTRO #
#=====================#

#faz o cadastro do aluno e retorna uma lista com os dados cadastrados buscados do banco de dados
def cadastraAluno(nome,email,senha,cpf,curso,telefone):
    cursor.execute("INSERT INTO alunos (nome,senha,email,cpf,curso,telefone) VALUES (%s,%s,%s,%s,%s,%s)",(nome,senha,email,cpf,curso,telefone))
    conn.commit()
    cursor.execute("SELECT * FROM alunos WHERE cpf = %s",(cpf,))
    result = cursor.fetchone()
    return result

#função busca tudo da tabela alunos e verifica se algum é igual aos valores fornecidos
#retornando os campos onde os valores já existem se houver
#e retorna um valor boolean que confirma se há valores que já existem
def validaCadastro(nome,email,telefone):
    cursor.execute("SELECT * FROM alunos")
    result = cursor.fetchall()
    valido = True
    campos = []
    for i in result:
        nomeR = i[1]
        emailR = i[2]
        telefoneR = i[6]
        if(nomeR == nome):
            valido = False
            campos.append("nome")
        if(emailR == email):
            valido = False
            campos.append("email")
        if(telefoneR == telefone):
            valido = False
            campos.append("telefone")
    return valido,campos