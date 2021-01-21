from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ItemTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=True)
    desc = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return self.name


@app.route('/buy/<int:id>')
def buy(id):
    item = ItemTable.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@app.route('/')
def index():
    items = ItemTable.query.all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        desc = request.form['desc']

        item = ItemTable(name=name, price=price, desc=desc)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ошибка'
    else:
        return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)