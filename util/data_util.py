import redis
import json
from app.extensions import redis_util
from const.redis_key import IN_NUM, OUT_NUM

def get_realtime_data(merchant_name: str):
    """获取实时进出数据"""
    # 这里替换为你的实际数据获取逻辑
    
    redis_util.hget(f'{merchant_name}:{IN_NUM}')
    return {
        "in_num": redis_util.hget(f'{merchant_name}:{IN_NUM}'),
        "out_num": redis_util.hget(f'{merchant_name}:{OUT_NUM}')
    }

