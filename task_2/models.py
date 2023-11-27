from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    registration_date = Column(DateTime, default=func.now())
    last_login = Column(DateTime, onupdate=func.now())

    # Relationship to orders
    orders = relationship('Order', back_populates='user')


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    brand = Column(String)
    price = Column(Float, nullable=False)
    description = Column(String)
    stock_quantity = Column(Integer, nullable=False)

    # Relationship to order details
    order_details = relationship('OrderDetail', back_populates='product')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)
    parent_category_id = Column(Integer, ForeignKey('categories.id'))

    # Relationship to products
    products = relationship('Product', back_populates='category')
    # Relationship for subcategories
    subcategories = relationship('Category')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_date = Column(DateTime, default=func.now())
    status = Column(String)
    total_price = Column(Float, nullable=False)

    # Relationship to user
    user = relationship('User', back_populates='orders')
    # Relationship to order details
    order_details = relationship('OrderDetail', back_populates='order')


class OrderDetail(Base):
    __tablename__ = 'order_details'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    discount = Column(Float)

    # Relationship to order
    order = relationship('Order', back_populates='order_details')
    # Relationship to product
    product = relationship('Product', back_populates='order_details')


if __name__ == "__main__":
    # Connect to the database (the URL will depend on your database setup)
    engine = create_engine('sqlite:///mydatabase.db')

    # Create the tables in the database
    Base.metadata.create_all(engine)
