import json
import ast


def process_exception(get_response):
    def middelware(request):
        response = get_response(request)
        try:

            body = None
            error_message = None
            if response.status_code is 200:
                body = ast.literal_eval(response.content.decode('UTF-8'))
            else:
                d = dict(ast.literal_eval(response.content.decode('UTF-8')))
                for i in d.keys():
                    error_message = {
                        "message": (d.get(i)[0])
                    }

            custom_container = {
                "status": response.status_code,
                "result": body,
                "error": error_message
            }

            print(response.content.decode('UTF-8'))

            response.content = str(json.dumps(custom_container)).encode('UTF-8')

            return response
        except:
            return response

    return middelware
