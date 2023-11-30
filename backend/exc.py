class ApplicationBaseException(Exception):
    def __init__(self, err_msg: str, status_code: int):
        self.err_msg = str
        self.status_code = status_code

        super().__init__(err_msg)


class IncorrectAuthenticationCredentialsException(ApplicationBaseException):
    def __init__(self, err_msg="Incorrect credentials provided"):
        self.status_code = 401
        super().__init__(err_msg, status_code=401)


class ExpiredUserSessionExcpetion(BaseException):
    def __init__(self, err_msg="Expired session"):
        self.status_code = 440
        super().__init__(err_msg, status_code=440)
