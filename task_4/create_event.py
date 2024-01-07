import tqdm
from sqlalchemy.orm import sessionmaker
from models import User, Event, Order, OrderDetail, CartItem, Product, Base, Cart
from setting import get_engine
from random import randint, sample, choices
from datetime import datetime, timedelta

# 创建数据库引擎和会话
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

def create_events(batch_size=100):
    # 查询所有用户ID
    user_ids = [user_id for (user_id,) in session.query(User.id).all()]
    selected_user_ids = sample(user_ids, int(len(user_ids) * 0.8))

    purchase_events = session.query(OrderDetail.product_id, Order.user_id, Order.order_date).join(Order, Order.id == OrderDetail.order_id).all()

    count = 0
    for product_id, user_id, order_date in tqdm.tqdm(purchase_events):
        create_purchase_and_view_events(user_id, product_id, order_date)
        count += 1
        if count % batch_size == 0:
            session.commit()

    cart_events = session.query(Cart.user_id, CartItem.product_id, CartItem.added_time).join(CartItem,
                                                                                             Cart.id == CartItem.cart_id).all()
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

    # 提交剩余的更改
    session.commit()

def create_purchase_and_view_events(user_id, product_id, order_date):
    purchase_event = Event(user_id=user_id, product_id=product_id, event_type='purchase', event_time=order_date)
    session.add(purchase_event)
    for _ in range(randint(1, 10)):
        view_time = order_date - timedelta(days=randint(1, 30))
        view_event = Event(user_id=user_id, product_id=product_id, event_type='view', event_time=view_time)
        session.add(view_event)

def create_cart_and_remove_events(user_id, product_id, added_time):
    cart_event = Event(user_id=user_id, product_id=product_id, event_type='cart', event_time=added_time)
    session.add(cart_event)
    if randint(0, 1):
        remove_time = added_time + timedelta(days=randint(1, 10))
        remove_event = Event(user_id=user_id, product_id=product_id, event_type='remove_from_cart', event_time=remove_time)
        session.add(remove_event)

def create_view_events(user_id):
    product_id = sample(session.query(Product.id).all(), 1)[0][0]
    view_time = datetime.now() - timedelta(days=randint(1, 30))
    view_event = Event(user_id=user_id, product_id=product_id, event_type='view', event_time=view_time)
    session.add(view_event)

if __name__ == "__main__":
    create_events()
