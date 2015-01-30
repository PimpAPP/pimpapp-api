from models import Base, Catador
from flask_sqlalchemy import SQLAlchemy

from app import app
from databases import db


@app.route('/')
def root():
    catadores = db.session.query(Catador).all()
    return u"<br>".join([u"{0}".format(c.name) for c in catadores])

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
