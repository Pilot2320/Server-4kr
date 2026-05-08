from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# 1. Custom exception classes
class ItemNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name

class InsufficientPermissionsException(Exception):
    def __init__(self, user: str):
        self.user = user

# 3. Pydantic models for error responses
class ErrorResponseModel(BaseModel):
    status: str
    message: str
    detail: str

# 2. Custom exception handlers
@app.exception_handler(ItemNotFoundException)
async def item_not_found_exception_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content=ErrorResponseModel(
            status="error",
            message="Item Not Found",
            detail=f"The item '{exc.name}' was not found in the inventory."
        ).model_dump()
    )

@app.exception_handler(InsufficientPermissionsException)
async def insufficient_permissions_exception_handler(request: Request, exc: InsufficientPermissionsException):
    return JSONResponse(
        status_code=403,
        content=ErrorResponseModel(
            status="error",
            message="Access Denied",
            detail=f"User '{exc.user}' does not have permission to perform this action."
        ).model_dump()
    )

# 4. Endpoints triggering exceptions
@app.get("/items/{item_name}")
async def get_item(item_name: str):
    if item_name == "forbidden":
        raise ItemNotFoundException(name=item_name)
    return {"item": item_name, "status": "available"}

@app.get("/admin/{username}")
async def admin_access(username: str):
    if username != "admin":
        raise InsufficientPermissionsException(user=username)
    return {"message": f"Welcome, {username}!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
