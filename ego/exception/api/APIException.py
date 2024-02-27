from flask import json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = "sorry, we make a mistake"
    error = 500

    def __init__(self, msg=None, error=None, code=None, header=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if error:
            self.code = error
        if error:
            self.error = error
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        body = dict(
            msg=self.msg,
            code=self.code
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None, scope=None):
        return [("Content-Type", "application/json")]
