from flask import make_response, jsonify

def response(status_code, message=None):
    body = {
        'status': status_code
    }
    if message:
        body['message'] = message

    return make_response(jsonify(body), status_code)

def not_found(message=None):
    return response(404, message)

def no_content(message=None):
    return response(204, message)