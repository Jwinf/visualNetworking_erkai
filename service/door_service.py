from const.colors_enum import Colors
from const.redis_key import DOOR_STATE, SERIAL_ID_MAP
from app.extensions import redis_util
import threading
from task.hourly_task import schedule_thread

def set(data):
    # 提取字段
    merchant_name = data['merchant']
    x1 = data['x1']
    y1 = data['y1']
    x2 = data['x2']
    y2 = data['y2']
    state = data['direction']
    serial_id = data['serial_id']
    
    # 打印接收到的数据（用于调试）
    print(f"{Colors.GREEN.value}Received data: merchant_name = {merchant_name}, x1={x1}, y1={y1}, x2={x2}, y2={y2}, state={state}, serial_id={serial_id}{Colors.END.value}")   
    # 存入redis
    redis_util.hset(SERIAL_ID_MAP, serial_id, merchant_name)
    redis_util.hmset(f'{merchant_name}:{DOOR_STATE}', {
        'x1': x1,'y1': y1, 'x2': x2, 'y2': y2, 'state': state
    })

    scheduler_thread = threading.Thread(target=schedule_thread, daemon=True)
    scheduler_thread.start()