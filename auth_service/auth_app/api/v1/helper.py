from flask import jsonify

def send_result(data=None, message='OK', code=200, status='success'):
    message_dict = {
        'message' : message,
        'status' : status
    }

    res = {
        'code' : code,
        'data' : data,
        'message' : message_dict
    }

    return jsonify(res), code

def send_error(data=None, message='ERROR', code=400, status='error'):
    message_dict = {
        'message' : message,
        'status' : status
    }

    res = {
        'code' : code,
        'data' : data,
        'message' : message_dict
    }

    return jsonify(res), code

    