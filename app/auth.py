from fastapi import Header, HTTPException

async def verify_token(authorization: str = Header(None)):
    if authorization != "Bearer tk421secret":
        raise HTTPException(status_code=401, detail="Unauthorized")
