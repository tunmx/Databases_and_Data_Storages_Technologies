from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from setting import get_engine

Base = declarative_base()

class User(Base):
    """User model"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # User ID, primary key
    username = Column(String(100), nullable=False, unique=True)  # Username, must be non-null and unique
    email = Column(String(100), nullable=False, unique=True)  # Email, must be non-null and unique
    password_hash = Column(String(255), nullable=False)  # Password hash, must be non-null
    registration_date = Column(DateTime, default=func.now())  # Registration date and time, defaults to now
    last_login = Column(DateTime, onupdate=func.now())  # Last login date and time, updates on login

    # Relationships with other tables
    orders = relationship('Order', back_populates='user')  # User's orders
    events = relationship('Event', back_populates='user')  # User's events
    cart = relationship('Cart', uselist=False, back_populates='user', cascade='all, delete-orphan')  # User's cart

class Product(Base):
    """Product model"""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)  # Product ID, primary key
    name = Column(String(100), nullable=False)  # Product name, must be non-null
    category_id = Column(Integer, ForeignKey('categories.id'))  # Foreign key to category
    brand = Column(String(50))  # Brand
    price = Column(Float, nullable=False)  # Price, must be non-null
    description = Column(String(255))  # Description
    stock_quantity = Column(Integer, nullable=False)  # Stock quantity, must be non-null

    # Relationships with other tables
    order_details = relationship('OrderDetail', back_populates='product')  # Product's order details
    events = relationship('Event', back_populates='product')  # Product's events
    cart_items = relationship('CartItem', back_populates='product')  # Products in the cart

class Category(Base):
    """Category model"""
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)  # Category ID, primary key
    name = Column(String(100), nullable=False, unique=True)  # Category name, must be non-null and unique
    code = Column(String(50), nullable=False, unique=True)  # Category code, must be non-null and unique
    parent_category_id = Column(Integer, ForeignKey('categories.id'))  # Parent category ID, foreign key

    # Relationship with the product table
    products = relationship('Product', back_populates='category')  # Products belonging to this category

class Order(Base):
    """Order model"""
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)  # Order ID, primary key
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to user who created the order
    order_date = Column(DateTime, default=func.now())  # Order creation date and time, defaults to now
    status = Column(String(50))  # Order status
    total_price = Column(Float, nullable=False)  # Total price of the order, must be non-null

    # Relationships with other tables
    user = relationship('User', back_populates='orders')  # User who placed the order
    order_details = relationship('OrderDetail', back_populates='order')  # Order details

class OrderDetail(Base):
    """Order detail model"""
    __tablename__ = 'order_details'
    id = Column(Integer, primary_key=True)  # Order detail ID, primary key
    order_id = Column(Integer, ForeignKey('orders.id'))  # Foreign key to the order
    product_id = Column(Integer, ForeignKey('products.id'))  # Foreign key to the product
    quantity = Column(Integer, nullable=False)  # Quantity of the product, must be non-null
    price = Column(Float, nullable=False)  # Price of the product, must be non-null
    discount = Column(Float)  # Discount on the product, if applicable

    # Relationships with other tables
    order = relationship('Order', back_populates='order_details')  # The order to which this detail belongs
    product = relationship('Product', back_populates='order_details')  # The product in this order detail

class Event(Base):
    """Event model"""
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)  # Event ID, primary key
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to the user related to the event
    product_id = Column(Integer, ForeignKey('products.id'))  # Foreign key to the product related to the event
    event_type = Column(String(50))  # Type of event (e.g., view, add to cart, etc.)
    event_time = Column(DateTime, default=func.now())  # Date and time of the event, defaults to now

    # Relationships with other tables
    user = relationship('User', back_populates='events')  # User related to this event
    product = relationship('Product', back_populates='events')  # Product related to this event

class Cart(Base):
    """Cart model"""
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)  # Cart ID, primary key
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)  # Foreign key to the user, unique

    # Relationships with other tables
    user = relationship('User', back_populates='cart')  # User owning this cart
    cart_items = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')  # Items in the cart

class CartItem(Base):
    """Cart item model"""
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)  # Cart item ID, primary key
    cart_id = Column(Integer, ForeignKey('carts.id'))  # Foreign key to the cart
    product_id = Column(Integer, ForeignKey('products.id'))  # Foreign key to the product
    quantity = Column(Integer, nullable=False)  # Quantity of the product in the cart, must be non-null
    added_time = Column(DateTime, default=func.now())  # Date and time the product was added to the cart, defaults to now

    # Relationships with other tables
    cart = relationship('Cart', back_populates='cart_items')  # The cart to which this item belongs
    product = relationship('Product', back_populates='cart_items')  # The product in this cart item

if __name__ == "__main__":
    engine = get_engine()
    Base.metadata.create_all(engine)
