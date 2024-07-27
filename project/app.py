from flask import Flask, render_template, request, url_for, redirect
import controle as c

app = Flask(__name__)

#aqui ficam todas as rotas de acesso a diferentes paginas HTML

#rota para a pagina inicial ao abrir a aplicação
@app.route('/' , methods=['GET','POST'])
def formulario():
    return render_template('pagina_inicial.html')

#rota para tela de registro de frequencia
@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('index2.html',error="")

#rota para a pagina inicial acessada por link 
@app.route('/pagina_inicial', methods=['GET','POST'])
def pagina_inicial():
    return render_template('pagina_inicial.html')

#rota para a pagina de recuperamento de senha
@app.route('/esqueceu_senha', methods=['GET','POST'])
def esqueceu_senha():
    return render_template('esqueceu_senha.html')

#rota para tela de cadastro
@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    return render_template('cadastro.html')

#Funções principais do codigo acessada atraves de rotas

#Rota para a função de recuperar senha
@app.route('/valida_email', methods=['GET','POST'])
def valida_email():
    #busca email da pagina html com um request
    email = request.form['email']
    #chamada de função do controle para verificar o email fornecido
    #result armazena o resultado da função sendo False ou True
    result = c.validaDadoEmail(email)
    #se verdadeiro prossegue-se com o codigo senão retorna-se um erro para a pagina HTML
    if result:
        #chamada de função para validar se o email fornecido existe no banco de dados
        #rst armazena o resultado retornado do controle
        rst = c.validaEmail(email)
        #se o resultado não estiver vazio prossegue senão retorna-se um erro para a pagina HTML
        if rst != None:
            #armazenamento de variaveis que serão usadas na chamada da função enviarEmail()
            email = rst[0]
            senha = rst[1]
            #envia um email para o email fornecido com a senha que foi registrada
            #result retorna se o email foi enviado com sucesso ou não para a pagina HTML
            result = c.enviarEmail(email,senha)
            alert='True'
            return render_template('esqueceu_senha.html',result=result,alert=alert)
        else:
            #retorno de string como mensagem de erro para a pagina HTML
            error = 'o email digitado não consta no banco de dados'
            alert='False'
            return render_template('esqueceu_senha.html',result=error,alert=alert)
    else:
        #retorno de string como mensagem de erro para a pagina HTML
        error = 'o email digitado ou está vazio ou passa de 50 caracteres'
        alert='False'
        return render_template('esqueceu_senha.html',result=error,alert=alert)

#rota para função de cadastro de alunos
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    #busca valores da pagina HTML com request e armazena-os em variaveis
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    cpf = request.form['cpf']
    curso = request.form['curso']
    telefone = request.form['telefone']
    #chama uma função de controle onde os dados nome,email e telefone são verificados se foram cadastrados ou não
    #result recebe um valor boolean que verifica se os dados foram cadastrados ou não
    #campos recebe os valores que já foram cadastrados caso haja algum
    result,campos = c.validaCadastro(nome,email,telefone)
    #se result for True os dados são validos e prossegue senão retorna um erro a pagina HTML
    if result:
        #testa se há algum campo vazio ou que passsa de 50 carcteres se não a propria função cadastra o aluno
        #result recebe uma lista ou uma variavel boolean False
        result = c.cadastraAluno(nome,email,senha,cpf,curso,telefone)
        if result:
            #pega os elementos da lista e atribui a variaveis que são retornadas para pagina HTML
            matricula = result[0]
            nome = result[1]
            senha = result[3]
            email = result[2]
            cpf = result[4]
            curso = result[5]
            telefone = result[6]
            print(result)
            result = c.enviarEmailCadastro(email,matricula,nome,senha,cpf,curso)
            alert='True'
            return render_template('resultCadastro.html',
                                nome = nome,
                                matricula = matricula,
                                email = email,
                                cpf = cpf,
                                curso = curso,
                                telefone = telefone,
                                result = result,
                                alert = alert)
        else:
            #retorno de string como mensagem de erro para a pagina HTML
            error = "Não foi possivel cadastrar verifique se algum campo está vazio ou se os carcteres passam de 50"
            alert='False'
            return render_template('cadastro.html',result = error,alert=alert)
    else:
        #retorno de string como mensagem de erro para a pagina HTML
        #formação de string com mensagem de erro pegando da lista campos retornada
        error = "os seguintes campos já foram registrados: "
        for i in campos:
            error += i + ','
        error_cy = error
        error = ""
        for i in range(len(error_cy) - 1):
            error += error_cy[i]
        error += ". Troque eles para poder se registrar"
        alert='False'
        return render_template('cadastro.html',result = error,alert=alert)
    
#rota para a função cadastro de frequencia
@app.route('/frequencia', methods=['POST'])
def frequencia():
    #busca valores da pagina HTML e os atribui a variaveis
    matricula = request.form['matricula']
    senha = request.form['senha']
    #chama a função validalogin do controle passando matricula e senha
    result = c.validaLogin(matricula,senha)
    #se result que recebe a lista não estiver vazio o programa prossegue
    #senão é retornada uma mensagem a pagina HTML
    if result != None:
        #é chamdaa uma função de controle que recebe a matricula e busca a data mais recente de login desse aluno
        #checando se ele pode ou não fazer login novamente verificando se ele ja fez login neste dia
        #retorna True ou False
        rst = c.valida_data(matricula)
        #se o valor retornado for True prossegue senão retorna uma mensagem a pagina HTML
        if rst:
            #pega o nome do aluno da lista recebida em c.validaLogin()
            nome = result[1]
            #chama função cadastraFrequencia() passando matricula informada
            #retornando a lista de frequencias do aluno
            frequencias = c.cadastraFrequencia(matricula)
            #passa para a pagina HTML nome e a lista de frequencias
            result = 'Frequencia registrada com sucesso!'
            alert = 'True'
            return render_template('frequencia.html', nome=nome, frequencias=frequencias,result=result,alert=alert)
        else:
            #retorno de string como mensagem de erro para a pagina HTML
            error = "Você já logou em menos de 24H"
            alert='False'
            return render_template('index2.html',result=error,alert=alert)
    else:
        #retorno de string como mensagem de erro para a pagina HTML
        error = "Matrícula e/ou senha incorretas"
        alert='False'
        return render_template('index2.html', result=error,alert=alert)
    
if __name__ == '__main__':
    app.run(debug=True)