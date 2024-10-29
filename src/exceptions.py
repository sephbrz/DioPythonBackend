class AccountNotFoundError(Exception):
    pass


class TransactionsNotFoundError(Exception):
    pass


class BusinessError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class DatabaseError(Exception):
    pass
