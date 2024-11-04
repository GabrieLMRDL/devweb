from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados usando pymysql
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:senhaexemplo@localhost:3306/desafio3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Contato(db.Model):
    __tablename__ = 'contato'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    mensagem = db.Column(db.Text, nullable=False)

# Rotas
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/contatos")
def listar_contatos():
    # Busca todos os registros da tabela 'contato'
    contatos = Contato.query.all()
    return render_template("lista_contatos.html", contatos=contatos)


@app.route("/about")
def about():
    return render_template("quem-somos.html")

# Rota para adicionar contato
@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        contato = Contato(
            nome_completo=request.form["nome_completo"],
            email=request.form["email"],
            telefone=request.form["telefone"],
            mensagem=request.form["mensagem"]
        )
        db.session.add(contato)
        db.session.commit()
        return redirect(url_for("contato"))
    return render_template("contato.html")

if __name__ == '__main__':
    # Criar as tabelas do banco de dados
    with app.app_context():
        db.create_all()
    app.run(debug=True)
