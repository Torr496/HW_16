import json
import raw_data

from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON AS ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def instance_to_dict(self):
        """
        Трансформируем в словарь
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    customer = db.relationship("Order", foreign_keys=[order_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def instance_to_dict(self):
        """
        Трансформируем в словарь
        """
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,

        }


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def istance_to_dict(self):
        """
        Трансформируем в словарь
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,

        }


db.create_all()

for user_data in raw_data.users:
    new_user = User(
        id=user_data["id"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        age=user_data["age"],
        email=user_data["email"],
        role=user_data["role"],
        phone=user_data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()

for offer_data in raw_data.offers:
    new_offer = Offer(
        id=offer_data["id"],
        order_id=offer_data["order_id"],
        executor_id=offer_data["executor_id"],
    )
    db.session.add(new_offer)
    db.session.commit()

for order_data in raw_data.orders:
    new_orders = Order(
        id=order_data["id"],
        name=order_data["name"],
        description=order_data["description"],
        start_date=order_data["start_date"],
        end_date=order_data["end_date"],
        address=order_data["address"],
        price=order_data["price"],
        customer_id=order_data["customer_id"],
        executor_id=order_data["executor_id"],

    )
    db.session.add(new_orders)
    db.session.commit()



@app.route("/users", methods=["GET", "POST"])
def all_users():
    if request.method == "GET":
        res = []
        for u in User.query.all():
            res.append(u.instance_to_dict())
        return jsonify(res)

    elif request.method == "POST":
        user_data = request.json
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )
        db.session.add(new_user)
        db.session.commit()
        return "", 201


@app.route('/users/<int:uid>', methods=["GET", "PUT", "DELETE"])
def user(uid: int):
    if request.method == "GET":
        return jsonify(User.query.get(uid).instance_to_dict())
    elif request.method == "DELETE":
        u = User.query.get(uid)
        db.session.delete(u)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        user_ = request.json
        u = User.query.get(uid)
        u.first_name=user_["first_name"],
        u.last_name=user_["last_name"],
        u.age=user_["age"],
        u.email=user_["email"],
        u.role=user_["role"],
        u.phone=user_["phone"],
        db.session.add(u)
        db.session.commit()
        return "", 204


@app.route("/offers", methods=["GET", "POST"])
def all_offers():
    if request.method == "GET":
        res = []
        for o in Offer.query.all():
            res.append(o.instance_to_dict())
        return jsonify(res)

    elif request.method == "POST":
        offer_data = request.json
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=user_data["executor_id"],

        )
        db.session.add(new_offer)
        db.session.commit()
        return "", 201


@app.route('/offers/<int:uid>', methods=["GET", "PUT", "DELETE"])
def offer(uid: int):
    if request.method == "GET":
        return jsonify(Offer.query.get(uid).instance_to_dict())
    elif request.method == "DELETE":
        o = Offer.query.get(uid)
        db.session.delete(o)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        offer_ = request.json
        o = User.query.get(uid)
        o.order_id=offer_["order_id"],
        o.executor_id=offer_["executor_id"],
        db.session.add(o)
        db.session.commit()
        return "", 204

@app.route("/orders", methods=["GET", "POST"])
def all_orders():
    if request.method == "GET":
        res = []
        for ord in Order.query.all():
            res.append(ord.istance_to_dict())
        return jsonify(res)

    elif request.method == "POST":
        order_data = request.json
        new_order = Order(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"],

        )
        db.session.add(new_order)
        db.session.commit()
        return "", 201

@app.route('/orders/<int:uid>', methods=["GET", "PUT", "DELETE"])
def orders(uid: int):
    if request.method == "GET":
        return jsonify(Order.query.get(uid).istance_to_dict())
    elif request.method == "DELETE":
        ord = Order.query.get(uid)
        db.session.delete(ord)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        orders_ = request.json
        o = User.query.get(uid)
        o.name=orders_["name"],
        o.description=orders_["description"],
        o.start_date = orders_["start_date"],
        o.end_date = orders_["end_date"],
        o.address = orders_["address"],
        o.price = orders_["price"],
        o.customer_id = orders_["customer_id"],
        o.executor_id = orders_["executor_id"],
        db.session.add(o)
        db.session.commit()
        return "", 204



if __name__ == '__main__':
    app.run()
