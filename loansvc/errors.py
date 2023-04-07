from fastapi import HTTPException

class NotFoundHTTPException(HTTPException):
    def __init__(self, entity_name: str, id: int):
        detail = f"Could not find {entity_name} with id={id}"
        super().__init__(status_code=404, detail=detail)
