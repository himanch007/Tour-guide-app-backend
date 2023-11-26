from core.database import conn
from bson import ObjectId
import datetime
from pydantic import validate_arguments

db = conn['User']


class UserManager:
    @validate_arguments
    async def find_user(self, email: str = None, user_id: str = None):
        user_data = {}
        if email:
            user_data = db.find_one({"email": email})
        if user_id:
            user_data = db.find_one({"_id":ObjectId(user_id)})

        return user_data

    @validate_arguments
    async def add_user(self, user: dict):
        user['metadata']= {
            'createdOn': datetime.datetime.now()
        }

        db.insert_one(user)
