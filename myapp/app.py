from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Chave secreta para criptografar os dados da sessão

def get_db_connection():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='bdanunsee'
    )
    return conexao

# Página de Login (rota principal)
@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = None  # Inicializa a variável error_message
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificação de nome de usuário e senha fixos
        if username == 'admin' and password == '1234':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error_message = "Login falhou. Verifique seu nome de usuário e senha."

    return render_template('login.html', error_message=error_message)

# Página Principal Protegida
@app.route('/index', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    vendas = None
    if request.method == 'POST':
        action = request.form['action']
        
        if action == 'Registrar Venda':
            nome_produto = request.form['nome_produto']
            valor = request.form['valor']
            
            conexao = get_db_connection()
            cursor = conexao.cursor()
            comando = 'INSERT INTO vendas(nome_produto, valor) VALUES (%s, %s)'
            cursor.execute(comando, (nome_produto, valor))
            conexao.commit()
            cursor.close()
            conexao.close()

        elif action == 'Mostrar Vendas':
            conexao = get_db_connection()
            cursor = conexao.cursor()
            cursor.execute('SELECT nome_produto, valor FROM vendas')
            vendas = cursor.fetchall()
            cursor.close()
            conexao.close()

        elif action == 'Sair':
            session.pop('logged_in', None)
            return redirect(url_for('login'))

    return render_template('index.html', vendas=vendas)

if __name__ == '__main__':
    app.run(debug=True)
