import os
#调试模式是否开启
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
#session必须要设置key
SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#mysql数据库连接信息,这里改为自己的账号

#DATABASE_HOST="3.1.75.82:3306"
#DATABASE_USER="root"
#DATABASE_PASS="!@#sam@5678/*-"
#DATABASE_NAME="StockEveryday"
#app.config['SQLALCHEMY_DATABASE_URL'] = r"mysql+pymysql://root:!@#sam@5678/*-@3.1.75.82:3306/StockEveryday"
SQLALCHEMY_DATABASE_URI = r"mysql+pymysql://root:!@#sam@5678/*-@3.1.75.82:3306/StockEveryday"
        