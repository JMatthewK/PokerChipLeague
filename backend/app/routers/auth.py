from fastapi import APIRouter, Request
from auth import oauth

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
    print("Token received:")
    print(token)
    
    user_info = await oauth.cognito.parse_id_token(request, token)
    print("User info retrieved:")
    print(user_info)

    # Here you would typically create a session or JWT for the user
    return {
        "message": "Login successful", 
        "user_info": user_info
        }
    
@router.get("/logout")
async def logout():
    return {"message": "Logout endpoint"}


# Endpoint to get user info from the session
@router.get("/user")
async def get_user_info(request: Request):
    # Retrieve user info from the session
    user_info = request.session.get("user_info")
    if not user_info:
        return {"error": "User not authenticated"}
    return {"user_info": user_info}