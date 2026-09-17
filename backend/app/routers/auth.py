from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import oauth
from app.dependencies.database import get_db
from app.services.users import get_or_create_cognito_user
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# This router will handle authentication-related endpoints
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Authentication Endpoints for logging in and out

@router.get("/login")
async def login(request: Request):
    """Redirects user to Cognito hosted UI login page

    Args:
        request (Request): Request object contains information about the request and is used to access the request context, which is necessary for OAuth2 flow.

    Returns:
        RedirectResponse: Redirects the user to AWS Cognito for authentication.
    """
    
    redirect_uri = request.url_for('auth_callback')
    return await oauth.cognito.authorize_redirect(request, redirect_uri)

# Callback endpoint to handle the response from Cognito after authentication
@router.get("/callback", name="auth_callback")
async def auth_callback(
    request: Request, 
    db: AsyncSession = Depends(get_db)):
    """Handles Cognito OAuth callback requests
    
    After successful authentication, Cognito will redirect the user to this endpoint with an authorization code. This function exchanges the code for an access token and retrieves user information.

    Args:
        request (Request): Request object contains information about the request and is used to access the request context, which is necessary for OAuth2 flow.

    Returns:
        dict: A dictionary containing the login status and user information.
    """
    
    print("Callback received, processing authentication...")
    
    # Information from Cognito login response is stored in the session for later use
    token = await oauth.cognito.authorize_access_token(request)
    user_info = token["userinfo"]
    
    # If user_info doesn't exist raise a value error
    if not user_info:
        raise ValueError("Cognito response is missing user information")
    
    # Get or create the user in the database based on Cognito sub and email
    user = await get_or_create_cognito_user(db=db, user_info=user_info)
    
    # Request a session using the user data
    request.session["user"] = {
        "id": str(user.id),
        "sub": user_info["sub"],
        "email": user_info["email"],
        "username": user_info.get("username"),
        "nickname": user_info.get("nickname")
    }
    print("Session: ")
    print(request.session)
    

    # Here you would typically create a session or JWT for the user
    return {
        "message": "Login successful", 
        "user": request.session["user"]
        }
    
@router.get("/logout")
async def logout(request: Request):
    """Endpoint to logout user and end session data

    Args:
        request (Request): Request object contains information about the request and is used to access the request context, which is necessary for OAuth2 flow.

    Returns:
        _type_: Message indicating that the user has been logged out.
    """
    request.session.clear()
    
    cognito_logout_url = (
        f"https://{os.getenv('COGNITO_DOMAIN')}/logout"
        f"?client_id={os.getenv('COGNITO_CLIENT_ID')}"
        f"&logout_uri={os.getenv('COGNITO_LOGOUT_REDIRECT_URI')}"
    )
    
    return RedirectResponse(url=cognito_logout_url)


@router.get("/me")
async def get_user_info(request: Request):
    """API endpoint to retrieve user info from current session

    Args:
        request (Request): Request object contains information about the request and is used to access the request context, which is necessary for OAuth2 flow.

    Returns:
        _type_: A dictionary containing the user information.
    """
    # Retrieve user info from the session
    user = request.session.get("user")
    
    if not user :
        return {"error": "User not authenticated"}
    return {"user": user}