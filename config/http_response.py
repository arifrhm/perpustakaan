class HTTPResponse:
    # 1xx Informational
    CONTINUE = {"status_code": 100, "message": "Continue"}
    CREATED = {"status_code": 201, "message": "Created"}
    ACCEPTED = {"status_code": 202, "message": "Accepted"}
    NON_AUTHORITATIVE_INFORMATION = {"status_code": 203, "message": "Non-Authoritative Information"}
    NO_CONTENT = {"status_code": 204, "message": "No Content"}
    PARTIAL_CONTENT = {"status_code": 206, "message": "Partial Content"}
    MULTI_STATUS = {"status_code": 207, "message": "Multi-Status"}
    ALREADY_REPORTED = {"status_code": 208, "message": "Already Reported"}
    IM_USED = {"status_code": 226, "message": "IM Used"}

    # 3xx Redirection
    MULTIPLE_CHOICES = {"status_code": 300, "message": "Multiple Choices"}
    MOVED_PERMANENTLY = {"status_code": 301, "message": "Moved Permanently"}
    FOUND = {"status_code": 302, "message": "Found"}
    SEE_OTHER = {"status_code": 303, "message": "See Other"}
    NOT_MODIFIED = {"status_code": 304, "message": "Not Modified"}
    USE_PROXY = {"status_code": 305, "message": "Use Proxy"}
    SWITCH_PROXY = {"status_code": 306, "message": "Switch Proxy"}
    TEMPORARY_REDIRECT = {"status_code": 307, "message": "Temporary Redirect"}
    PERMANENT_REDIRECT = {"status_code": 308, "message": "Permanent Redirect"}

    # 4xx Client Errors
    BAD_REQUEST = {"status_code": 400, "message": "Bad Request"}
    UNAUTHORIZED = {"status_code": 401, "message": "Unauthorized"}
    PAYMENT_REQUIRED = {"status_code": 402, "message": "Payment Required"}
    FORBIDDEN = {"status_code": 403, "message": "Forbidden"}
    NOT_FOUND = {"status_code": 404, "message": "Not Found"}
    METHOD_NOT_ALLOWED = {"status_code": 405, "message": "Method Not Allowed"}
    NOT_ACCEPTABLE = {"status_code": 406, "message": "Not Acceptable"}
    PROXY_AUTHENTICATION_REQUIRED = {"status_code": 407, "message": "Proxy Authentication Required"}
    REQUEST_TIMEOUT = {"status_code": 408, "message": "Request Timeout"}
    CONFLICT = {"status_code": 409, "message": "Conflict"}
    GONE = {"status_code": 410, "message": "Gone"}
    LENGTH_REQUIRED = {"status_code": 411, "message": "Length Required"}
    PRECONDITION_FAILED = {"status_code": 412, "message": "Precondition Failed"}
    PAYLOAD_TOO_LARGE = {"status_code": 413, "message": "Payload Too Large"}
    URI_TOO_LONG = {"status_code": 414, "message": "URI Too Long"}
    RANGE_NOT_SATISFIABLE = {"status_code": 416, "message": "Range Not Satisfiable"}
    EXPECTATION_FAILED = {"status_code": 417, "message": "Expectation Failed"}
    IM_A_TEAPOT = {"status_code": 418, "message": "I'm a teapot"}
    ENHANCE_YOUR_CALM = {"status_code": 420, "message": "Enhance Your Calm"}
    LOCKED = {"status_code": 423, "message": "Locked"}
    FAILED_DEPENDENCY = {"status_code": 424, "message": "Failed Dependency"}
    UNORDERED_COLLECTION = {"status_code": 425, "message": "Unordered Collection"}
    UPGRADE_REQUIRED = {"status_code": 426, "message": "Upgrade Required"}
    TOO_MANY_REQUESTS = {"status_code": 429, "message": "Too Many Requests"}
    REQUEST_HEADER_FIELDS_TOO_LARGE = {"status_code": 431, "message": "Request Header Fields Too Large"}
    NO_RESPONSE = {"status_code": 444, "message": "No Response"}
    RETRY_WITH = {"status_code": 449, "message": "Retry With"}
    BLOCKED_BY_WINDOWS_PARENTAL_CONTROLS = {"status_code": 450, "message": "Blocked by Windows Parental Controls"}
    UNAVAILABLE_FOR_LEGAL_REASONS = {"status_code": 451, "message": "Unavailable For Legal Reasons"}
    REQUEST_HEADER_TOO_LARGE = {"status_code": 494, "message": "Request Header Too Large"}

    # 5xx Server Errors
    INTERNAL_SERVER_ERROR = {"status_code": 500, "message": "Internal Server Error"}
