import random
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from models import User, Event, Order, OrderDetail, CartItem, Product, Cart  # 确保从您的模型文件中导入所需的类
from setting import get_engine  # 确保从您的设置文件中获取数据库引擎配置
import tqdm
from random import randint

# 创建数据库引擎和会话
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

def generate_unique_id(model):
    """生成一个对于指定模型唯一的随机ID。"""
    max_id = 1000000000
    while True:
        random_id = random.randint(1, max_id)
        if not session.query(model.id).filter_by(id=random_id).first():
            return random_id

def create_purchase_and_view_events(user_id, product_id, order_date):
    event_id = generate_unique_id(Event)
    purchase_event = Event(id=event_id, user_id=user_id, product_id=product_id, event_type='purchase', event_time=order_date)
    session.add(purchase_event)
    for _ in range(randint(1, 10)):
        view_event_id = generate_unique_id(Event)
        view_time = order_date - timedelta(days=randint(1, 30))
        view_event = Event(id=view_event_id, user_id=user_id, product_id=product_id, event_type='view', event_time=view_time)
        session.add(view_event)

def create_cart_and_remove_events(user_id, product_id, added_time):
    cart_event_id = generate_unique_id(Event)
    cart_event = Event(id=cart_event_id, user_id=user_id, product_id=product_id, event_type='cart', event_time=added_time)
    session.add(cart_event)
    if random.choice([True, False]):
        remove_event_id = generate_unique_id(Event)
        remove_time = added_time + timedelta(days=randint(1, 10))
        remove_event = Event(id=remove_event_id, user_id=user_id, product_id=product_id, event_type='remove_from_cart', event_time=remove_time)
        session.add(remove_event)

def create_view_events(user_id):
    view_event_id = generate_unique_id(Event)
    product_id = random.choice([pid for (pid,) in session.query(Product.id).all()])
    view_time = datetime.now() - timedelta(days=randint(1, 30))
    view_event = Event(id=view_event_id, user_id=user_id, product_id=product_id, event_type='view', event_time=view_time)
    session.add(view_event)

def create_events(batch_size=100):
    user_ids = [user_id for (user_id,) in session.query(User.id).all()]
    selected_user_ids = random.sample(user_ids, int(len(user_ids) * 0.8))

    purchase_events = session.query(OrderDetail.product_id, Order.user_id, Order.order_date).join(Order, Order.id == OrderDetail.order_id).all()
    count = 0
    for product_id, user_id, order_date in tqdm.tqdm(purchase_events):
        create_purchase_and_view_events(user_id, product_id, order_date)
        count += 1
        if count % batch_size == 0:
            session.commit()

    cart_events = session.query(Cart.user_id, CartItem.product_id, CartItem.added_time).join(CartItem, Cart.id == CartItem.cart_id).all()
    for user_id, product_id, added_time in tqdm.tqdm(cart_events):
        create_cart_and_remove_events(user_id, product_id, added_time)
        count += 1
        if count % batch_size == 0:
            session.commit()

    for user_id in tqdm.tqdm(selected_user_ids):
        create_view_events(user_id)
        count += 1
        if count % batch_size == 0:
            session.commit()

    session.commit()

if __name__ == "__main__":
    create_events()
