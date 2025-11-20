from typing import Dict
from task.data_aggregation_task import get_daily_hourly_data
from const.colors_enum import Colors
from app.extensions import redis_util
from datetime import datetime
import json

def get_daily_statistics(serial_id) -> Dict:
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    try:
        hourly_in, hourly_out = get_daily_hourly_data(serial_id, date_str)
        
        total_in = sum(hourly_in)
        total_out = sum(hourly_out)
        net_flow = total_in - total_out
        
        # 找到热点时间（进入数最大的小时）
        peak_hour_index = hourly_in.index(max(hourly_in)) if hourly_in else 0
        peak_hour = f"{peak_hour_index:02d}:00"
        
        return {
            "totalIN": str(total_in),
            "totalOut": str(total_out),
            "netFlow": str(net_flow),
            "peakHour": peak_hour
        }
    except Exception as e:
        print(f"{Colors.RED.value}获取每日统计数据失败: {e}{Colors.END.value}")
        return {
            "totalIn": 0,
            "totalOut": 0,
            "netFlow": 0,
            "peakHour": "0:00"
        }

def get_range_statistics(serial_id, flag: str = 'week') -> Dict:
    if flag == 'week':
        time_str = datetime.now().strftime("%Y-%W")
    elif flag == 'month':
        time_str = datetime.now.strftime('%Y-%m')
    in_key = f"{serial_id}:week_in:{time_str}"
    out_key = f"{serial_id}:week_out:{time_str}"

    try:
        in_data = redis_util.get(in_key)
        out_data = redis_util.get(out_key)
        if in_data == None or out_data == None:
            print(f'{Colors.YELLOW}当前商户为配置，请先配置商户。serial_id:{serial_id}{Colors.END}')
            return {
            "totalIn": 0,
            "totalOut": 0,
            "netFlow": 0,
            "peakHour": 0
        }
        in_value = json.loads(in_data).get('data', [0] * 24)
        out_value = json.loads(out_data).get('data', [0] * 24)

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
            "peakHour": peak_hour
        }
    except Exception  as e:
        print(f'{Colors.RED}Error: 获取周数据出错：{e}{Colors.END}')
        return {
            "totalIn": 0,
            "totalOut": 0,
            "netFlow": 0,
            "peakHour": '0:00'
        }