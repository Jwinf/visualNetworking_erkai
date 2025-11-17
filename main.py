from util.data_process_utils import compact, get_point_x_list_by_state, find_monotonic_sequence
from const.colors_enum import Colors

RED = '\033[91m'
GREEN = '\033[92m'

def banner():
    with open('./favicon.txt', 'r') as f:
        print(f.read())

def counter(feature_map, state=0):
    """
    param: feature_map 数据字典<track_id, seq>; state 场景状态[0,3]
    情况1：判断p1横坐标单调性，p1递增且p1位于门下方为进门；
          p1递减且p3位于门上方为出门。state = 0
    情况2：判断p1横坐标单调性，p1递增且p1位于门下方为出门；
          p1递减且p3位于门上方为进门。 state = 1
    情况3：判断p横2坐标的单调性，p2递增且p4位于门上方为进门；
          p2递减且p2位于门下方为出门。 state = 2
    情况4：判断p2横坐标的单调性，p2递增且p4位于门上方为出门
          p2递减且p2位于门下方为进门。 state = 3
    """
    for track_id in feature_map:
        op_list = get_point_x_list_by_state(feature_map, track_id, state)
        start_index, end_index, monotonic_type = find_monotonic_sequence(op_list)
        while end_index < len(op_list) - 1:
            match state:
                case 0:
                    pass
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass

if __name__ == '__main__':
    banner()
    
    input_file = "virtual_data.json"
    output_file = "compacted_data.json"
    
    # 执行转换
    result = compact(input_file, output_file)