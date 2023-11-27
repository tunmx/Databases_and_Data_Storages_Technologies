import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print(sqlalchemy.__version__)

# 连接信息
username = 'root'  # 通常是root
password = '123456'  # 替换为你的密码
host = 'localhost'  # 如果你的docker运行在本机上
port = '3306'
dbname = 's2023'  # 可以是任何数据库名，这里使用默认的mysql数据库

# 创建连接引擎
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}')

# 测试连接
with engine.connect() as conn:
    result = conn.execute("select version()")
    print(result.fetchone())
