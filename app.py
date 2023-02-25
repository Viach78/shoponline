from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title


with app.app_context():
    db.create_all()
    db.session.commit()



@app.route('/')
def index():
    item = Item.query.order_by(Item.price).all()
    return render_template("index.html", item=item)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/buy/<int:id>')
def buy(id):
    item = Item.query.get(id)
    return render_template("buy.html", item=item)


@app.route('/buy_id/<int:id>')
def buy_id(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": item.price
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка ввода данных"
    else:

        return render_template("create.html")




if __name__ == '__main__':
    app.run(debug=True)