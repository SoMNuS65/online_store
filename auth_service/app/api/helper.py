from flask import jsonify

def send_error(data=None, message="Error", code=400, status="error"):
    message_to_dict = {
        "text" : message,
        "status" : status,
    }

    res = {
        "message" : message_to_dict,
        "code" : code,
        "data" : data
    }
    return jsonify(res), code

def send_result(data=None, message="OK", code=200, status="success"):
    message_to_dict = {
        "text" : message,
        "status" : status,
    }

    res = {
        "message" : message_to_dict,
        "code" : code,
        "data" : data
    }
    return jsonify(res), code

def json_parse(json_req):

    json_body = {}
    for key, value in json_req.items():
        if isinstance(value, str):
            json_body.setdefault(key, value.strip())
        else:
            json_body.setdefault(key, value)
            
    return json_body