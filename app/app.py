from flask import Flask
from models import Base, Catador
from flask_sqlalchemy import SQLAlchemy

app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

@app.before_first_request
def setup():
    # Recreate database each time for demo
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    #db.session.add(Catador('Dunha'))
    db.session.commit()

@app.route('/')
def root():
    catadores = db.session.query(Catador).all()
    return u"<br>".join([u"{0}".format(c.name) for c in catadores])

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)

