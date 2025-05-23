from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # essiz id tanimi
    firstName = db.Column(db.String(100), nullable=False) #firstName=form ıcındekı degerı al ve gonder
    lastName = db.Column(db.String(100), nullable=False) #lastName=form ıcındekı degerı al ve gonder
    email = db.Column(db.String(100), unique=True, nullable=False) #email verısı
    role = db.Column(db.String(100), nullable=False, default="User") #role verısı
    phone = db.Column(db.String(15), nullable=False) #phone verısı
    password = db.Column(db.String(100), nullable=False) #password verısı
    confirmPassword = db.Column(db.String(100), nullable=True) #confirmPassword verısı
    
def db_to_json():
    with app.app_context():
        users = User.query.all()
        data = []
        for user in users:
            data.append ({
                'id': user.id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'role': user.role,
                'phone': user.phone,
                'password': user.password,
            })
                                   
        with open('users.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file,ensure_ascii=False, indent=7)
        
        print("Kullanıcı verileri JSON dosyasına aktarıldı.")
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    db_to_json()