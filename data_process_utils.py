import json
from collections import defaultdict

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
                    print(f"警告: 跳过格式不正确的数据项: {item}")
        else:
            print("错误: 不支持的JSON格式")
            return
        
        # 将defaultdict转换为普通dict
        result_dict = dict(result)
        
        # 保存转换后的数据
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, ensure_ascii=False, indent=2)
        
        print(f"转换完成! 输入文件: {input_file} -> 输出文件: {output_file}")
        print(f"处理了 {len(result_dict)} 个不同的reid")
        
        return result_dict
        
    except FileNotFoundError:
        print(f"错误: 文件 {input_file} 不存在")
    except json.JSONDecodeError:
        print(f"错误: 文件 {input_file} 不是有效的JSON格式")
    except Exception as e:
        print(f"错误: {str(e)}")

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
        return -1, -1, 'none'
    
    if start_index >= n:
        return -1, -1, 'none'
    
    # 如果从起始位置开始只剩一个元素
    if start_index == n - 1:
        return start_index, start_index, 'equal'
    
    # 检查单调性
    current_start = start_index
    
    # 检查前两个元素的关系来确定初始单调性
    if sequence[start_index] < sequence[start_index + 1]:
        monotonic_type = 'increasing'
    elif sequence[start_index] > sequence[start_index + 1]:
        monotonic_type = 'decreasing'
    else:
        monotonic_type = 'equal'
    
    # 从第三个元素开始继续检查
    i = start_index + 2
    while i < n:
        if monotonic_type == 'increasing':
            if sequence[i] >= sequence[i - 1]:
                # 继续保持递增
                pass
            else:
                # 单调性改变，结束当前序列
                break
        elif monotonic_type == 'decreasing':
            if sequence[i] <= sequence[i - 1]:
                # 继续保持递减
                pass
            else:
                # 单调性改变，结束当前序列
                break
        elif monotonic_type == 'equal':
            if sequence[i] > sequence[i - 1]:
                monotonic_type = 'increasing'
            elif sequence[i] < sequence[i - 1]:
                monotonic_type = 'decreasing'
            # 如果继续相等，保持 'equal'
        
        i += 1
    
    # 返回结果
    end_index = i - 1
    
    return current_start, end_index, monotonic_type


# 测试函数
def test_monotonic_sequence():
    """测试函数"""
    test_cases = [
        # (序列, 起始索引, 期望结果)
        ([1, 2, 3, 4, 5], 0, (0, 4, 'increasing')),      # 整个序列递增
        ([5, 4, 3, 2, 1], 0, (0, 4, 'decreasing')),      # 整个序列递减
        ([1, 1, 1, 1, 1], 0, (0, 4, 'equal')),           # 整个序列相等
        ([1, 2, 3, 2, 1], 0, (0, 2, 'increasing')),      # 先增后减
        ([5, 4, 3, 4, 5], 0, (0, 2, 'decreasing')),      # 先减后增
        ([1, 2, 2, 3, 4], 0, (0, 4, 'increasing')),      # 非严格递增
        ([], 0, (-1, -1, 'none')),                       # 空序列
        ([1], 0, (0, 0, 'equal')),                       # 单元素序列
        ([1, 2, 3, 2, 1], 2, (2, 4, 'decreasing')),      # 从中间开始
    ]
    
    print("测试 find_monotonic_sequence:")
    for i, (seq, start, expected) in enumerate(test_cases):
        result = find_monotonic_sequence(seq, start)
        status = "✓" if result == expected else "✗"
        print(f"测试 {i+1}: {status} 序列: {seq}, 起始: {start}")
        print(f"  期望: {expected}, 实际: {result}")
        print()
    


# 使用示例
if __name__ == "__main__":
    # 运行测试
    test_monotonic_sequence()
    
    print("\n" + "="*50)
    print("使用示例:")
    
    # 示例1: 基本使用
    sequence1 = [1, 2, 3, 1, 1, 1, 1, 1]
    start1, end1, type1 = find_monotonic_sequence(sequence1, 0)
    print(f"序列: {sequence1}")
    print(f"从位置0开始: 单调序列 [{start1}:{end1}] = {sequence1[start1:end1+1]}, 类型: {type1}")
    
    # 示例2: 从中间位置开始
    start2, end2, type2 = find_monotonic_sequence(sequence1, 3)
    print(f"从位置3开始: 单调序列 [{start2}:{end2}] = {sequence1[start2:end2+1]}, 类型: {type2}")
    
    # 示例3: 递减序列
    sequence2 = [5, 4, 3, 2, 1, 2, 3]
    start3, end3, type3 = find_monotonic_sequence(sequence2, 0)
    print(f"序列: {sequence2}")
    print(f"从位置0开始: 单调序列 [{start3}:{end3}] = {sequence2[start3:end3+1]}, 类型: {type3}")