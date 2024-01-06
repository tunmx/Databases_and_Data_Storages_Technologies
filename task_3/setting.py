from sqlalchemy import create_engine

# connect setting
username = 'root'
password = '123456'
host = 'localhost'
port = '3306'
dbname = 'CosmeticsShopMyISAM'  # any database
# dbname = 'CosmeticsShop'  # any database

use_mysql_engine = "MyISAM"
# use_mysql_engine = "InnoDB"

def get_engine():
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}')

    return engine
