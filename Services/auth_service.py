from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Optional
from bson import ObjectId
from DB.db import users_db
from models import User

# Constants
SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Common exception for invalid credentials
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Generate user token with roles
def create_user_token(username: str, role: str):
    return create_access_token(data={"sub": username, "role": role})

# Verify token and extract user information
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        role: Optional[str] = payload.get("role")
        if not username or not role:
            raise credentials_exception
        return {"username": username, "role": role}
    except JWTError:
        raise credentials_exception

# Get the current authenticated user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    token_data = verify_token(token)
    username = token_data["username"]

    user_data = users_db.find_one({"username": username})
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Convert MongoDB _id to string and return as User model instance
    user_data["_id"] = str(user_data["_id"])
    return User(**user_data)

# Admin access verification
async def verify_admin(token: str = Depends(oauth2_scheme)):
    user_data = verify_token(token)
    if user_data["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return user_data

# User registration
def register_user(username: str, password: str, full_name: str, email: str, role: str = "customer"):
    if users_db.find_one({"username": username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    hashed_password = pwd_context.hash(password)
    user_data = {
        "username": username,
        "full_name": full_name,
        "email": email,
        "password": hashed_password,
        "role": role,
        "created_at": datetime.utcnow(),
    }
    result = users_db.insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)
    user_data.pop("password")  # Remove password from response
    return user_data

# Password hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# User authentication (login)
def authenticate_user(username: str, password: str):
    user = users_db.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_user_token(username=username, role=user["role"])
    user["_id"] = str(user["_id"])
    user_details = {
        "id": user["_id"],
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"],
        "access_token": access_token,
        "token_type": "bearer",
    }
    if "email" in user:
        user_details["email"] = user["email"]
    return user_details

# Retrieve all users
def get_all_users():
    return [User(**user) for user in users_db.find({})]

# Get user by ID
def get_user_by_id(id: str):
    user = users_db.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return user

# Get user by email
def get_users_by_email(email: str):
    users = users_db.find({"email": {"$regex": email, "$options": "i"}})
    user_list = [User(**user) for user in users]
    if not user_list:
        raise HTTPException(status_code=404, detail="No users found with the specified email")
    return user_list

# Edit user
def edit_user(id: str, body: User):
    update_data = {k: v for k, v in body.dict(exclude_unset=True).items() if v is not None}
    user = users_db.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users_db.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    updated_user = users_db.find_one({"_id": ObjectId(id)})
    updated_user["_id"] = str(updated_user["_id"])
    return updated_user

# Delete user
def delete_user(id: str):
    result = users_db.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return f"User with ID: {id} was successfully deleted"
