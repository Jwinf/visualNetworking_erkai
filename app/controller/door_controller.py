from flask import Blueprint, request, jsonify
from const.colors_enum import Colors
from const.redis_key import DOOR_STATE
from app.extensions import redis_util

door_controller = Blueprint('door', __name__)

@door_controller.route('/set', methods=['POST'])
def set_state():
    try:
        # 获取前端发送的JSON数据
        data = request.get_json()
        
        # 检查数据是否为空
        if not data:
            return jsonify({'error': 'No data received'}), 400
      # 提取字段
        merchant_name = data.get('merchant_name')
        x1 = data.get('x1')
        y1 = data.get('y1')
        x2 = data.get('x2')
        y2 = data.get('y2')
        state = data.get('state')
        
        # 打印接收到的数据（用于调试）
        print(f"{Colors.GREEN.value}Received data: merchant_name = {merchant_name}, x1={x1}, y1={y1}, x2={x2}, y2={y2}, state={state}{Colors.END.value}")   
        # 存入redis
        redis_util.hmset(f'{merchant_name}:{DOOR_STATE}', jsonify({
            'x1': x1,'y1': y1, 'x2': x2, 'y2': y2, 'state': state
        }))

        # 返回成功响应
        return jsonify({
            'status': 'success',
            'message': 'Parameter set successed!',
            'received_data': data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@door_controller.route('/test', methods=['GET'])   
def test():
    return redis_util.hget_all("中国电信:DOOR_STATE")