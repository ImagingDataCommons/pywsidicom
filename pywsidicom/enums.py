class ErrorCode:
    NOMEM = 1
    INVALID = 2
    PARSE = 3
    IO = 4

class LogLevel:
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0

class VRClass:
    ERROR = 0
    STRING_MULTI = 1
    STRING_SINGLE = 2
    NUMERIC_DECIMAL = 3
    NUMERIC_INTEGER = 4
    BINARY = 5
    SEQUENCE = 6
