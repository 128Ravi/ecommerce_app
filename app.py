"""
from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret123'

# Dummy product data
products = [
    {"id": 1, "name": "Laptop", "price": 55000},
    {"id": 2, "name": "Mobile", "price": 25000},
    {"id": 3, "name": "Headphones", "price": 3000}
]


@app.route('/')
def home():
    return render_template('index.html', products=products)
    


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(product_id)
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart_items = []
    total = 0

    if 'cart' in session:
        for pid in session['cart']:
            product = next(p for p in products if p['id'] == pid)
            cart_items.append(product)
            total += product['price']

    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return "Order placed successfully!"


if __name__ == '__main__':
    app.run(debug=True)

"""

"""
from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret123'

# Electronics products
products = [
    {"id": 1, "name": "Laptop", "price": 55000},
    {"id": 2, "name": "Mobile", "price": 25000},
    {"id": 3, "name": "Headphones", "price": 3000}
]

# Clothes products
clothes = [
    {"id": 101, "name": "T-Shirt", "price": 999},
    {"id": 102, "name": "Jeans", "price": 1999},
    {"id": 103, "name": "Jacket", "price": 3499}
]


@app.route('/')
def home():
    return render_template('index.html', products=products)


@app.route('/clothes')
def clothes_section():
    return render_template('clothes.html', clothes=clothes)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(product_id)
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart_items = []
    total = 0

    if 'cart' in session:
        for pid in session['cart']:
            product = next((p for p in products if p['id'] == pid), None)
            cloth = next((c for c in clothes if c['id'] == pid), None)

            if product:
                cart_items.append(product)
                total += product['price']
            elif cloth:
                cart_items.append(cloth)
                total += cloth['price']

    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return "Order placed successfully!"


if __name__ == '__main__':
    app.run(debug=True)

"""

"""


# The Below Code is working correctly at application level




from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- PRODUCTS ---------------- #

products = [
    {"id": 1, "name": "Laptop", "price": 55000},
    {"id": 2, "name": "Mobile", "price": 25000},
    {"id": 3, "name": "Headphones", "price": 3000},
    {"id": 4, "name": "Charger", "price": 1500}
] 

clothes = [
    {"id": 101, "name": "T-Shirt", "price": 999},
    {"id": 102, "name": "Jeans", "price": 1999},
    {"id": 103, "name": "Jacket", "price": 3499},
    {"id": 104, "name": "Jerkin", "price": 2999}
]

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html", products=products)


@app.route("/clothes")
def clothes_section():
    return render_template("clothes.html", clothes=clothes)


@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)

    

    cart[pid] = cart.get(pid, 0) + 1
    session["cart"] = cart

    return redirect(url_for("cart"))


@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)

    if pid in cart:
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            cart.pop(pid)

    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    cart_items = []
    total = 0
    cart = session.get("cart", {})

    for pid_str, qty in cart.items():
        pid = int(pid_str)

        item = next((p for p in products if p["id"] == pid), None)
        if not item:
            item = next((c for c in clothes if c["id"] == pid), None)

        if item:
            line_total = item["price"] * qty
            cart_items.append({
                "id": pid,
                "name": item["name"],
                "price": item["price"],
                "qty": qty,
                "line_total": line_total
            })
            total += line_total

    return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/checkout")
def checkout():
    session.pop("cart", None)
    return "✅ Order placed successfully!"


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)



"""

""" # Remove this One

from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"   # redirect if not logged in
app.secret_key = "secret123" 

# ---------------- DATABASE CONFIG ---------------- #

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- MODELS ---------------- #


class User(db.Model):
    __tablename__ = "user"   # IMPORTANT

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    cart_items = db.relationship("CartItem", backref="user", lazy=True)


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)



class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    category = db.Column(db.String(50))

class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),   # MUST match __tablename__
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    quantity = db.Column(db.Integer, default=1)

    product = db.relationship("Product")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    category = db.Column(db.String(50))  # electronics / clothes

    def __repr__(self):
        return f"<Product {self.name}>"



# ---------------- INITIALIZE DATABASE ---------------- #

@app.before_request
def create_tables():
    db.create_all()

    # Insert default products only if DB empty
    if not Product.query.first():
        sample_products = [
            Product(name="Laptop", price=55000, category="electronics"),
            Product(name="Mobile", price=25000, category="electronics"),
            Product(name="Headphones", price=3000, category="electronics"),
            Product(name="Charger", price=1500, category="electronics"),
            Product(name="T-Shirt", price=999, category="clothes"),
            Product(name="Jeans", price=1999, category="clothes"),
            Product(name="Jacket", price=3499, category="clothes"),
            Product(name="Jerkin", price=2999, category="clothes"),
        ]
        db.session.add_all(sample_products)
        db.session.commit()

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    products = Product.query.filter_by(category="electronics").all()
    return render_template("index.html", products=products)


@app.route("/clothes")
def clothes_section():
    clothes = Product.query.filter_by(category="clothes").all()
    return render_template("clothes.html", clothes=clothes)

@app.route("/add_to_cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    existing_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(new_item)

    db.session.commit()

    return redirect(url_for("cart"))



@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)

    cart[pid] = cart.get(pid, 0) + 1
    session["cart"] = cart

    return redirect(url_for("cart"))

@app.route("/remove_from_cart/<int:product_id>")
@login_required
def remove_from_cart(product_id):
    item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if item:
        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.session.delete(item)

        db.session.commit()

    return redirect(url_for("cart"))


""""""
@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)

    if pid in cart:
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            cart.pop(pid)

    session["cart"] = cart
    return redirect(url_for("cart"))

"""

"""
@app.route("/cart")
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = 0

    items = []

    for item in cart_items:
        line_total = item.product.price * item.quantity
        total += line_total

        items.append({
            "id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "qty": item.quantity,
            "line_total": line_total
        })

    return render_template("cart.html", cart_items=items, total=total)


@app.route("/cart")
def cart():
    cart_items = []
    total = 0
    cart = session.get("cart", {})

    for pid_str, qty in cart.items():
        product = Product.query.get(int(pid_str))

        if product:
            line_total = product.price * qty
            cart_items.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "qty": qty,
                "line_total": line_total
            })
            total += line_total

    return render_template("cart.html", cart_items=cart_items, total=total)



@app.route("/checkout")
def checkout():
    session.pop("cart", None)
    return "✅ Order placed successfully!"

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
"""








from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash
from flask import request, redirect, url_for, flash
import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin



# ---------------- APP CONFIG ---------------- #

app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ecommerce.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# ---------------- MODELS ---------------- #

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))



class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    category = db.Column(db.String(50))

class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship("User", backref="cart_items")
    product = db.relationship("Product")

# ---------------- USER LOADER ---------------- #

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- INITIALIZE DB ---------------- #

with app.app_context():
    db.create_all()

    # Insert products only if empty
    if not Product.query.first():
        products = [
            Product(name="Laptop", price=65000, category="electronics"),
            Product(name="Mobile", price=35000, category="electronics"),
            Product(name="Headphones", price=3000, category="electronics"),
            Product(name="T-Shirt", price=999, category="clothes"),
            Product(name="Jeans", price=1999, category="clothes"),
            Product(name="Jacket", price=3499, category="clothes"),
        ]
        db.session.add_all(products)
        db.session.commit()

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    products = Product.query.filter_by(category="electronics").all()
    return render_template("index.html", products=products)

@app.route("/clothes")
def clothes():
    clothes = Product.query.filter_by(category="clothes").all()
    return render_template("clothes.html", clothes=clothes)

# ---------------- AUTH ---------------- #



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!")
            return redirect(url_for("register"))

        # Hash password
        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful! Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for("home"))

        else:
            flash("Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# ---------------- CART ---------------- #

@app.route("/add_to_cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if item:
        item.quantity += 1
    else:
        item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(item)

    db.session.commit()
    return redirect(url_for("cart"))

@app.route("/remove_from_cart/<int:product_id>")
@login_required
def remove_from_cart(product_id):
    item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if item:
        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.session.delete(item)

        db.session.commit()

    return redirect(url_for("cart"))

@app.route("/cart")
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    total = 0
    items = []

    for item in cart_items:
        line_total = item.product.price * item.quantity
        total += line_total

        items.append({
            "id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "line_total": line_total
        })

    return render_template("cart.html", cart_items=items, total=total)

@app.route("/checkout")
@login_required
def checkout():
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return "✅ Order placed successfully!"

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


