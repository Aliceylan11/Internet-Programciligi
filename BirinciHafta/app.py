from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login/dashboard/reports")
def reports():
    return render_template("reports.html")

@app.route("/login/dashboard/critical_stock")
def critical_stock():
    return render_template("critical_stock.html")

@app.route("/login/dashboard/category")
def category():
    return render_template("categories.html")

@app.route("/login/dashboard/users")
def users():
    return render_template("users.html")

@app.route("/login/dashboard/products")
def products():
    return render_template("products.html")

@app.route("/login/dashboard/products/add")
def products_add():
    return render_template("products_add.html")

@app.route("/login/dashboard/products/del")
def products_del():
    return render_template("products_del.html")

@app.route("/login/dashboard/products/update")
def products_update():
    return render_template("products_update.html")

if __name__ == "__main__":
    app.run(debug=True)
