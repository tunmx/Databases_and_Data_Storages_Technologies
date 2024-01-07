import tqdm
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
import hashlib
import datetime
from models import *
from setting import get_engine

engine = get_engine()

Session = sessionmaker(bind=engine)  # 创建session工厂

# 初始化Faker
fake = Faker()


def create_fake_user():
    """创建一个伪造的用户并返回。"""
    base_username = fake.user_name() + str(random.randint(1000, 99999))  # 加入随机数字以生成唯一用户名
    email = f"{base_username}@{fake.free_email_domain()}"
    password_hash = hashlib.sha256(fake.word().encode('utf-8')).hexdigest()
    registration_date = fake.date_time_between(start_date='-10y', end_date='-2y')
    last_login = fake.date_time_between(start_date=registration_date, end_date='now')

    return User(username=base_username, email=email, password_hash=password_hash,
                registration_date=registration_date, last_login=last_login)


def insert_fake_users(num):
    Base.metadata.create_all(engine)
    session = Session()
    for _ in tqdm.tqdm(range(num)):
        user = create_fake_user()
        session.add(user)

    session.commit()
    session.close()  # 关闭session






if __name__ == "__main__":
    # 创建用户数据
    insert_fake_users(10032)
