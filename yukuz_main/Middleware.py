import json
import ast


def process_exception(get_response):
    def middleware(request):
        print(request.path)
        response = get_response(request)
        try:

            body = None
            error_message = None
            if 200 <= response.status_code <= 299:
                body = response.data

            else:
                d = response.data
                for i in d.keys():
                    error_message = {
                        "message": (d.get(i)[0])
                    }

            if response.status_code == 401:
                error_message = {
                    "message": "Not authenticated user"
                }

            custom_container = {
                "status": response.status_code,
                "result": body,
                "error": error_message
            }

            response.content = str(json.dumps(custom_container))

            return response
        except Exception as error:
            print(error)
            return response

    return middleware
