import tqdm
from sqlalchemy.orm import sessionmaker
from models import User, Cart, CartItem, Product, Base
from setting import get_engine
from random import randint, sample, uniform
from datetime import datetime

# 创建数据库引擎和会话
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()


def random_date(start, end):
    """生成两个日期之间的随机日期"""
    return start + (end - start) * uniform(0, 1)


def create_cart_items():
    # 查询所有用户ID、购物车ID、注册日期和最后登录时间
    users_with_cart = session.query(User.id, Cart.id, User.registration_date, User.last_login).join(Cart,
                                                                                                    User.id == Cart.user_id).all()

    # 随机选择60%的用户
    selected_users = sample(users_with_cart, int(len(users_with_cart) * 0.6))

    # 获取所有产品的ID
    product_ids = [prod_id for (prod_id,) in session.query(Product.id).all()]

    for user_id, cart_id, registration_date, last_login in tqdm.tqdm(selected_users):
        # 为每个选中的用户随机添加1到10种商品
        for _ in range(randint(1, 10)):
            # 随机选择一个产品
            product_id = sample(product_ids, 1)[0]
            # 随机生成1到5件产品的数量
            quantity = randint(1, 5)
            # 生成一个在注册日期和最后登录日期之间的随机日期
            added_time = random_date(registration_date, last_login) if last_login else registration_date

            cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity, added_time=added_time)
            session.add(cart_item)

    # 提交会话以保存更改
    session.commit()


if __name__ == "__main__":
    create_cart_items()
