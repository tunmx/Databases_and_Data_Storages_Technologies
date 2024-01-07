import tqdm
from sqlalchemy.orm import sessionmaker
from models import User, Order, OrderDetail, Product, Base
from setting import get_engine
from random import randint, sample, choices, uniform
from datetime import datetime, timedelta


def random_date(start, end):
    """生成两个日期之间的随机日期"""
    return start + (end - start) * uniform(0, 1)

def create_orders_and_details(session, batch_size=100):
    # 查询所有用户ID和相关日期信息
    user_data = session.query(User.id, User.registration_date, User.last_login).all()

    # 随机选择约60%的用户
    selected_user_data = sample(user_data, int(len(user_data) * 0.6))

    # 获取所有产品的ID和价格
    products = session.query(Product.id, Product.price).all()

    # 设置订单状态选项
    status_options = ['Pending', 'Processing', 'Shipped', 'Cancelled', 'Completed']
    status_probabilities = [0.1, 0.1, 0.1, 0.1, 0.6]

    count = 0
    for user_id, registration_date, last_login in tqdm.tqdm(selected_user_data):
        last_login = last_login if last_login else datetime.now()

        for _ in range(randint(1, 15)):
            order_date = random_date(registration_date, last_login)
            status = choices(status_options, status_probabilities)[0]
            if status == 'Completed':
                order_date = random_date(registration_date, registration_date + timedelta(days=30))

            order = Order(user_id=user_id, order_date=order_date, status=status, total_price=0)
            session.add(order)
            session.flush()

            total_price = 0
            for _ in range(randint(1, 5)):
                product_id, product_price = sample(products, 1)[0]
                quantity = randint(1, 5)
                discount = 1

                order_detail = OrderDetail(order_id=order.id, product_id=product_id, quantity=quantity, price=product_price * discount)
                total_price += product_price * discount * quantity
                session.add(order_detail)

            order.total_price = total_price
            count += 1

            # 分批提交
            if count % batch_size == 0:
                session.commit()
                session.close()
                session = Session()

    # 提交剩余的数据
    session.commit()

if __name__ == "__main__":
    # 创建数据库引擎和会话
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    create_orders_and_details(session)
