from middleware.http_error import Unauthorized
from fastapi.requests import Request
from users.models.user import User
from users.utils.token import decode_access_token


async def authentication_dependency(request: Request):
    '''
    Function to check for authentication
    '''
    auth_token = request.headers.get('authorization')

    if auth_token is None:
        raise Unauthorized()
    else:
        try:
            payload = await decode_access_token(auth_token.split()[1])
            print("Code for single login will be here")
            user_data = await User.Model.objects.find_user(user_id=payload['id'])
            user_data.pop('password')
            setattr(request, 'user_data', user_data)
        except:
            raise Unauthorized()
