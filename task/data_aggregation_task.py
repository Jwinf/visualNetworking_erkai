import json
from datetime import datetime, timedelta
from app.extensions import redis_util
from const.redis_key import IN_NUM, OUT_NUM

def store_hourly_data(merchant_name):
    try:
        now = datetime.now()
        hour_timestamp = now.replace(minute=0, second=0, microsecond=0)
        cur_in_num = redis_util.get(f'{merchant_name}:current:{IN_NUM}', 0)
        cur_out_num = redis_util.get(f'{merchant_name}:current:{OUT_NUM}', 0)
        
        # 创建小时数据记录
        hour_in_data = {
            "timestamp": hour_timestamp.isoformat(),
            "value": cur_in_num,
            "hour": now.hour,
            "date": now.strftime("%Y-%m-%d")
        }

        hour_out_data = {
            "timestamp": hour_timestamp.isoformat(),
            "value": cur_out_num,
            "hour": now.hour,
            "date": now.strftime("%Y-%m-%d")
        }
        
        # 存储到每日小时数据列表
        hour_in_data_key = f"{merchant_name}:hour_in:{now.strftime('%Y-%m-%d')}"
        hour_out_data_key = f"{merchant_name}:hour_out:{now.strftime('%Y-%m-%d')}"
        redis_util.rpush(hour_in_data_key, json.dumps(hour_in_data))
        redis_util.rpush(hour_out_data_key, json.dumps(hour_out_data))
        
        # 设置过期时间（2天，确保有足够时间进行聚合）
        redis_util.expire(hour_in_data_key, 3600 * 24 * 2)
        redis_util.expire(hour_out_data_key, 3600 * 24 * 2)
        
        print(f"[{now}] 小时数据已存储: in_num->{cur_in_num}, out_num->{cur_out_num}")
        
        # 触发聚合计算
        _calculate_aggregations()
        
        return True
        
    except Exception as e:
        print(f"存储小时数据失败: {e}")
        return False

def get_daily_hourly_data(merchant_name, date_str=None):
    """获取某天的小时数据"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    hourly_in_key = f"{merchant_name}:hour_in:{date_str}"
    hourly_out_ley = f"{merchant_name}:hour_out:{date_str}"

    in_data_list = redis_util.lrange(hourly_in_key, 0, -1)
    out_data_list = redis_util.lrange(hourly_out_ley, 0, -1)
    
    hourly_in_values = [0] * 24  # 初始化24小时数据
    hourly_out_values = [0] * 24
    
    for data_json in in_data_list:
        try:
            data = json.loads(data_json)
            hour = data.get("hour", 0)
            value = data.get("value", 0)
            if 0 <= hour < 24:
                hourly_in_values[hour] = value
        except Exception as e:
            print(f"解析小时进门数据失败: {e}")
    
    for data_json in out_data_list:
        try:
            data = json.loads(data_json)
            hour = data.get("hour", 0)
            value = data.get("value", 0)
            if 0 <= hour < 24:
                hourly_out_values[hour] = value
        except Exception as e:
            print(f"解析小时出门数据失败: {e}")       
    return hourly_in_values, hourly_out_values

def _calculate_aggregations():
    """计算周度和月度聚合数据"""
    try:
        now = datetime.now()
        
        # 计算周聚合
        _calculate_weekly_aggregation(now)
        
        # 计算月聚合
        _calculate_monthly_aggregation(now)
        
    except Exception as e:
        print(f"计算聚合数据失败: {e}")

def _calculate_weekly_aggregation(merchant_name, current_time):
    """计算本周的小时数据聚合"""
    try:
        # 获取本周的开始日期（周一）
        start_of_week = current_time - timedelta(days=current_time.weekday())
        
        weekly_hourly_in_data = [[] for _ in range(24)]  # 24小时，每个小时一个列表
        weekly_hourly_out_data = [[] for _ in range(24)]
        
        # 遍历本周的每一天
        for day_offset in range(7):
            current_date = start_of_week + timedelta(days=day_offset)
            if current_date > current_time:
                break
            date_str = current_date.strftime("%Y-%m-%d")
            
            # 获取当天的24小时数据
            daily_in_values, daily_out_values = get_daily_hourly_data(merchant_name, date_str)
            
            # 将每个小时的数据添加到对应的聚合列表中
            for hour in range(24):
                weekly_hourly_in_data[hour].append(daily_in_values[hour])
                weekly_hourly_out_data[hour].append(daily_out_values[hour])
        
        # 计算每个小时的平均值（或其他聚合方式）
        weekly_in_aggregated = []
        weekly_out_aggregated = []
        for hour_data in weekly_hourly_in_data:
            if hour_data:
                # 这里使用平均值，你可以根据需要改为最大值、最小值、求和等
                avg_value = sum(hour_data) / len(hour_data)
                weekly_in_aggregated.append(round(avg_value, 2))
            else:
                weekly_in_aggregated.append(0)

        for hour_data in weekly_hourly_out_data:
            if hour_data:
                avg_value = sum(hour_data) / len(hour_data)
                weekly_out_aggregated.append(round(avg_value), 2)
            else:
                weekly_out_aggregated.append(0)
        
        # 存储周聚合数据
        week_in_key = f"{merchant_name}:week_in:{current_time.strftime('%Y-%W')}"
        week_out_key = f"{merchant_name}:week_out:{current_time.strftime('%Y-%W')}"
        redis_util.setex(week_in_key, 3600 * 24 * 8, json.dumps({
            "timestamp": current_time.isoformat(),
            "data": weekly_in_aggregated,
            "week_start": start_of_week.strftime("%Y-%m-%d")
        }))
        redis_util.setex(week_out_key, 3600 * 24 * 8, json.dumps({
            "timestamp": current_time.isoformat(),
            "data": weekly_out_aggregated,
            "week_start": start_of_week.strftime("%Y-%m-%d")
        }))
        
        print(f"周聚合数据已计算: [{week_in_key}]、[{week_out_key}]")
        
    except Exception as e:
        print(f"计算周聚合失败: {e}")

def _calculate_monthly_aggregation(merchant_name, current_time):
    """计算本月的小时数据聚合"""
    try:
        # 获取本月的第一天
        first_day_of_month = current_time.replace(day=1)
        
        # 获取本月的天数
        if current_time.month == 12:
            next_month = current_time.replace(year=current_time.year + 1, month=1, day=1)
        else:
            next_month = current_time.replace(month=current_time.month + 1, day=1)
        
        days_in_month = (next_month - first_day_of_month).days
        
        monthly_in_data = [[] for _ in range(24)]  # 24小时，每个小时一个列表
        monthly_out_data = [[] for _ in range(24)]
        
        # 遍历本月的每一天
        for day_offset in range(days_in_month):
            current_date = first_day_of_month + timedelta(days=day_offset)
            # 如果日期超过今天，则停止
            if current_date > current_time:
                break
                
            date_str = current_date.strftime("%Y-%m-%d")
            
            # 获取当天的24小时数据
            daily_in_data, daily_out_data = get_daily_hourly_data(merchant_name, date_str)
            
            # 将每个小时的数据添加到对应的聚合列表中
            for hour in range(24):
                monthly_in_data[hour].append(daily_in_data[hour])
                monthly_out_data[hour].append(daily_out_data[hour])
        
        # 计算每个小时的平均值
        monthly_in_aggregated = []
        monthly_out_aggregated = []
        for hour_data in monthly_in_data:
            if hour_data:
                avg_value = sum(hour_data) / len(hour_data)
                monthly_in_aggregated.append(round(avg_value, 2))
            else:
                monthly_in_aggregated.append(0)

        for hour_data in monthly_out_data:
            if hour_data:
                avg_value = sum(hour_data) / len(hour_data)
                monthly_out_aggregated.append(round(avg_value, 2))
            else:
                monthly_out_aggregated.append(0)
        
        # 存储月聚合数据
        month_in_key = f"{merchant_name}:month_in:{current_time.strftime('%Y-%m')}"
        month_out_key = f"{merchant_name}:month_out:{current_time.strftime('%Y-%m')}"
        
        redis_util.setex(month_in_key, 3600 * 24 * 32, json.dumps({
            "timestamp": current_time.isoformat(),
            "data": monthly_in_aggregated,
            "month": current_time.strftime("%Y-%m"),
            "days_count": len([d for d in monthly_in_data[0] if d])  # 实际有数据的天数
        }))

        redis_util.setex(month_out_key, 3600 * 24 * 32, json.dumps({
            "timestamp": current_time.isoformat(),
            "data": monthly_out_aggregated,
            "month": current_time.strftime("%Y-%m"),
            "days_count": len([d for d in monthly_in_data[0] if d])  # 实际有数据的天数
        }))
        
        print(f"月聚合数据已计算: [{month_in_key}][{month_out_key}]")
        
    except Exception as e:
        print(f"计算月聚合失败: {e}")