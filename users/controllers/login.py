from fastapi import APIRouter
from middleware.http_error import Unauthorized
from users.models.user import User
from users.utils.password import verify_password
from users.utils.token import get_access_token
from users.validators.login import LoginRequestFormat

router = APIRouter()


@router.post("", status_code=200)
async def login(request_body: LoginRequestFormat):

    request_data = request_body.dict()
    user = await User.Model.objects.find_user(email=request_data['email'])
    if not user:
        raise Unauthorized(message="User does not exist")
    
    plain_password = request_data['password']
    hashed_password = user['password']

    if await verify_password(plain_password, hashed_password):
        access_token = await get_access_token(user)
        # code to store token in db for single login
    else:
        raise Unauthorized(message="Incorrect password")
    
    return {
        "token": access_token
    }
