from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from main import app

db = SQLAlchemy(app)

class Product(db.Model):
    """
    Product Model

    Product will not be created in main service, but in admin service
    Main service only need to catch event and store the data
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

class ProductUser(db.Model):
    """
    Product User Model

    A relation table between product and user
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    # Combination of user_id and product_id must be unique
    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

if __name__ == '__main__':
    db.create_all()