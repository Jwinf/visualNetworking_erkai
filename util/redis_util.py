import redis
import json
from typing import Optional, Any, Dict, Union
from const.colors_enum import Colors

class Redis_util:
    def __init__(self):
        self.redis_client = None
    
    def init_app(self, app):
        """初始化Redis连接"""
        try:
            self.redis_client = redis.Redis(
                host=app.config.get('REDIS_HOST', 'localhost'),
                port=app.config.get('REDIS_PORT', 6379),
                db=app.config.get('REDIS_DB', 0),
                password=app.config.get('REDIS_PASSWORD', None),
                decode_responses=app.config.get('REDIS_DECODE_RESPONSES', True),
                socket_connect_timeout=app.config.get('REDIS_TIMEOUT', 5)
            )
            self.redis_client.ping()
            app.logger.info("Redis连接成功")
            
            # 将Redis实例添加到app上下文
            app.redis = self
            
            # 注册关闭连接的teardown
            @app.teardown_appcontext
            def close_redis(error):
                if hasattr(app, 'redis') and app.redis.redis_client:
                    app.redis.redis_client.close()
                    app.logger.info("Redis连接已关闭")
                    
        except redis.ConnectionError as e:
            app.logger.error(f"Redis连接失败: {e}")
            raise
        except Exception as e:
            app.logger.error(f"Redis初始化错误: {e}")
            raise

    def hset(self, key: str, field: str, value: Any) -> bool:
            """
            设置哈希表中字段的值
            
            Args:
                key: 哈希表名
                field: 字段名
                value: 字段值
                
            Returns:
                bool: 是否设置成功
            """
            try:
                result = self.redis_client.hset(key, field, value)
                return result >= 0  # hset返回0或1，但新版本可能返回其他值
            except redis.RedisError as e:
                print(f"{Colors.RED}Redis hset操作失败: {e}{Colors.END}")
                return False
            
    def hget(self, key: str, field: str) -> Optional[Any]:
            """
            获取哈希表中字段的值
            
            Args:
                key: 哈希表名
                field: 字段名
                
            Returns:
                Any: 字段值，如果字段不存在返回None
            """
            try:
                return self.redis_client.hget(key, field)
            except redis.RedisError as e:
                print(f"{Colors.RED}Redis hget操作失败: {e}{Colors.END}")
                return None
            
    def hmset(self, key: str, data: Union[Dict, str]) -> bool:
        """
        将JSON数据解析并存储为多个hset字段
        
        Args:
            key: Redis键名
            data: JSON数据，可以是字典或JSON字符串
            
        Returns:
            bool: 是否设置成功
        """
        try:
            # 如果传入的是JSON字符串，则解析为字典
            if isinstance(data, str):
                try:
                    data_dict = json.loads(data)
                except json.JSONDecodeError as e:
                    print(f"JSON解析失败: {e}")
                    return False
            else:
                data_dict = data
            
            # 使用hmset批量设置字段
            if data_dict:
                self.redis_client.hmset(key, data_dict)
                return True
            else:
                print("JSON数据为空")
                return False
                
        except redis.RedisError as e:
            print(f"Redis hset操作失败: {e}")
            return False
        except Exception as e:
            print(f"hset操作发生未知错误: {e}")
            return False
        
    def hget_all(self, key: str) -> Optional[Dict[str, Any]]:
        """
            获取整个哈希表并以JSON格式返回
        
        Args:
            key: Redis键名
            
        Returns:
            Dict: 包含所有字段和值的字典
        """
        return self.redis_client.hgetall(key)
        

    def close(self):
        """关闭Redis连接"""
        if hasattr(self, 'redis_client'):
            self.redis_client.close()