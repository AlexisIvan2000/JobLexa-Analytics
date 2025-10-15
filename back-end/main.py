import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv 
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

load_dotenv() 

from settings import initialize_settings
initialize_settings() 

from models.database import create_tables
from auth.user_auth import auth_router
from auth.oauth import oauth_router
from services.router import router as jobmatch_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Démarrage de l'application... Création des tables.")
    await create_tables()
    yield
 
    print("Arrêt de l'application.")


app = FastAPI(lifespan=lifespan)

origins = [
   
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to JobLexa Analytics API! Use /docs for endpoints."}

app.include_router(auth_router)
app.include_router(oauth_router)
app.include_router(jobmatch_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)