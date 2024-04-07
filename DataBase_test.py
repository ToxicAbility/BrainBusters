from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
DB_USERNAME = "DESKTOP-1HCAB3I"
DB_DATABASE = "BrainBuster"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://{DB_USERNAME}/{DB_DATABASE}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

# Test the connection
try:
    db.create_all()
    print("Connection to the database established successfully!")
except Exception as e:
    print(f"Failed to connect to the database: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)