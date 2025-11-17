import json
import random
import os

def generate_single_box(base_x1, y_center, width, height):
    """根据给定的x1基值生成单个box数据"""
    x1 = base_x1
    y1 = y_center - height // 2
    x2 = x1 + width
    y2 = y1
    x3 = x2
    y3 = y1 + height
    x4 = x1
    y4 = y3
    
    return [
        [x1, y1],
        [x2, y2],
        [x3, y3],
        [x4, y4]
    ]

def append_to_json_with_monotonic_x1(
    filename="virtual_data.json", 
    num_reids=10, 
    boxes_per_reid=10, 
    increasing=True,
    x_step_range=(5, 20)
):
    """
    向JSON文件追加数据，同一个reid的x1具有单调性
    
    参数:
    filename: 文件名
    num_reids: reid数量
    boxes_per_reid: 每个reid的box数量
    increasing: True表示x1递增，False表示x1递减
    x_step_range: x1变化的步长范围(最小,最大)
    """
    
    # 如果文件不存在，创建空列表
    if not os.path.exists(filename):
        existing_data = []
    else:
        # 读取现有数据
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, Exception):
            # 如果文件损坏或为空，初始化为空列表
            existing_data = []
    
    # 生成新数据
    new_data = []
    for reid_index in range(num_reids):
        reid = f"person_{reid_index:03d}"
        
        # 为每个reid确定初始x1和变化步长
        initial_x1 = random.randint(100, 1500)
        x_step = random.randint(x_step_range[0], x_step_range[1])
        
        # 如果递减，步长为负
        if not increasing:
            x_step = -x_step
        
        # 为每个reid确定y中心点和尺寸范围
        y_center = random.randint(200, 800)
        width_range = (50, 200)
        height_range = (100, 300)
        
        for box_index in range(boxes_per_reid):
            # 使用临时步长变量，有5%的概率临时使用相反方向的步长
            temp_x_step = x_step
            if random.random() < 0.05:
                temp_x_step = -x_step
                print(f"注意: {reid} 的box {box_index} 临时使用反向步长!")
            
            # 计算当前x1值，使用临时步长
            current_x1 = initial_x1 + box_index * temp_x_step
            
            # 确保x1在合理范围内
            if current_x1 < 0:
                current_x1 = 0
            elif current_x1 > 1820:
                current_x1 = 1820
                
            # 随机生成宽度和高度
            width = random.randint(width_range[0], width_range[1])
            height = random.randint(height_range[0], height_range[1])
            
            # 确保box不会超出图像边界
            if current_x1 + width > 1920:
                width = 1920 - current_x1
                
            if y_center - height // 2 < 0:
                height = y_center * 2
            elif y_center + height // 2 > 1080:
                height = (1080 - y_center) * 2
            
            box_data = {
                "reid": reid,
                "box": generate_single_box(current_x1, y_center, width, height)
            }
            new_data.append(box_data)
    
    # 合并数据
    combined_data = existing_data + new_data
    
    # 写回文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)
    
    print(f"已向 {filename} 追加 {len(new_data)} 条数据")
    print(f"文件现在共有 {len(combined_data)} 条数据")
    print(f"初始单调性: {'递增' if increasing else '递减'}")
    
    return new_data

# 示例用法
if __name__ == "__main__":
    # 第一次运行：创建文件并添加递增数据
    print("第一次运行：创建文件并添加x1递增的数据")
    new_data = append_to_json_with_monotonic_x1(
        "virtual_data.json", 
        num_reids=20, 
        boxes_per_reid=50, 
        increasing=True,
        x_step_range=(5, 15)
    )
    
    # 打印前几条新数据作为示例
    print("\n新添加的数据示例（前3条）：")
    for i, item in enumerate(new_data[:3]):
        print(f"{i+1}. {json.dumps(item, ensure_ascii=False)}")
    
    # 第二次运行：追加递减数据
    print("\n" + "="*50)
    print("第二次运行：追加x1递减的数据")
    new_data = append_to_json_with_monotonic_x1(
        "virtual_data.json", 
        num_reids=20, 
        boxes_per_reid=50, 
        increasing=False,
        x_step_range=(5, 15)
    )