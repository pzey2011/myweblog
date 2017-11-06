from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
class ApiResponse:
    @staticmethod
    def get_base_response(response_code=HTTP_200_OK, data=None, message=""):
        if data is None:
            data = {}

        if message:
            data['message'] = message
        response = {
            "status": response_code,
            "errors": {
                "general_errors": [
                ],
                "form_errors": {
                }
            },
            "data": data
        }

        return response

    @staticmethod
    def get_fail_response(response_code=HTTP_400_BAD_REQUEST, general_errors=None, form_errors=None):
        if form_errors is None:
            form_errors = {}
        if general_errors is None:
            general_errors = []
        response = ApiResponse.get_base_response(response_code)
        if not isinstance(general_errors, list):
            general_errors = [general_errors]
        response['errors']['general_errors'] = general_errors
        response['errors']['form_errors'] = form_errors

        return response