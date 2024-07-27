import smtplib
import email.message 

#função que envia senha para email fornecido
#retorna ou uma mensagem de erro ou uma mensagem de sucesso
def enviarEmail(to,senha):
    email_address = 'senac.recuperasenha@gmail.com'
    password = 'cvnnbgqrhokympnx'
    corpo_email = f"""
    <p>Seu email foi verificado e ele consta no banco de dados</p>
    <p>Sua senha é: {senha}</p>
    """
    msg = email.message.Message()
    msg['Subject'] = 'recuperação de senha'
    msg['From'] = email_address
    msg['To'] = to
    msg.add_header('Content-Type','text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(email_address,password)
    try:
        s.sendmail(msg['From'],msg['To'],msg.as_string().encode('utf-8'))
        return "Email enviado com sucesso. Cheque seu email"
    except:
        return "Email não pode ser enviado com sucesso"
    
def enviarEmailCadastro(to,matricula,nome,senha,cpf,curso):
    email_address = 'senac.recuperasenha@gmail.com'
    password = 'cvnnbgqrhokympnx'
    corpo_email = f"""
    <p>Seu cadastro foi realizado com sucesso!!!</p>
    <p>Sua matricula é: {matricula}</p>
    <p>Seu nome é: {nome}</p>
    <p>Sua senha é: {senha}</p>
    <p>Seu email é: {to}</p>
    <p>Seu cpf é: {cpf}</p>
    <p>Seu curso é: {curso}</p>
    """
    msg = email.message.Message()
    msg['Subject'] = 'recuperação de senha'
    msg['From'] = email_address
    msg['To'] = to
    msg.add_header('Content-Type','text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(email_address,password)
    try:
        s.sendmail(msg['From'],msg['To'],msg.as_string().encode('utf-8'))
        return "Email enviado com sucesso. Cheque seu email"
    except:
        return "Email não pode ser enviado com sucesso"
