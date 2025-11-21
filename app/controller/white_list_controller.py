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
    return jsonify({
        "status": "success",
        "message": "白名单删除成功"
    })

    
    


@white_list_controller.route('/whitelist', methods=['GET', 'POST', 'PUT', 'DELETE'])
def whitelist_management():
    try:
        if request.method == 'GET':
            # 获取白名单列表
            serial_id = request.args.get('serial_id', 'default')
            
            # 从Redis获取白名单track_id集合
            white_list_key = f"{serial_id}:white_list"
            track_ids = redis_client.smembers(white_list_key)
            
            # 从Redis获取白名单图片信息
            white_list_image_key = f"{serial_id}:white_list_image"
            whitelist_data = []
            
            for track_id in track_ids:
                image_data = redis_client.hget(white_list_image_key, track_id)
                if image_data:
                    whitelist_data.append({
                        "track_id": track_id,
                        "image": image_data
                    })
            
            return jsonify({
                "status": "success",
                "data": whitelist_data
            })
            
        elif request.method == 'POST':
            # 添加白名单
            data = request.get_json()
            
            if 'track_id' not in data or 'serial_id' not in data:
                return jsonify({
                    "status": "error",
                    "message": "缺少track_id或serial_id字段"
                }), 400
            
            track_id = data['track_id']
            serial_id = data['serial_id']
            image_data = data.get('image', '')
            
            # 检查是否已存在
            white_list_key = f"{serial_id}:white_list"
            if redis_client.sismember(white_list_key, track_id):
                return jsonify({
                    "status": "error",
                    "message": "该track_id已存在"
                }), 400
            
            # 添加到Redis集合
            redis_client.sadd(white_list_key, track_id)
            
            # 添加到Redis哈希表
            if image_data:
                white_list_image_key = f"{serial_id}:white_list_image"
                redis_client.hset(white_list_image_key, track_id, image_data)
            
            return jsonify({
                "status": "success",
                "message": "白名单添加成功",
                "data": {
                    "track_id": track_id,
                    "image": image_data
                }
            })
            
        elif request.method == 'PUT':
            # 更新白名单
            data = request.get_json()
            
            if 'track_id' not in data or 'new_track_id' not in data or 'serial_id' not in data:
                return jsonify({
                    "status": "error",
                    "message": "缺少必需字段"
                }), 400
            
            track_id = data['track_id']
            new_track_id = data['new_track_id']
            serial_id = data['serial_id']
            image_data = data.get('image', None)
            
            # 检查原track_id是否存在
            white_list_key = f"{serial_id}:white_list"
            if not redis_client.sismember(white_list_key, track_id):
                return jsonify({
                    "status": "error",
                    "message": "未找到指定的track_id"
                }), 404
            
            # 检查新track_id是否已存在（如果不同）
            if track_id != new_track_id and redis_client.sismember(white_list_key, new_track_id):
                return jsonify({
                    "status": "error",
                    "message": "新track_id已存在"
                }), 400
            
            # 更新Redis集合
            if track_id != new_track_id:
                redis_client.srem(white_list_key, track_id)
                redis_client.sadd(white_list_key, new_track_id)
            
            # 更新Redis哈希表
            white_list_image_key = f"{serial_id}:white_list_image"
            if image_data is not None:
                # 如果提供了新图片，更新图片
                redis_client.hset(white_list_image_key, new_track_id, image_data)
            elif track_id != new_track_id:
                # 如果只是修改track_id，复制图片数据
                old_image = redis_client.hget(white_list_image_key, track_id)
                if old_image:
                    redis_client.hset(white_list_image_key, new_track_id, old_image)
                    redis_client.hdel(white_list_image_key, track_id)
            
            return jsonify({
                "status": "success",
                "message": "白名单更新成功"
            })
            
        elif request.method == 'DELETE':
            # 删除白名单
            track_id = request.args.get('track_id')
            serial_id = request.args.get('serial_id', 'default')
            
            if not track_id:
                return jsonify({
                    "status": "error",
                    "message": "缺少track_id参数"
                }), 400
            
            # 检查是否存在
            white_list_key = f"{serial_id}:white_list"
            if not redis_client.sismember(white_list_key, track_id):
                return jsonify({
                    "status": "error",
                    "message": "未找到指定的track_id"
                }), 404
            
            # 从Redis集合中删除
            redis_client.srem(white_list_key, track_id)
            
            # 从Redis哈希表中删除图片
            white_list_image_key = f"{serial_id}:white_list_image"
            redis_client.hdel(white_list_image_key, track_id)
            
            return jsonify({
                "status": "success",
                "message": "白名单删除成功"
            })
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"服务器错误: {str(e)}"
        }), 500
