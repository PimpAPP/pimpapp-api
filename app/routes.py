from flask import Response
from flask_sqlalchemy import SQLAlchemy

from app import app
from databases import db
from models import Base, Catador


@app.route('/')
def index():
    catadores = db.session.query(Catador).all()
    return u"<br>".join([u"{0}".format(c.name) for c in catadores])


@app.route('/catador/<int:id>')
def get_catador(id):
    catador = db.session.query(Catador).get(id)
    response = Response(catador.to_JSON(),
            status=200, mimetype="application/json")
    return response

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
