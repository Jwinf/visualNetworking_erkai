from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # 配置应用
    app.config.update(
    REDIS_HOST='localhost',
    REDIS_PORT=6379,
    REDIS_DB=0,
    REDIS_PASSWORD=None,
    REDIS_DECODE_RESPONSES=True,
    REDIS_TIMEOUT=5
    )
    
    # 初始化扩展
    from app.extensions import redis_util
    redis_util.init_app(app)
    
    # 注册蓝图
    from app.controller.door_controller import door_controller
    app.register_blueprint(door_controller, url_prefix='/erkai/visualnet')
    
    return app