from fastapi import APIRouter
from middleware.http_error import Conflict, Unprocessable
from users.models.user import User
from users.utils.password import get_password_hash
from users.validators.register import RegisterRequestFormat

router = APIRouter()


@router.post("", status_code=201)
async def register(request_body: RegisterRequestFormat):

    request_data = request_body.dict()
    user_data = await User.Model.objects.find_user(email=request_data['email'])

    if user_data:
        raise Conflict()

    if request_data['password'] != request_data['reenteredPassword']:
        raise Unprocessable("Passwords don't match")

    request_data.pop('reenteredPassword')

    request_data['password'] = await get_password_hash(request_data['password'])
    await User.Model.objects.add_user(request_data)

    return {'message': 'user has been created'}
