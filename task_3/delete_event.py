import tqdm
from sqlalchemy.orm import sessionmaker
from models import User, Event, Order, OrderDetail, CartItem, Product, Base, Cart
from setting import get_engine
from random import randint, sample, choices
from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine, func

engine = get_engine()

Session = sessionmaker(bind=engine)
session = Session()
print(session)

try:
    # 查询 Event 表中的总记录数
    total_events = session.query(func.count(Event.id)).scalar()
    print(total_events)
    num_to_delete = total_events * 30 // 100  # 计算要删除的记录数（30%）
    print(num_to_delete)
    # 设置每批删除的记录数
    batch_size = 100  # 可以根据需要调整这个数值
    batches = num_to_delete // batch_size

    # 获取随机的记录ID
    random_ids = random.sample(
        [event.id for event in session.query(Event.id).all()], num_to_delete
    )

    # 执行批量删除操作
    for _ in tqdm.tqdm(range(batches)):
        batch_ids = random_ids[:batch_size]
        random_ids = random_ids[batch_size:]
        session.query(Event).filter(Event.id.in_(batch_ids)).delete(synchronize_session='fetch')
        session.commit()

    # 删除剩余的记录（如果有）
    if random_ids:
        session.query(Event).filter(Event.id.in_(random_ids)).delete(synchronize_session='fetch')
        session.commit()

    print(f"{num_to_delete} records have been deleted.")
except Exception as e:
    session.rollback()
    print(f"An error occurred: {e}")
finally:
    session.close()