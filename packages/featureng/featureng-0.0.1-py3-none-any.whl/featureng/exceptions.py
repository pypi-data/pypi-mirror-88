
class AuthError(Exception):
    def __init__(self,service):
        super().__init__(service)
        self.service = service

    def __str__(self):
        up = "_".join(self.service.upper().split(" ")) + "_KEY"
        msg = f"{self.service} key is required. Pass as argument or set environment variable '{up}'."
        return msg

class ApiRequestError(Exception):
    pass

class ApiResponseError(Exception):
    pass
