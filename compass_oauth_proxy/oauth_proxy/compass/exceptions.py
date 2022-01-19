class CompassException(Exception):
    message = "Compass Exception"

    def __init__(self, message=message) -> None:
        super().__init__(message)


class CompassAuthException(CompassException):
    def __init__(self) -> None:
        super().__init__("Compass Login failed")
