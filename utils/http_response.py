def format_response_success(data):
    return {
        'success': True,
        'data': data,
    }


def format_response_failure(data):
    return {
        'success': False,
        'data': data,
    }