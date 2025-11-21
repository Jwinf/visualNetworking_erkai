from flask import Flask
from config.config import config
from config.config import get_config

def banner():
    with open('E:\workplace\VSCodeWorkplace\\visualNetworking_erkai\static\\favicon.txt', 'r') as f:
        print(f.read())

def create_app(config_name=None):
    banner()

    app = Flask(__name__)
    
    # 配置应用
    if config_name is None:
        app.config.from_object(get_config())
    else:
        app.config.from_object(config[config_name])
    
    # 初始化扩展
    from app.extensions import redis_util
    redis_util.init_app(app)
    
    # 注册蓝图
    from app.controller.door_controller import door_controller
    from app.controller.data_source_controller import data_source_controller
    from app.controller.white_list_controller import white_list_controller
    app.register_blueprint(door_controller, url_prefix='/erkai/visualnet')
    app.register_blueprint(data_source_controller, url_prefix='/erkai/visualnet')
    app.register_blueprint(white_list_controller, url_prefix='/erkai/visualnet')
    
    return app