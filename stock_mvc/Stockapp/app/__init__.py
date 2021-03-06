from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from functools import wraps

#创建项目对象
app = Flask(__name__)
import  os
app.config.from_object('app.utils.setting')     #模块下的setting文件名，不用加py后缀 
app.config.from_envvar('FLASKR_SETTINGS', silent=True)   #环境变量，指向配置文件setting的路径
app.config['SQLALCHEMY_DATABASE_URL'] = #mysql://username:password@server/db



        
# Decorator Function
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if "cookie" in session:
            return func(*args, **kwargs)
        else:            
            return redirect(url_for("login"))
    return wrap

#创建数据库对象 
db = SQLAlchemy(app)
#db.init_app(app)
#bcrypt = Bcrypt(app)
#app 導入後才能import 
from app.model import UserModel, TaiexModel, TodayStockModel, YieldRateModel, ChooseShortTermStrongStockModel
from app.service import TaiexService, TodayStockService, YieldRateService, ShortTermStrongStockService, ChooseShortTermStrongStockService
#只有在app对象之后声明，用于导入view模块
from app.controller import IndexController, TodayStockController, TaiexController, YieldRateController, ShortTermStrongStockController, ChooseShortTermStrongStockController
