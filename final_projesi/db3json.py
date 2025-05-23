from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # essiz id tanimi
    barkod = db.Column(db.Integer, nullable=False)  # barkod numarasi
    name = db.Column(db.String(100), nullable=False)  # urun adi
    category = db.Column(db.String(50), nullable=False)  # urun kategorisi
    fiyat = db.Column(db.Float, nullable=False)  # urun fiyatı
    marka = db.Column(db.String(50), nullable=False)  # urun markasi
    adet = db.Column(db.Integer, nullable=False)  # urun adedi
    kapasite = db.Column(db.Integer, nullable=False)  # urun kapasitesi

def db_to_json_products():
    with app.app_context():
        products = Product.query.all()
        data = []
        for product in products:
            data.append({
                'id': product.id,
                'barkod': product.barkod,
                'name': product.name,
                'category': product.category,
                'fiyat': product.fiyat,
                'marka': product.marka,
                'Capacity': product.kapasite,
                'adet': product.adet
            })                        
        with open('products.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=8)
        print("Ürün verileri JSON dosyasına aktarıldı.")
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    db_to_json_products()