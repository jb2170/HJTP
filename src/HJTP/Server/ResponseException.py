class ResponseException(Exception):
    """
    raise an instance of this exception when 4XX or 5XX codes apply
    let the server handle the exception
    """

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
