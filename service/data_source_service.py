from typing import Dict
from task.data_aggregation_task import get_daily_hourly_data
from const.colors_enum import Colors
from app.extensions import redis_util
from datetime import datetime
import json

def get_statistics(serial_id, flag: str) -> Dict:
    in_value = []
    out_value = []
    match flag:
        case 'day':
            in_value, out_value = get_daily_hourly_data(serial_id)
        case 'week' | 'month':
            time_str = datetime.now().strftime("%Y-%W") if flag == 'week' else datetime.now.strftime('%Y-%m')
            in_key = f"{serial_id}:week_in:{time_str}"
            out_key = f"{serial_id}:week_out:{time_str}"
            try:
                in_data = redis_util.get(in_key)
                out_data = redis_util.get(out_key)
                if in_data == None or out_data == None:
                    print(f'{Colors.YELLOW}当前商户为配置，请先配置商户。serial_id:{serial_id}{Colors.END}')
                    return empty_result()
                in_value = json.loads(in_data).get('data', [0] * 24)
                out_value = json.loads(out_data).get('data', [0] * 24)
            except Exception  as e:
                print(f'{Colors.RED}Error: 获取周数据出错：{e}{Colors.END}')
                return empty_result()

    total_in = sum(in_value)
    total_out = sum(out_value)
    net_flow = total_in - total_out
    
    # 找到热点时间（进入数最大的小时）
    peak_hour_index = in_value.index(max(in_value)) if in_value else 0
    peak_hour = f"{peak_hour_index:02d}:00"

    return {
        "totalIN": str(total_in),
        "totalOut": str(total_out),
        "netFlow": str(net_flow),
        "peakHour": peak_hour,
        "in_data": in_value,
        "out_data": out_value,
        "labels":  [f"{hour:02d}:00" for hour in range(len(in_data))]
    }

def empty_result():
    return {
        "totalIn": 0,
        "totalOut": 0,
        "netFlow": 0,
        "peakHour": 0,
        "in_data": [],
        "out_data": [],
        'labels' : [f"{hour:02d}:00" for hour in range(24)]
    }
