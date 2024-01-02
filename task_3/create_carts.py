import tqdm
from sqlalchemy.orm import sessionmaker
from models import User, Cart, Base
from setting import get_engine

# 创建数据库引擎和会话
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

def create_carts_for_all_users():
    # 查询所有用户的ID
    user_ids = session.query(User.id).all()

    # 为每个用户创建购物车
    for user_id in tqdm.tqdm(user_ids):
        cart = Cart(user_id=user_id[0])  # User.id 返回的是一个元组，我们需要第一个元素
        session.add(cart)

    # 提交会话以保存更改
    session.commit()

if __name__ == "__main__":
    create_carts_for_all_users()
