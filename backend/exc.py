class ApplicationBaseException(Exception):
    def __init__(self, err_msg: str, status_code: int):
        self.err_msg = err_msg
        self.status_code = status_code

        super().__init__(err_msg)


class BadPaginationParameter(ApplicationBaseException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg=err_msg, status_code=400)


class ObjectNotFound(ApplicationBaseException):
    def __init__(self, obj_name: str):
        super().__init__(
            err_msg=f"{obj_name} not found",
            status_code=404,
        )


class IncorrectAuthenticationCredentialsException(ApplicationBaseException):
    def __init__(self, err_msg="Incorrect credentials provided"):
        self.status_code = 401
        super().__init__(err_msg, status_code=401)


class ExpiredUserSessionExcpetion(ApplicationBaseException):
    def __init__(self, err_msg="Expired session"):
        self.status_code = 440
        super().__init__(err_msg, status_code=440)


class InvalidCollectionTemplate(ApplicationBaseException):
    def __init__(self, err_msg="Invalid collection template provided"):
        super().__init__(err_msg, 400)


class ConflictingCollectionName(ApplicationBaseException):
    def __init__(self, collection_name: str):
        err_msg = f"collection with name: {collection_name} already exists!"

        super().__init__(err_msg=err_msg, status_code=409)


class InvalidEntryContent(ApplicationBaseException):
    def __init__(self):
        super().__init__(err_msg="invalid entry content supplied", status_code=400)


class InactiveCollectionEntryAddition(ApplicationBaseException):
    def __init__(self):
        super().__init__(
            err_msg="cannot add an entry for an inactive collection", status_code=400
        )
