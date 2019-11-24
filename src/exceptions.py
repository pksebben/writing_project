class CreateError(Exception):
    pass

class UserExistsError(CreateError):
    pass

class AuthError(Exception):
    pass

class IncorrectPasswordErr(AuthError):
    pass
