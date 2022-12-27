
from customers import customers
from books import books
from booktypes import booktypes
from loans import loans
from flask import Flask
from flask_cors import CORS
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sifria.sqlite3'
app.config['SECRET_KEY'] = "random string"

CORS(app)

db.init_app(app)
with app.app_context():
    db.create_all()
    
app.register_blueprint(books)
app.register_blueprint(customers)
app.register_blueprint(loans)
app.register_blueprint(booktypes)

@app.route("/")
def home():
    return "Welcome to Library"

##### Main page of Server  #####
if __name__ == '__main__':
    app.run(debug = True)

