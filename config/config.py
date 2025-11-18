import os

# 通用配置
class Config:
    pass

# 开发环境配置
class DevelopmentConfig:
    DEBUG = True
    ENV = 'development'
    REDIS_HOST = os.environ.get('DEV_REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('DEV_REDIS_PORT', 6379)
    REDIS_PASSWORD = os.environ.get('DEV_REDIS_PASSWORD', None)
    REDIS_DECODE_RESPONSES =os.environ.get('DEV_REDIS_DECODE_RESPONSES', True)
    REDIS_TIMEOUT = os.environ.get('DEV_REDIS_TIMEOUT', 5)

class ProductionConfig:
    ENV = 'product'
    REDIS_HOST = os.environ.get('PRO_REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('PRO_REDIS_PORT', 6379)
    REDIS_PASSWORD = os.environ.get('PRO_REDIS_PASSWORD', None)
    REDIS_DECODE_RESPONSES =os.environ.get('PRO_REDIS_DECODE_RESPONSES', True)
    REDIS_TIMEOUT = os.environ.get('PRO_REDIS_TIMEOUT', 5)

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """获取当前环境配置"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
