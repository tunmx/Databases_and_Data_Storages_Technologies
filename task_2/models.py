from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from setting import get_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    registration_date = Column(DateTime, default=func.now())
    last_login = Column(DateTime, onupdate=func.now())

    # Relationships
    orders = relationship('Order', back_populates='user')
    events = relationship('Event', back_populates='user')
    carts = relationship('Cart', back_populates='user')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    brand = Column(String(50))
    price = Column(Float, nullable=False)
    description = Column(String(255))
    stock_quantity = Column(Integer, nullable=False)

    # Relationships
    order_details = relationship('OrderDetail', back_populates='product')
    events = relationship('Event', back_populates='product')
    cart_items = relationship('CartItem', back_populates='product')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True)
    parent_category_id = Column(Integer, ForeignKey('categories.id'))

    # Relationship to products
    products = relationship('Product', back_populates='category')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_date = Column(DateTime, default=func.now())
    status = Column(String(50))
    total_price = Column(Float, nullable=False)

    # Relationships
    user = relationship('User', back_populates='orders')
    order_details = relationship('OrderDetail', back_populates='order')

class OrderDetail(Base):
    __tablename__ = 'order_details'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    discount = Column(Float)

    # Relationships
    order = relationship('Order', back_populates='order_details')
    product = relationship('Product', back_populates='order_details')

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    event_type = Column(String(50))
    event_time = Column(DateTime, default=func.now())

    # Relationships
    user = relationship('User', back_populates='events')
    product = relationship('Product', back_populates='events')

class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    user = relationship('User', back_populates='carts')
    cart_items = relationship('CartItem', back_populates='cart')

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    added_time = Column(DateTime, default=func.now())

    # Relationships
    cart = relationship('Cart', back_populates='cart_items')
    product = relationship('Product', back_populates='cart_items')

if __name__ == "__main__":
    engine = get_engine()
    Base.metadata.create_all(engine)
