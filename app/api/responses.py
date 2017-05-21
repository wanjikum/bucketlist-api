from flask import jsonify

# define a blue print of a response that contains error(s)


def error_response(validation_errors=None,
                   message='Please correct the identified errors, \
                   for correct output',
                   status=400,
                   error='Bad request'):

    # A blue print of a response that contains validation error(s)
    if validation_errors:
        response = jsonify(
            {'status': status,
             'error': error,
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

# define a blue print of a response that is successful


def success_response(message, status=200, added=None, modified=None):

    # if you add something successfully
    if added:
        response = jsonify(
            {'status': status,
             'message': message,
             'added': added}
        )

    # if you modify something successfully
    elif modified:
        response = jsonify(
            {'status': status,
             'message': message,
             'modified': modified}
        )

    else:
        response = jsonify(
            {'status': status,
             'message': message}
        )

    response.status_code = status
    return response
