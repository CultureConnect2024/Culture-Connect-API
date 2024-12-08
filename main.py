from fastapi import FastAPI
from datetime import datetime
app = FastAPI()

@app.get("/")
async def root():
    return { "status": "success",  
        "message": "API connection successful",  
        "timestamp": datetime.now().isoformat(),}

app.include_router(
    __import__("app.src.routes.check", fromlist=["router"]).router, 
    prefix="/check", 
    tags=["Check"]
)

app.include_router(
    __import__("app.src.routes.auth", fromlist=["router"]).router, 
    prefix="/auth", 
    tags=["Auth"]
)

app.include_router(
    __import__("app.src.routes.users", fromlist=["router"]).router, 
    prefix="/users", 
    tags=["Users"]
)
# app.include_router(check_router, prefix="/check", tags=["Check"])
# app.include_router(auth_router, prefix="/auth", tags=["Check"])
