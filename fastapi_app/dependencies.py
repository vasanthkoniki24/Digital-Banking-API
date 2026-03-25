from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import decode_token
from database import cursor   # IMPORTANT

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = decode_token(token)

        username = payload.get("sub")

        #  Fetch user from DB
        cursor.execute(
            "SELECT id, username FROM banking_userdata WHERE username=?",
            (username,)
        )
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        #  RETURN FULL USER OBJECT
        return {
            "id": user[0],
            "username": user[1]
        }

    except:
        raise HTTPException(status_code=401, detail="Invalid token")