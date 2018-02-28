import logging
import datetime

from flask import request, jsonify


def log_api_call(func):
    """
    function:   log_api_call
    params:     function this decorator is decorating.
    returns:    function that being wrapped.  The inner wrapped function is optionally logging
                api calls and returns the result of the function being wrapped.
    notes:      This decorator function may be applied to any flask api call.  The idea is
                that if a "Apitrace" header value is supplied, then this can be output
                to a log.  This is useful for clients using multiple micro services and want
                to trace transactions through all of them.
                Currently using the default flask log.  Could be easily augmented to log
                to centralized syslog, RabbitMQ, or any other mechanism.

    examples:
              -- The code

              @app.route('/ndimensionaltictactoe/foo', methods=['GET'])
              @log_api_call
              def ndimensionaltictactoe_foo_api():
                   do something interesting...

              -- The client
              curl -H "Apitrace: 1232345346" http://localhost:5000/ndimensionaltictactoe/foo

              -- Output to logs:
              API CALL: ndimensionaltictactoe_foo_api TRACE: 1232345346
    """

    def log_api_call_wrapper(*args, **kwargs):
        if 'Apitrace' in request.headers and request.headers['Apitrace'] is not None:
            log = logging.getLogger('werkzeug')
            log.info("%s | API CALL: %s TRACE: %s " % (
            str(datetime.datetime.now()), func.__name__, request.headers['Apitrace']))
        return func(*args, **kwargs)

    return log_api_call_wrapper


def notify_error(msg, status_code):
    """
    function:   notify_error
    params:     msg - message to send back to the client.
                status_code - http status code to send to the client.
    returns:    flask response object suitable for return to the client.  Will have an
                "error" key with the message from our caller.
    notes:      Common status codes for client side problems:
                https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error
                Common status codes for server side problems:
                https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_Server_Error
    examples:

    if 'count' not in request.args:
        return notify_error("'count' argument required to /ndimensionaltictactoe/api", 403)

    """
    resp = jsonify(error=str(msg))
    resp.status_code = status_code
    return resp
