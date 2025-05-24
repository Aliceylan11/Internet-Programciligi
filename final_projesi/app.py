from flask import Flask,render_template, request, redirect, url_for, session, flash, jsonify,send_file,abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os,json,io
import pandas as pd
from fpdf import FPDF
app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = 'development_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # essiz id tanimi
    firstName = db.Column(db.String(100), nullable=False) #firstName=form ıcındekı degerı al ve gonder
    lastName = db.Column(db.String(100), nullable=False) #lastName=form ıcındekı degerı al ve gonder
    email = db.Column(db.String(100), unique=True, nullable=False) #email verısı
    role = db.Column(db.String(100), nullable=False, default="User") #role verısı
    phone = db.Column(db.String(15), nullable=False) #phone verısı
    password = db.Column(db.String(100), nullable=False) #password verısı
    confirmPassword = db.Column(db.String(100), nullable=True) #confirmPassword verısı
    
    urunler = db.relationship('Product', back_populates='user', cascade='all, delete-orphan') #ürünler ile kullanıcı arasında ilişki tanımı
    def set_password(self, password):
        self.password = generate_password_hash(password)
class Product(UserMixin,db.Model):
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
    


@login_manager.user_loader
def load_user(id): 
    return User.query.get(int(id))
   
@app.route("/")
def home():
    total_products = Product.query.count()
    toplam_stok = db.session.query(db.func.sum(Product.adet)).scalar()
    toplam_kapasite = db.session.query(db.func.sum(Product.kapasite)).scalar()
    if toplam_kapasite and toplam_kapasite > 0:
        doluluk_orani = (toplam_stok / toplam_kapasite) * 100
    else:
        doluluk_orani = 0
    return render_template("home.html", total_products=total_products, doluluk_orani=round(doluluk_orani, 2))

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and  check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('E-posta veya şifre hatalı!', 'danger')
    return render_template("login.html") 

@app.route('/register', methods=['GET', 'POST'])
def register():
 if request.method == 'POST':
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')
 # E-posta daha önce kullanılmış mı kontrolü
    if User.query.filter_by(email=email).first():
        flash('Bu e-posta zaten kayıtlı!', 'danger')
        return redirect(url_for('register')) 
    if password != confirmPassword:
            flash('Şifreler eşleşmiyor!', 'danger')
            return redirect(url_for('register'))
    # Şifreyi güvenli hâle getir (hashleme)
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    # Yeni kullanıcı oluştur
    new_user = User(firstName=firstName, lastName=lastName,email=email, role='User' , phone=phone, password=hashed_password, confirmPassword=confirmPassword)
    db.session.add(new_user)
    db.session.commit()
    
    flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
    return redirect(url_for('login'))
 return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Admin':
        return redirect(url_for('admin_dashboard'))
    products_page = request.args.get('products_page', 1, type=int)
    critical_page = request.args.get('critical_page', 1, type=int)
    per_page = 10
    products = Product.query.paginate(page=products_page, per_page=per_page, error_out=False)
    critical_products = Product.query.filter(Product.adet <= 10).paginate(page=critical_page, per_page=per_page, error_out=False)

    return render_template('dashboard.html', 
                           name=current_user.firstName, 
                           products=products, 
                           critical_products=critical_products)
    
    
    
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        abort(403)  # yetkisiz kullanıcı engellenir

    total_users = User.query.count()
    total_products = Product.query.count()
    return render_template("admin_dashboard.html", 
                           total_users=total_users, 
                           total_products=total_products)
    
        

@app.route('/logout')
@login_required
def logout():
 logout_user()
 return redirect(url_for('home'))

@app.route("/login/dashboard/critical_stock")
@login_required
def critical_stock():
    page = request.args.get('page', 1, type=int)  
    per_page = 10  
    critical_products = Product.query.filter(Product.adet <= 10).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("critical_stock.html", critical_products=critical_products)


@app.route("/login/dashboard/users")
@login_required
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/login/dashboard/users/update/<int:user_id>", methods=["GET", "POST"])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)  # Kullanıcıyı veritabanından al
    if current_user.id != user.id and current_user.role != 'Admin':
        flash('Sadece kendi bilgilerinizi güncelleyebilirsiniz.', 'danger')
        return redirect(url_for('users'))
    if request.method == "POST":
        user.firstName = request.form['firstName']
        user.lastName = request.form['lastName']
        user.email = request.form['email']
        user.phone = request.form['phone']
        #user.role = request.form['role']
        new_password = request.form['password']
        confirm_password = request.form['confirmPassword']
        if new_password or confirm_password:  # şifre değişikliği istenmişse
            if new_password != confirm_password:
                flash("Şifreler eşleşmiyor!", "danger")
                return redirect(url_for("update_user", user_id=user_id))
        user.set_password(new_password)
        db.session.commit()
        flash("Kullanıcı bilgileri başarıyla güncellendi.", "success")
        return redirect(url_for("users")) 
    return render_template("users_update.html", user=user)


@app.route("/login/dashboard/users/delete/<int:user_id>", methods=['POST'])
@login_required
def users_delete(user_id):
    user = User.query.get_or_404(user_id)  # Kullanıcıyı al, bulunamazsa 404 döner
    if current_user.id != user.id and current_user.role != 'Admin':
        flash('Sadece kendi bilgilerinizi silebilirsiniz.', 'danger')
        return redirect(url_for('users'))
    db.session.delete(user)
    db.session.commit()
    flash(f"{user.firstName} adlı kullanıcı başarıyla silindi.", "success")
    return redirect(url_for('users'))

@app.route("/login/dashboard/products")
@login_required
def products():
    page = request.args.get('page', 1, type=int)  
    per_page = 15 
    pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template("products.html", products=pagination.items, pagination=pagination)

@app.route("/login/dashboard/products/add", methods=['GET', 'POST'])
@login_required
def products_add():
    if request.method=='POST':
        barkod = request.form.get('barkod')
        name = request.form.get('name')
        category = request.form.get('category') 
        fiyat = request.form.get('fiyat')
        marka = request.form.get('marka')
        adet = request.form.get('adet')
        kapasite = request.form.get('kapasite')
        if Product.query.filter_by(barkod=barkod).first():
            flash('Bu barkod zaten kayıtlı!', 'danger')
            return redirect(url_for('products_add'))
        if current_user.is_authenticated:
            new_product = Product(
                barkod=barkod, 
                name=name, 
                category=category, 
                fiyat=fiyat,
                marka=marka, 
                adet=adet,
                kapasite=kapasite,
                user_id=current_user.id,
            )
            db.session.add(new_product) 
            db.session.commit()
            flash('Ürün başarıyla eklendi!', 'success')
            return redirect(url_for('products'))
        else:
            flash('Ürün eklenemedi!', 'danger')
            return redirect(url_for('products_add'))
    return render_template("products_add.html")

@app.route("/login/dashboard/products/update/<int:products>", methods=['GET', 'POST'])
@login_required
def products_update(products):
    urun = Product.query.get(products)
    if urun.user_id != current_user.id and current_user.role != 'Admin':
        flash('Bu ürünü güncelleme yetkiniz yok.', 'danger')
        return redirect(url_for('products'))
    if request.method == 'POST':
        urun.barkod = request.form['barkod']
        urun.name = request.form['name']
        urun.fiyat = request.form['fiyat']
        urun.marka = request.form['marka']
        urun.adet = request.form['adet']
        urun.kapasite = request.form['kapasite']
        
        db.session.commit()
        return redirect(url_for('products'))
    return render_template("products_update.html", urunler=urun)


@app.route("/login/dashboard/products/delete/<int:products>", methods=['GET', 'POST'])
@login_required
def products_delete(products):
    products = Product.query.get(products)
    if current_user.role != 'Admin' and products.user_id != current_user.id:
        flash("Bu ürünü silme yetkiniz yok!", "danger")
        return redirect(url_for("products"))
    if request.method == 'POST':
        db.session.delete(products)
        db.session.commit()
        flash(f"{products.name} adlı ürün başarıyla silindi.", "success")
        return redirect(url_for('products'))
    return render_template("products.html", products=products)


@app.route("/login/dashboard/products/filter", methods=["GET"])
@login_required
def filter_products():
    stock_status = request.args.get('stock_status', 'all')  
    category = request.args.get('category', 'all')  
    search_query = request.args.get('search_query', '').strip()
    page = request.args.get('page', 1, type=int)  # Sayfa numarasını al
    per_page = 15  # Sayfa başına ürün sayısı
    query = Product.query
    
    if stock_status == 'in_stock':
        query = query.filter(Product.adet > 0)
    elif stock_status == 'out_of_stock':
        query = query.filter(Product.adet == 0)
    
    if category != 'all':
        query = query.filter(Product.category == category)

    if search_query:
        query = query.filter(Product.name.ilike(f"%{search_query}%"))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "products.html", 
        products=pagination.items, 
        pagination=pagination, 
        stock_status=stock_status, 
        category=category, 
        search_query=search_query
    )
    
@app.route("/login/dashboard/reports")
@login_required
def reports():
    page = request.args.get('page', 1, type=int)  
    per_page = 7 
    pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items
    return render_template("reports.html", products=products, pagination=pagination)


@app.route("/download_excel")
@login_required
def download_excel():
    # Veritabanındaki ürünleri al
    products = Product.query.all()

    # Verileri bir DataFrame'e dönüştür
    data = []
    for product in products:
        data.append({
            "Barkod": product.barkod,
            "Adı": product.name,
            "Kategori": product.category,
            "Fiyat": product.fiyat,
            "Marka": product.marka,
            "Adet": product.adet,
            "Kapasite": product.kapasite
        })
    
    # Pandas DataFrame oluştur
    df = pd.DataFrame(data)

    # Excel dosyasını bellek üzerinde oluştur
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Ürünler")
    output.seek(0)

    # Dosyayı kullanıcıya gönder
    return send_file(output, as_attachment=True, download_name="urunler.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")



@app.route("/download_pdf")
@login_required
def download_pdf():
    products = Product.query.all()
    pdf = FPDF(orientation='L', unit='mm', format='A4')  # A4 yatay formatında oluştur
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Türkçe karakterler için uygun fontu yükleyin
    font_path = os.path.join('static', 'fonts', 'arial.ttf')  # Font dosyasının doğru yolu
    pdf.add_font('Arial', '', font_path, uni=True)
    pdf.set_font('Arial', '', 10)  # Daha küçük font boyutu

    # Başlık
    pdf.cell(275, 10, txt="Ürün Raporu", ln=True, align='C')  # Yatay genişliğe uygun başlık

    # Tablo Başlıkları
    column_widths = [40, 50, 50, 30, 30, 30, 30]  # Yatay genişlik için sütun boyutları
    pdf.ln(10)
    headers = ["Barkod", "Adı", "Kategori", "Fiyat", "Marka", "Adet", "Kapasite"]
    for i, header in enumerate(headers):
        pdf.cell(column_widths[i], 10, header, border=1, align='C')
    pdf.ln(10)

    # Tablo Verileri
    for product in products:
        if pdf.get_y() > 190:  # Sayfa sonuna yaklaştıysa yeni sayfa ekle
            pdf.add_page()
        pdf.cell(column_widths[0], 10, product.barkod, border=1, align='C')
        pdf.cell(column_widths[1], 10, product.name, border=1, align='C')
        pdf.cell(column_widths[2], 10, product.category, border=1, align='C')
        pdf.cell(column_widths[3], 10, str(product.fiyat), border=1, align='C')
        pdf.cell(column_widths[4], 10, product.marka, border=1, align='C')
        pdf.cell(column_widths[5], 10, str(product.adet), border=1, align='C')
        pdf.cell(column_widths[6], 10, str(product.kapasite), border=1, align='C')
        pdf.ln(10)

    output = io.BytesIO()
    pdf.output(dest='S').encode('latin1')
    output.write(pdf.output(dest='S').encode('latin1'))
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="urunler_yatay_format.pdf",
        mimetype="application/pdf"
    )

@app.route("/download_csv")
@login_required
def download_csv():
    # Veritabanındaki ürünleri al
    products = Product.query.all()

    # Verileri bir listeye dönüştür
    data = []
    for product in products:
        data.append({
            "Barkod": product.barkod,
            "Adı": product.name,
            "Kategori": product.category,
            "Fiyat": product.fiyat,
            "Marka": product.marka,
            "Adet": product.adet,
            "Kapasite": product.kapasite
        })
    
    # Pandas DataFrame oluştur
    df = pd.DataFrame(data)

    # CSV dosyasını bellek üzerinde oluştur
    output = io.StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')  # Türkçe karakterler için 'utf-8-sig'
    output.seek(0)

    # CSV dosyasını kullanıcıya gönder
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        as_attachment=True,
        download_name="urunler.csv",
        mimetype="text/csv"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
