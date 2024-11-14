from fastapi import HTTPException, APIRouter,Depends, Form, status
from  models import User
from fastapi.security import OAuth2PasswordRequestForm
from Services.auth_service import get_user_by_id, authenticate_user, get_users_by_email,get_all_users, get_current_user,register_user,verify_admin

router = APIRouter()

@router.get("/")
def get_users(current_user: dict = Depends(verify_admin)):
    return get_all_users()


@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


    return {
        "access_token": user["access_token"],
        "token_type": "bearer",
        "user_details": {
            "id": user["id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

@router.post("/")
def register_me(username: str = Form(...), password: str = Form(...), full_name: str = Form(...), email: str = Form(...)):
    return register_user(username, password, full_name, email)

@router.get("/{id}")
def get_user_by_identifier(id:str):
    return get_user_by_id(id)

@router.get("/user/{email}")
def get_user_by_email(email):
    return get_users_by_email(email)

@router.get("/current_user")
def get_loggedin_user(current_user: User = Depends(get_current_user)):
    return current_user