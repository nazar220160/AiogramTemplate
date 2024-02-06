class DatabaseException(Exception):
    pass


class CommitError(DatabaseException):
    pass


class RollbackError(DatabaseException):
    pass


class InvalidParamsError(DatabaseException):
    pass
