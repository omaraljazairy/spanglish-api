from fastapi import status


class NotFoundException(Exception):
    def __init__(self, msg:str) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = msg


class AlreadyExistsException(Exception):
    def __init__(self, msg:str) -> None:
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = msg
