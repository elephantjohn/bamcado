import os

# 更新以下字段为你本地数据库的实际用户名、密码和数据库名
username = 'root'
hostname = '127.0.0.1'
database_name = 'bamcado'
password = "bamcado"

SQLALCHEMY_DATABASE_URI = f"mysql+asyncmy://{username}:{password}@{hostname}/{database_name}?charset=utf8mb4"


