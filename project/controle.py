import BD as bd
import recuperarSenha as rs
from datetime import date


#===================================#
# FUNÇÕES DE CADASTRO DE FREQUENCIA #
#===================================#

#chama função validaLogin() o banco de dados passando matricula e senha
#retorna result(que contem uma lista ou None) para a app.py
def validaLogin(matricula,senha):
    result = bd.validaLogin(matricula,senha)    
    return result

#função verifica se o login pode ser realizado novamente ou não
def valida_data(matricula):
    #chama função no banco de dados que retorna a data mais recente de login do aluno 
    #buscando pela matricula
    data_recente = bd.buscaDataRecente(matricula)
    valido = False
    #busca a data recente da lista retornada
    data = data_recente[0]
    #verifica atraves de date.time.today() a data atual
    data_atual = date.today()
    #verifica se a data esta vazia e retorna um valor True
    #assim se não houver um cadastro previo o aluno podera se cadastrar pela primeira vez
    if data == None:
        valido = True
        return valido
    #faz a subtração das duas datas e atribui a uma variavel
    comparacao = data_atual - data
    #faz a conversão do resultado para dias
    comparacao = comparacao.days
    #compara se o resultado é maior que um
    #se sim atribui True a valido
    if comparacao >= 1:
        valido = True   
    #retorna um valor True ou False dependendo do programa  
    return valido

#função retorna lista de frequencia do aluno
def cadastraFrequencia(matricula):
    #busca curso do aluno com a matricula passada
    curso = bd.buscaCurso(matricula)
    #cadastra a frequencia do aluno e busca todas as frequencias dele
    frequencia = bd.cadastraFrequencia(matricula,curso)
    return frequencia

#============================#
# FUNÇÕES DE RECUPERAR SENHA #
#============================#

#função verifica se o email consta no Banco de dados
def validaEmail(email):
    #chamada de função do banco de dados
    #retorno do resultado para app.py
    result = bd.validaEmail(email)
    return result

#função que verifica se o email está vazio ou passa de 50 carcteres
#retorna False ou True 
def validaDadoEmail(email):
    result = True
    if email == "" or len(email) > 50 or email == None:
        result = False
    return result

#chama a função enviarEmail() do arquivo recuperarSenha.py e retorna o resultado para app.py
def enviarEmail(email,senha):
    result = rs.enviarEmail(email,senha)
    return result

def enviarEmailCadastro(email,matricula,nome,senha,cpf,curso):
    result = rs.enviarEmailCadastro(email,matricula,nome,senha,cpf,curso)
    return result

#=====================#
# FUNÇÕES DE CADASTRO #
#=====================#

#valida dados usados para cadastrar alunos 
#retorna se são validos ou não
def validaDados(nome,email,senha,cpf,curso,telefone):
    valido = True
    if nome == "" or len(nome) > 50 or nome == None:
        valido = False
    elif email == "" or len(nome) > 50 or email == None:
        valido = False
    elif senha == "" or len(nome) > 50 or senha == None:
        valido = False
    elif cpf == "" or cpf == None:
        valido = False
    elif curso == "" or len(nome) > 50 or curso == None:
        valido = False
    elif telefone == "" or telefone == None:
        valido = False
    return valido

#verifica se os dados passados são validos atraves de uma função de controle
#se os dados forem validos ele cadastra o aluno e retorna uma lista
#se os dados forem invalidos ele retorna False
def cadastraAluno(nome,email,senha,cpf,curso,telefone):
    #chamada da função de controle que valida os dados
    valido = validaDados(nome,email,senha,cpf,curso,telefone)
    if valido:
        #Chama função de cadastro do banco de dados
        result = bd.cadastraAluno(nome,email,senha,cpf,curso,telefone)
        return result
    else:
        return valido

#chama função do banco de dados e retorna uma lista com os campos e um valor boolean
def validaCadastro(nome,email,telefone):
    valido,campos = bd.validaCadastro(nome,email,telefone)
    return valido,campos