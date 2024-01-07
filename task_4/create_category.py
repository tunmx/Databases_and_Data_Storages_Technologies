import csv
from models import Category, Base
from setting import get_engine
from sqlalchemy.orm import sessionmaker

# 配置数据库连接和会话
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()


def create_category(label, code):
    """创建一个新的类别实例"""
    category = Category(name=label, code=code)
    session.add(category)


def generate_unique_code(id):
    """为类别生成一个唯一的code，可以基于id来生成"""
    return f"CATEGORY-{id:05d}"


def import_categories_from_csv(csv_file_path):
    Base.metadata.create_all(engine)  # 创建数据库表

    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        unique_labels = set()  # 使用集合去重
        for row in reader:
            label = row['Label']  # 此处可以直接使用 'Label'，因为BOM已经被处理
            if label not in unique_labels:
                unique_labels.add(label)

        # 已去重的标签可以用来创建Category实例
        for id, label in enumerate(unique_labels, start=1):
            code = generate_unique_code(id)
            create_category(label, code)

        session.commit()  # 提交会话，保存到数据库

if __name__ == "__main__":
    csv_file_path = 'cosmetics.csv'  # 替换为CSV文件的实际路径
    import_categories_from_csv(csv_file_path)
