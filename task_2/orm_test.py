import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from setting import get_engine

print(sqlalchemy.__version__)
engine = get_engine()

# 测试连接
with engine.connect() as conn:
    result = conn.execute("select version()")
    print(result.fetchone())
