from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'error': exc.detail}
        response.data = data
    return response
