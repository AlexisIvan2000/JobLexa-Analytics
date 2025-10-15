from fastapi import APIRouter,HTTPException,Depends,status
from passlib.context import CryptContext
from models.schemas import UserLogin, UserCreate,TokenData,UserLoggedIn
from models.database import get_db_session, Users
from auth.jwt_handler import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth.jwt_handler import create_access_token, verify_access_token


pwd_context = CryptContext(schemes=["argon2"],deprecated= "auto")

auth_router = APIRouter(
    prefix= "/auth",
    tags=["Authentication"]
)

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
   query = select(Users).where(Users.email == user.email)
   result = await db.execute(query)
   existing_user = result.scalars().first()

   if existing_user:
      raise HTTPException(status_code=400, detail="User already exists")
   
   password_to_hash = user.password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
   hashed_pw = pwd_context.hash(password_to_hash)
   new_user = Users(
      first_name = user.first_name,
      last_name = user.last_name,
      email = user.email,
      password = hashed_pw
   )

   db.add(new_user)
   await db.commit()
   await db.refresh(new_user)
   

   return {
      "status": "success",
      "message" : "User registered successfully",
    }
   

@auth_router.post("/login", response_model=TokenData)
async def login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db_session)):
   query = select(Users).where(Users.email == user_credentials.email)
   result = await db.execute(query)
   db_user = result.scalars().first()

   if not db_user or not pwd_context.verify(user_credentials.password,db_user.password):
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED, 
         detail="Invalid credentials (Email or Password)"
      )
   
   access_token = create_access_token(data={"sub": db_user.email, "user_id":db_user.id})
   return TokenData(
      access_token=access_token,
      token_type="bearer",
      user=UserLoggedIn(
         email=db_user.email,
         first_name=db_user.first_name
      )
   )

@auth_router.get("/me")
async def get_current_user(token: str):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    return {"status": "success", "data": payload}