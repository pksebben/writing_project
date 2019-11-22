class CreateError(Exception):
    pass

class UserExistsError(CreateError):
    pass
