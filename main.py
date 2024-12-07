from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API connection successful"}

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
# app.include_router(check_router, prefix="/check", tags=["Check"])
# app.include_router(auth_router, prefix="/auth", tags=["Check"])
