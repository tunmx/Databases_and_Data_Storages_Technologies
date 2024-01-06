import random
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from models import Event, Product, User  # 确保从你的模型文件中导入 Event, Product, User
from setting import get_engine  # 从您的设置文件中获取数据库引擎配置
import tqdm

# 创建数据库引擎和会话
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

def create_view_events(total_events=500, batch_size=128):
    # 查询所有产品ID和用户ID
    product_ids = [pid for (pid,) in session.query(Product.id).all()]
    user_ids = [uid for (uid,) in session.query(User.id).all()]

    # 初始化计数器
    count = 0

    with tqdm.tqdm(total=total_events) as pbar:
        while count < total_events:
            # 生成一个批次的事件
            events_batch = []
            for _ in range(min(batch_size, total_events - count)):
                user_id = random.choice(user_ids)
                product_id = random.choice(product_ids)
                view_time = datetime.now() - timedelta(days=random.randint(1, 30))

                event_id = random.randint(1, 1000000000)
                while session.query(Event.id).filter_by(id=event_id).scalar() is not None:
                    event_id = random.randint(1, 1000000000)

                events_batch.append(Event(id=event_id, user_id=user_id, product_id=product_id, event_type='view', event_time=view_time))
                count += 1

            # 将批次的事件添加到数据库并提交
            session.bulk_save_objects(events_batch)
            session.commit()
            pbar.update(len(events_batch))

if __name__ == "__main__":
    create_view_events(500000, 512)  # 生成并插入500条随机事件，每批次最少128条
