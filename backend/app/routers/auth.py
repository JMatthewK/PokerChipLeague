from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.auth import oauth
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
async def auth_callback(request: Request):
    """Handles Cognito OAuth callback requests
    
    After successful authentication, Cognito will redirect the user to this endpoint with an authorization code. This function exchanges the code for an access token and retrieves user information.

    Args:
        request (Request): Request object contains information about the request and is used to access the request context, which is necessary for OAuth2 flow.

    Returns:
        dict: A dictionary containing the login status and user information.
    """
    
    print("Callback received, processing authentication...")
    
    token = await oauth.cognito.authorize_access_token(request)
    user_info = token["userinfo"]
    request.session["user_info"] = {
        "sub": user_info["sub"],
        "email": user_info["email"],
        "username": user_info.get("cognito:username")
    }
    print("Session: ")
    print(request.session)

    # Here you would typically create a session or JWT for the user
    return {
        "message": "Login successful", 
        "user_info": user_info
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
    user_info = request.session.get("user_info")
    
    if not user_info:
        return {"error": "User not authenticated"}
    return {"user_info": user_info}