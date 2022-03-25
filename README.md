## About The Project
Esta é uma api que se conecta a um banco de dados local postgresql para permitir que clientes possam criar usuário, fazer login, logout e criar itens.

Criação de usuário

A rota /signup espera receber um formulario com nome, email e senha. Com essas informações, a senha é criptografada usando bcrypt e um usuário é criado armazenando as informações de nome e email junto com um hash da senha no banco de dados postgresql.

Login

A rota /login espera receber um formulario contento email e senha. As informações passadas são conferidas com as informações no banco de dados e caso estejam corretas, uma server side session é criada e um id de sessão é enviado como resposta ao cliente para que este o armazene em forma de cookie. A partir de então, todas requesições vindas do cliente trarão um cookie de id de sessão, o que permitirá a API identificar que aquele cliente já foi authenticado e possui uma sessão ativa.

Logout

A rota de /logout permitirá que o cliente destrua a sessão que possui com a API, desse modo, ele se torna não authenticado.

Dash

A rota /dash traz todos os itens que o usuário criou e armazenou no banco de dados postgresql e permite a ele criar novos itens.


### Built With
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [Flask-Session](https://flask-session.readthedocs.io/en/latest/)
* [Postgresql](https://www.postgresql.org/docs/current/index.html)

## Getting Started
Para fazer o projeto rodar localmente na sua máquina siga os passos de instalação a seguir.

### Installation

1. Clone o repositório

2. Crie um ambiente virtual python com a versão 3.8 e o ative
   ```sh
   python3.8 -m venv env
   ```

   ```sh
   source env/bin/activate
   ```

3. Instale as depedências
    ```sh
   pip install -r requirements.txt
   ```

4. Configurando duas variáveis de ambiente.

Crie um arquivo .env dentro da pasta raiz do projeto e configure as seguintes variáveis. 
A primeira é chamada SQLALCHEMY_DATABASE_URI, ela identifica o banco de dados local postgresql no qual sua api se concetará. O formato dela é: dialect+driver://username:password@host:port/database e um exemplo poderia ser: postgresql://scott:tiger@localhost/mydatabase .

A segunda é chamada SECRET_KEY, ela server para assinar os cookies de sessão; qualquer string serve neste caso, mas pode-se gerar uma longa string randomica.


6. Torne o arquivo run executável
   ```sh
   chmod +x run
   ```

6. Inicie o servidor
   ```sh
   ./run
   ```

O servidor deverá estar rodando http://127.0.0.1:5000/

Pode-se agora fazer requesições http ao seu servidor
