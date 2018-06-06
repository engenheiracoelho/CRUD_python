from flask import (
    flash, g, redirect, render_template, request, session, url_for, Flask

)

from mysql.connector import MySQLConnection, Error

SECRET_KEY = "aula de banco de dados"

app = Flask(__name__)  # criando estancia da classe flask

app.secret_key = SECRET_KEY

db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'aula',
    'raise_on_warnings': True,
}


@app.route('/')  #
def main():
    return render_template('index.html')


@app.route('/inserir', methods=('GET', 'POST'))
def inserir():
    if request.method == 'POST':
        Nome = request.form['Nome']
        Email = request.form['Email']

        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor()

        consulta = "INSERT INTO Contato (Nome,Email) VALUES (%s,%s)"
        dados = (Nome, Email)

        cursor.execute(consulta, dados)
        g.db.commit()
        cursor.close()
        g.db.close()

        return redirect(url_for('listar'))

    return render_template('inserir.html', title='Adicionar Contato')


@app.route('/listar')  #
def listar():
    resultado = []
    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    consulta = "SELECT * FROM Contato"

    cursor.execute(consulta)

    for (ID, Nome, Email) in cursor:
        resultado.append({'ID': ID, 'Nome': Nome, 'Email': Email})

    cursor.close()
    g.db.close()

    return render_template('listar.html', contatos=resultado)

@app.route('/editar')
def editar():
    if request.method == 'GET':
        ID = str(request.args.get('ID'))
        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor(prepared=True)
        consulta = ("SELECT * FROM Contato WHERE ID=%s")
        cursor.execute(consulta, (ID))
        linha = cursor.fetchone()

        contato = [
            {
                'ID' : linha[0],
                'Nome' : linha[1],
                'Email' : linha[2]
            }
        ]
        cursor.close()
        g.db.close()

        session['ID']=ID;
        return render_template('editar.html',title='Editar contato', contato=contato)
    else:
        ID=session['ID']
        Nome= request.form['Nome']
        Email= request.form['Email']
        session.pop('ID',None)

        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor(prepared=True)
        consulta = "UPDATE contato SET Nome= %s, Email= %s WHERE ID= %s"
        dados = (Nome, Email, str(ID))
        cursor.execute(consulta,dados)
        g.db.commit()
        cursor.close()
        g.db.close()
        return redirect(url_for('listar'))
if __name__ == '__main__':
    app.run()
