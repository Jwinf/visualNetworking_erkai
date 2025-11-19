from util.data_process_utils import compact, get_point_x_list_by_state, find_monotonic_sequence, is_point_above_line_vector, is_point_below_line_vector
from const.monotonic_type_enum import Monotonic
from entity.door import Door
from entity.statistic import Flow
from app.extensions import redis_util
from const.redis_key import IN_NUM, OUT_NUM, SERIAL_ID_MAP, DOOR_STATE

def counter(feature_map, door, flow):
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
        op_list = get_point_x_list_by_state(feature_map, track_id, door.state)
        start_index, end_index, monotonic_type = find_monotonic_sequence(op_list)
        while end_index < len(op_list) - 1:
            frame = feature_map[track_id][op_list[end_index][1]]
            match door.state:
                case 0:
                    if monotonic_type == Monotonic.INCREASING and is_point_below_line_vector(frame[0][0], frame[0][1], door.x1, door.y1, door.x2, door.y2):
                        # 进门数+1
                        flow.in_num += 1
                    elif monotonic_type == Monotonic.DECREASING and is_point_above_line_vector(frame[2][0], frame[2][1], door.x1, door.y1, door.x2, door.y2):
                        # 出门数+1
                        flow.out_num += 1
                case 1:
                    if monotonic_type == Monotonic.INCREASING and is_point_below_line_vector(frame[0][0], frame[0][1], door.x1, door.y1, door.x2, door.y2):
                        # 出门数+1
                        flow.out_num += 1
                    elif monotonic_type == Monotonic.DECREASING and is_point_above_line_vector(frame[2][0], frame[2][1], door.x1, door.y1, door.x2, door.y2):
                        # 进门数+1
                        flow.in_num += 1
                case 2:
                    if monotonic_type == Monotonic.INCREASING and is_point_above_line_vector(frame[3][0], frame[3][1], door.x1, door.y1, door.x2, door.y2):
                        # 进门数+1
                        flow.in_num += 1
                    elif monotonic_type == Monotonic.DECREASING and is_point_below_line_vector(frame[1][0], frame[1][1], door.x1, door.y1, door.x2, door.y2):
                        # 出门数+1
                        flow.out_num += 1
                case 3:
                    if monotonic_type == Monotonic.INCREASING and is_point_above_line_vector(frame[3][0], frame[3][1], door.x1, door.y1, door.x2, door.y2):
                        # 出门数+1
                        flow.out_num += 1
                    elif monotonic_type == Monotonic.DECREASING and is_point_below_line_vector(frame[1][0], frame[1][1], door.x1, door.y1, door.x2, door.y2):
                        # 进门数+1
                        flow.in_num += 1
            start_index, end_index, monotonic_type = find_monotonic_sequence(op_list, end_index + 1)

        redis_util.set(f'{door.merchant_name}:current:{IN_NUM}', flow.in_num)
        redis_util.set(f'{door.merchant_name}:current:{OUT_NUM}', flow.out_num)

        

        

def execute(serial_id):
     # 读取门配置
    merchant_name = redis_util.hget(SERIAL_ID_MAP, serial_id)
    if merchant_name == None:
        print('商户不存在，请先配置商户')
        return
    
    data = redis_util.hget_all(f'{merchant_name}:{DOOR_STATE}')
    door = Door(data['x1'], data['y1'], data['x2'], data['y2'], data['state'], merchant_name)
    
    flow = Flow()
    # 执行转换

    input_file = './data/virtual_data.json'
    output_file = './data/compacted_data.json'
    result = compact(input_file, output_file)
    counter(result, door, flow)