from flask import Blueprint, request, jsonify
import json
from datetime import datetime
from service.data_source_service import get_daily_statistics, get_range_statistics
from app.extensions import redis_util
from const.redis_key import SERIAL_ID_MAP

data_source_controller = Blueprint('data_source', __name__)


@data_source_controller.route('/dashboard/stats', methods=['GET'])
def statistics():
    serial_id = request.args.get("period", "000")
    merchant_name = redis_util.hget(SERIAL_ID_MAP, serial_id)
    if merchant_name is None:
        return jsonify({
            "code": 403,
            "message": "请先配置商户",
            "data": None
        })
    period = request.args.get("period", "day")
    match period:
        case 'day':
            result = get_daily_statistics(serial_id)
        case "week" | 'month':
            result = get_range_statistics(serial_id, period)
    return jsonify({
            "code": 200,
            "message": "success",
            "data": result
        })
