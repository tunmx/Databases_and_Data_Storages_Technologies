from sqlalchemy import create_engine

# connect setting
username = 'root'
password = '123456'
host = 'localhost'
port = '3306'
dbname = 'CosmeticsShop'  # any database

def get_engine():
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}')

    return engine
