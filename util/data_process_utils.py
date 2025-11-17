import json
from collections import defaultdict
from const.colors_enum import Colors
from const.monotonic_type_enum import Monotonic

def compact(input_file, output_file):
    """
    将JSON数据从 {reid: "001", box: []} 格式转换为 {"reid": [box]} 格式
    
    Args:
        input_file: 输入JSON文件路径
        output_file: 输出JSON文件路径
    """
    try:
        # 读取原始JSON文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 使用defaultdict自动处理重复的reid
        result = defaultdict(list)
        
        # 检查数据格式并处理
        if isinstance(data, list):
            # 如果数据是列表形式
            for item in data:
                if 'reid' in item and 'box' in item:
                    reid = item['reid']
                    box = item['box']
                    result[reid].append(box)
                else:
                    print(f"{Colors.YELLOW.value}警告: 跳过格式不正确的数据项: {item}{Colors.END.value}")
        else:
            print("错误: 不支持的JSON格式")
            return
        
        # 将defaultdict转换为普通dict
        result_dict = dict(result)
        
        # 保存转换后的数据
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, ensure_ascii=False, indent=2)
        
        print(f"{Colors.GREEN.value}转换完成!{Colors.END.value} 输入文件: {input_file} -> 输出文件: {output_file}")
        print(f"处理了 {len(result_dict)} 个不同的reid")
        
        return result_dict
        
    except FileNotFoundError:
        print(f"{Colors.RED.value}错误: 文件 {input_file} 不存在{Colors.END.value}")
    except json.JSONDecodeError:
        print(f"{Colors.RED.value}错误: 文件 {input_file} 不是有效的JSON格式{Colors.END.value}")
    except Exception as e:
        print(f"{Colors.RED.value}错误: {str(e)}{Colors.END.value}")


def get_point_x_list_by_state(feature_map, track_id, state=0):
    
    """
    param: feature_map 数据字典<track_id, seq>; state 场景状态[0,3]
    state=0或1，获取p1横坐标列表；
    state=2或3，获取p2横坐标列表
    return 返回识别框指定点横坐标列表
    """
    op_seq = []
    match state:
        case 0 | 1:
            for f_index, frame in enumerate(feature_map[track_id]):
                if len(frame) > 0 and len(frame[0]) > 0:
                    op_seq.append([frame[0][0], f_index])
        
        case 2 | 3:
            for f_index, frame in enumerate(feature_map[track_id]):
                if len(frame) > 1 and len(frame[1]) > 0:
                    op_seq.append([frame[1][0], f_index])
        case _:
            print(f"{Colors.RED}{Colors.BOLD}Error: state code error, please input the right state code [0,3].{Colors.END}")
            return
    
    return op_seq

def find_monotonic_sequence(sequence, start_index=0):
    """
    在整数序列中查找从指定位置开始的第一个单调序列
    
    参数:
        sequence: 整数列表
        start_index: 开始查找的索引位置
    
    返回:
        tuple: (start, end, monotonic_type)
        - start: 单调序列的起始索引
        - end: 单调序列的结束索引  
        - monotonic_type: 单调类型 ('increasing', 'decreasing', 'equal', 'none')
    """
    n = len(sequence)
    
    # 处理边界情况
    if n == 0:
        return -1, -1, Monotonic.NONE
    
    if start_index >= n:
        return -1, -1, Monotonic.NONE
    
    # 如果从起始位置开始只剩一个元素
    if start_index == n - 1:
        return start_index, start_index, Monotonic.EQUAL
    
    # 检查单调性
    current_start = start_index
    
    # 检查前两个元素的关系来确定初始单调性
    if sequence[start_index][0] < sequence[start_index + 1][0]:
        monotonic_type = Monotonic.INCREASING
    elif sequence[start_index][0] > sequence[start_index + 1][0]:
        monotonic_type = Monotonic.DECREASING
    else:
        monotonic_type = Monotonic.EQUAL
    
    # 从第三个元素开始继续检查
    i = start_index + 2
    while i < n:
        if monotonic_type == Monotonic.INCREASING:
            if sequence[i][0] >= sequence[i - 1][0]:
                # 继续保持递增
                pass
            else:
                # 单调性改变，结束当前序列
                break
        elif monotonic_type == Monotonic.DECREASING:
            if sequence[i][0] <= sequence[i - 1][0]:
                # 继续保持递减
                pass
            else:
                # 单调性改变，结束当前序列
                break
        elif monotonic_type == Monotonic.EQUAL:
            if sequence[i][0] > sequence[i - 1][0]:
                monotonic_type = Monotonic.INCREASING
            elif sequence[i][0] < sequence[i - 1][0]:
                monotonic_type = Monotonic.DECREASING
            # 如果继续相等，保持 'equal'
        
        i += 1
    
    # 返回结果
    end_index = i - 1
    
    return current_start, end_index, monotonic_type

def is_point_above_line_vector(x1, y1, x2, y2, x3, y3, tolerance=1e-10):
    """
    使用向量叉积判断点是否在线段上方或线上
    点的坐标（x1, y1）
    门的两个端点(x2, y2), (x3, y3)
    """
    # 计算向量叉积
    cross_product = (x3 - x2) * (y1 - y2) - (y3 - y2) * (x1 - x2)
    
    # 如果叉积 >= 0，点在线上或上方（对于标准的数学坐标系）
    # 注意：在计算机图形学中，y轴通常是向下的，所以符号可能需要调整
    return cross_product >= -tolerance


def is_point_below_line_vector(x1, y1, x2, y2, x3, y3, tolerance=1e-10):
    """
    使用向量叉积判断点是否在线段下方或线上
    点的坐标（x1, y1）
    门的两个端点(x2, y2), (x3, y3)
    """
    # 计算向量叉积
    cross_product = (x3 - x2) * (y1 - y2) - (y3 - y2) * (x1 - x2)
    return cross_product <= -tolerance