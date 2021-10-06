from flask import Flask, render_template, url_for, request, redirect
from flask.globals import request
import sqlalchemy
import os
from werkzeug.utils import redirect


app = Flask(__name__)


def init_connection_engine():
    db_config = {
        # [START cloud_sql_postgres_sqlalchemy_limit]
        # Pool size é o numero máximo de conexões permanentes a serem mantidas.
        "pool_size": 5,
        # Temporariamente excede o pool_size se não hão conexões disponíveis.
        "max_overflow": 2,
        # O número total de conexões simultaneas será a soma do pool_size e max_overflow.
        # [END cloud_sql_postgres_sqlalchemy_limit]

        # [START cloud_sql_postgres_sqlalchemy_timeout]
        # 'pool_timeout' é o numero de segundos máximo para esperar quanto há a tentativa de nova conexão. 
        # Após esse tempo uma exception será lançada.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_postgres_sqlalchemy_timeout]

        # [START cloud_sql_postgres_sqlalchemy_lifetime]
        # 'pool_recycle' é o numero de segundos máximo que uma conexão pode ter.
        # Conexões que durarem mais que o valor específico serão reestabelecidas.
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_postgres_sqlalchemy_lifetime]
        "pool_pre_ping": True
    }
    return init_tcp_connection_engine(db_config)

def init_tcp_connection_engine(db_config):
    # [START cloud_sql_postgres_sqlalchemy_create_tcp]

    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]

    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 5432
            database=db_name  # e.g. "my-database-name"
        ),
        **db_config
    )
    # [END cloud_sql_postgres_sqlalchemy_create_tcp]
    pool.dialect.description_encoding = None
    return pool


db = None

@app.before_first_request
def create_tables():
    print('app aberto pela primeira vez')

    global db
    db = init_connection_engine()
    # Criar a tabela (Caso ela não exista)
    with db.connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS tarefas "
            "( id SERIAL NOT NULL, content VARCHAR(200) NOT NULL, "
            "date_created timestamp NOT NULL, PRIMARY KEY (id) );"
        )


@app.route("/", methods=['POST', 'GET'])
def index(): 
    if request.method == 'POST':
        conteudo = request.form['content'] # conteudo do input
        # [START cloud_sql_postgres_sqlalchemy_connection]
        try:
            with db.connect() as conn:
                conn.execute(
                    "INSERT INTO tarefas (content, date_created)"
                    f" VALUES ('{conteudo}', current_timestamp)"                    
                )
            return redirect('/')

        except:
            return "Houve um problema ao adicionar sua tarefa."
        # [END cloud_sql_postgres_sqlalchemy_connection]
    else:
        with db.connect() as conn:
            tarefas = conn.execute(
                "SELECT * FROM tarefas "
                "ORDER BY date_created"
            ).fetchall()
            
        return render_template('index.html', tasks=tarefas)


@app.route('/delete/<int:id>')
def delete(id):
    try:
        with db.connect() as conn:
            conn.execute(
                f"DELETE FROM tarefas WHERE id = {id};"               
            )
        return redirect('/')
    except:
        return 'Houve um problema ao deletar a tarefa'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    with db.connect() as conn:
        tarefas = conn.execute(
            f"SELECT * FROM tarefas WHERE id = {id};"
        ).fetchone()


    if request.method == 'POST':
        new_content = request.form['content']

        try:
            with db.connect() as conn:
                conn.execute(
                    f"UPDATE tarefas SET content = '{new_content}', date_created = current_timestamp WHERE id = {id};"           
                )
            return redirect('/')
        except:
            return 'Houve um problema ao atualizar a tarefa'
    else:          
        return render_template('update.html', task=tarefas)
        


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))