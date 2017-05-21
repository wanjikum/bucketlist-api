from flask import jsonify


def error_response(validation_errors=None,
                   message='Please correct the identified errors, \
                   for correct output',
                   status=400,
                   error='Bad request'):

    if validation_errors:
        response = jsonify(
            {'status': status, 'error': error,
             'validation_errors': validation_errors,
             'message': message}
        )

    else:
        response = jsonify(
            {'status': status, 'error': error,
             'message': message}
        )

    response.status_code = status
    return response
