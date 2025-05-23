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
    
    urunler = db.relationship('Product', back_populates='user') #ürünler ile kullanıcı arasında ilişki tanımı
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # essiz id tanimi
    barkod = db.Column(db.String(100),unique=True ,nullable=False)  # barkod numarasi
    name = db.Column(db.String(100), nullable=False)  # urun adi
    category = db.Column(db.String(50), nullable=False)  # urun kategorisi
    fiyat = db.Column(db.Float, nullable=False)  # urun fiyatı
    marka = db.Column(db.String(50), nullable=False)  # urun markasi
    adet = db.Column(db.Integer, nullable=False)  # urun adedi    
    kapasite = db.Column(db.Integer, nullable=False,default=100)  # urun kapasitesi
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    user= db.relationship('User', back_populates='urunler')  
    
    
def to_json():
    with app.app_context():
        users = User.query.all()
        data=[]
       
        for user in users:
            user_data = {
                'id': user.id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'role': user.role,
                'phone': user.phone,
                'password': user.password,
                'products': []
            }
            for product in user.urunler:
                product_data = {
                    'id': product.id,
                    'barkod': product.barkod,
                    'name': product.name,
                    'category': product.category,
                    'fiyat': product.fiyat,
                    'marka': product.marka,
                    'adet': product.adet,
                    'kapasite': product.kapasite
                }
                user_data['products'].append(product_data)
            data.append(user_data)
            
        with open('kullanici_urunler.json', 'w',encoding='utf-8') as file:
            json.dump(data, file,ensure_ascii=False, indent=8)
            
        print("JSON dosyası oluşturuldu.")
        
        
if __name__ == "__main__":
    to_json()