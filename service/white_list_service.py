from app.extensions import redis_util
from const.redis_key import WHITE_LIST, TRACK_ID_IMAGE

def white_list_get(serial_id):
    # 从Redis获取白名单track_id集合
    white_list_key = f"{serial_id}:{WHITE_LIST}"
    track_ids = redis_util.smembers(white_list_key)
    
    # 从Redis获取白名单图片信息
    white_list_image_key = f"{serial_id}:{TRACK_ID_IMAGE}"
    whitelist_data = []
    
    for track_id in track_ids:
        image_data = redis_util.hget(white_list_image_key, track_id)
        if image_data:
            whitelist_data.append({
                "track_id": track_id,
                "image": image_data
            })
    return whitelist_data

def white_list_add(data):
    track_id = data['track_id']
    serial_id = data['serial_id']
    image_data = data.get('image', '')
    
    # 检查是否已存在
    white_list_key = f"{serial_id}:{WHITE_LIST}"
    if redis_util.sismember(white_list_key, track_id):
        return {
            "status": "error",
            "message": "该track_id已存在"
        }, 400
    
    # 添加到Redis集合
    redis_util.sadd(white_list_key, track_id)
    
    # 添加到Redis哈希表
    if image_data:
        white_list_image_key = f"{serial_id}:{WHITE_LIST}"
        redis_util.hset(white_list_image_key, track_id, image_data)
    
    return {
        "status": "success",
        "message": "添加成功!"
    }, 200

def white_list_edit(data):
    # 更新白名单
    track_id = data['track_id']
    serial_id = data['serial_id']
    image_data = data.get('image', None)
    
    # 检查原track_id是否存在
    white_list_key = f"{serial_id}:{WHITE_LIST}"
    if not redis_util.sismember(white_list_key, track_id):
        return {
            "status": "error",
            "message": "未找到指定的track_id"
        }, 404
    
    
    # 更新Redis哈希表
    white_list_image_key = f"{serial_id}:{TRACK_ID_IMAGE}"
    if image_data is not None:
        # 如果提供了新图片，更新图片
        redis_util.hset(white_list_image_key, track_id, image_data)
    
    return {
        "status": "success",
        "message": "白名单更新成功"
    }
    
def white_list_delete(serial_id, track_id):
    white_list_key = f"{serial_id}:{WHITE_LIST}"
    if not redis_util.sismember(white_list_key, track_id):
        return {
            "status": "error",
            "message": "未找到指定的track_id"
        }, 404
    
    # 从Redis集合中删除
    redis_util.srem(white_list_key, track_id)
    
    # 从Redis哈希表中删除图片
    white_list_image_key = f"{serial_id}:white_list_image"
    redis_util.hdel(white_list_image_key, track_id)