# Contains the OAuth registration and JWT validation

from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

oauth.register(
  name='oidc',
  authority='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_bLhaihn2p',
  client_id='paqhnpmsrdodif3jfe5u1r5ul',
  client_secret='<client secret>',
  server_metadata_url='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_bLhaihn2p/.well-known/openid-configuration',
  client_kwargs={'scope': 'phone openid email'}
)