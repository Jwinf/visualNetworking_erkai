from flask import Blueprint, request, jsonify
import json
from datetime import datetime
from service.door_service import set

door_controller = Blueprint('door', __name__)

@door_controller.route('/set', methods=['POST'])
def set_state():
    try:
        # 获取前端发送的JSON数据
        data = json.loads(request.get_json())
        if not data:
            return jsonify({'error': 'No data received'}), 400
        set(data)
        # 返回成功响应
        return jsonify({
            'status': 'success',
            'message': 'Parameter set successed!',
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@door_controller.route('/test', methods=['GET'])   
def test():
    print(datetime.now().strftime("%Y-%m-%d"))