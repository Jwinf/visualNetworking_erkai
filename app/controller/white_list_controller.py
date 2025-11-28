# 白名单管理接口
from flask import Blueprint, request, jsonify
import json
from service.white_list_service import white_list_get, white_list_add, white_list_edit, white_list_delete

white_list_controller = Blueprint('door', __name__)

@white_list_controller.route('/whitelist', methods=['GET'])
def get_whilte_list_by_serial_id():
    serial_id = request.args.get('serial_id', 000)
    white_list_data = white_list_get(serial_id)
    return jsonify({
        "status": "success",
        "data": white_list_data
    }), 200

@white_list_controller.route('/whitelist', methods=['POST'])
def add_white_list_by_serial_id():
    data = request.get_json()
    if 'track_id' not in data or 'serial_id' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少track_id或serial_id字段"
        }), 400
    result, code = white_list_add(data)
    return jsonify(result), code

@white_list_controller.route('/whitelist', mehtods=['PUT'])
def update_white_list_by_serial_id():
    data = request.get_json()
    if 'track_id' not in data or 'serial_id' not in data:
        return jsonify({
            "status": "error",
            "message": "缺少track_id或serial_id字段"
        }), 400
    result, code = white_list_edit(data)
    return jsonify(request), code

@white_list_controller.route('/white_list', methods=['DELETE'])
def delete_white_list_by_serial_id():
     # 删除白名单
    track_id = request.args.get('track_id')
    serial_id = request.args.get('serial_id', 'default')
    if not track_id or not serial_id:
        return jsonify({
            "status": "error",
            "message": "缺少track_id参数或serial_id字段"
        }), 400
    result, code = white_list_delete(serial_id, track_id)
    return jsonify(result), code
