from flask import Blueprint, request, jsonify
from const.colors_enum import Colors

counter_bp = Blueprint('counter', __name__)

@counter_bp.route('/set', methods=['POST'])
def set_state():
    try:
        # 获取前端发送的JSON数据
        data = request.get_json()
        
        # 检查数据是否为空
        if not data:
            return jsonify({'error': 'No data received'}), 400
      # 提取字段
        x1 = data.get('x1')
        y1 = data.get('y1')
        x2 = data.get('x2')
        y2 = data.get('y2')
        state = data.get('state')
        
        # 打印接收到的数据（用于调试）
        print(f"{Colors.GREEN.value}Received data: x1={x1}, y1={y1}, x2={x2}, y2={y2}, state={state}{Colors.END.value}")   
        # 业务逻辑处理
        
        # 返回成功响应
        return jsonify({
            'status': 'success',
            'message': 'Parameter set successed!',
            'received_data': data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500