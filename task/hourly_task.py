import schedule
import threading
import time
from datetime import datetime
from task.data_aggregation_task import store_hourly_data


def hourly_task(merchant_name):
    """每小时执行的任务"""
    try:
        print(f"[{datetime.now()}] 执行每小时数据存储")
        store_hourly_data(merchant_name)
    except Exception as e:
        print(f"每小时任务执行失败: {e}")

def schedule_thread(merchant_name):
    """定时任务调度线程"""
    # 每小时执行一次
    schedule.every().hour.at(":00").do(hourly_task, merchant_name)
    
    # 立即执行一次
    hourly_task(merchant_name)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次