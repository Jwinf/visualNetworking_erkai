from flask import Flask
from config.config import config
from config.config import get_config

def create_app(config_name=None):
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
    app.register_blueprint(door_controller, url_prefix='/erkai/visualnet')
    
    return app