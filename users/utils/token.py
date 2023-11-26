import jwt, datetime
from core.settings import SECRET_KEY


async def get_access_token(user):
    payload = {
            'id': str(user['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90),
            'iat': datetime.datetime.utcnow()
        }
    return jwt.encode(payload, SECRET_KEY)

async def decode_access_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])