from data_process_utils import compact

def banner():
    with open('./favicon.txt', 'r') as f:
        print(f.read())

def counter():
    """
    情况1：判断p1横坐标单调性，p1递增且p1位于门下方为进门；
          p1递减且p3位于门上方为出门。
    情况2：判断p1横坐标单调性，p1递增且p1位于门下方为出门；
          p1递减且p3位于门上方为进门
    情况3：判断p横2坐标的单调性，p2递增且p4位于门上方为进门；
          p2递减且p2位于门下方为出门
    情况4：判断p2横坐标的单调性，p2递增且p4位于门上方为出门
          p2递减且p2位于门下方为进门
        
    """

if __name__ == '__main__':
    banner()
    
    input_file = "virtual_data.json"
    output_file = "compacted_data.json"
    
    # 执行转换
    result = compact(input_file, output_file)
    