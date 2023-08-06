import json


class Response(object):
    """
    http response content
    """

    def __init__(self, http_code, actual_response):
        self.http_code = http_code
        self.actual_response = actual_response

    def to_string(self):
        return '{"http_code":' + str(self.http_code) + ',"actual_response":' + json.dumps(
            self.actual_response) + '}'
