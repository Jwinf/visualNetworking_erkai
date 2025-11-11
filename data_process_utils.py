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