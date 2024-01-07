import csv
from models import Product, Category, Base
from setting import get_engine
from sqlalchemy.orm import sessionmaker
from random import randint

# 配置数据库连接和会话
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

# 类别名称到ID的映射
category_name_to_id = {
    'Moisturizer': 1,
    'Cleanser': 2,
    'Treatment': 3,
    'Sun protect': 4,
    'Face Mask': 5,
    'Eye cream': 6
}


def create_product(name, brand, price, description, category_name):
    """创建一个新的产品实例"""
    category_id = category_name_to_id[category_name]
    stock_quantity = randint(1, 500)  # 生成1到500之间的随机库存量
    product = Product(
        name=name,
        brand=brand,
        price=price,
        description=description,
        stock_quantity=stock_quantity,
        category_id=category_id
    )
    session.add(product)

def import_products_from_csv(csv_file_path):
    Base.metadata.create_all(engine)  # 创建数据库表

    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        # 获取正确的列名
        label_column = reader.fieldnames[0] if reader.fieldnames[0].startswith('\ufeff') else 'Label'
        for row in reader:
            create_product(
                name=row['Name'],
                brand=row['Brand'],
                price=float(row['Price']),
                description=row['Ingredients'],  # 使用了Ingredients列作为描述
                category_name=row[label_column]  # 使用正确的列名，处理BOM
            )

        session.commit()  # 提交会话，保存到数据库


if __name__ == "__main__":
    csv_file_path = 'cosmetics.csv'  # 替换为CSV文件的实际路径
    import_products_from_csv(csv_file_path)
