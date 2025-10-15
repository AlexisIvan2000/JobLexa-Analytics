from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.database import Users, get_db_session
from auth.jwt_handler import create_access_token
from settings import settings
import requests
import time

oauth_router = APIRouter(prefix="/auth/google", tags=["OAuth2"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
REDIRECT_URI = settings.GOOGLE_REDIRECT_URI
FRONTEND_CALLBACK_URL = "http://localhost:5173/oauth/callback"

@oauth_router.get("/login")
async def google_login():
    """Redirige l'utilisateur vers la page de connexion Google"""
    auth_url = (
        f"{GOOGLE_AUTH_URL}"
        "?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
        "&prompt=consent"
    )
    return RedirectResponse(url=auth_url, status_code=302)


@oauth_router.get("/auth")
async def google_auth(request: Request, db: AsyncSession = Depends(get_db_session)):
    try:
        code = request.query_params.get("code")
        if not code:
            raise HTTPException(status_code=400, detail="Code manquant dans la redirection Google")

       
        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
        token_json = token_response.json()
        access_token = token_json.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Échec de l’obtention du token Google")

       
        user_info_response = requests.get(
            GOOGLE_USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"}
        )
        profile = user_info_response.json()

        email = profile.get("email")
        google_id = profile.get("id")
        first_name = profile.get("given_name", "")
        last_name = profile.get("family_name", "")

        if not email:
            raise HTTPException(status_code=400, detail="Impossible de récupérer l'email de Google")

        
        query = select(Users).where(Users.email == email)
        result = await db.execute(query)
        user = result.scalars().first()

        if user:
            user.oauth_provider = "google"
            user.google_id = google_id
            user.google_access_token = access_token
            user.google_expires_at = int(time.time()) + token_json.get("expires_in", 3600)
        else:
            user = Users(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password="GOOGLE_AUTH",
            )
            db.add(user)

        await db.commit()
        await db.refresh(user)

        app_token = create_access_token({"sub": email, "user_id": user.id})

        frontend_redirect = f"{FRONTEND_CALLBACK_URL}?token={app_token}"
        print("[DEBUG] Redirecting to:", frontend_redirect)

        return RedirectResponse(url=frontend_redirect, status_code=302)

    except Exception as e:
        print("[ERROR GOOGLE AUTH]:", str(e))
        raise HTTPException(status_code=500, detail=f"Erreur Google OAuth: {str(e)}")
