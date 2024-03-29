import string
from datetime import datetime
import random

from fastapi import HTTPException
from pydantic import EmailStr
from pymongo import MongoClient

from .email import EmailService
from .security import get_password_hash
from ..models.email import EmailSchema
from ..models.user import UserInCreate, UserInDB, UserInUpdate, User
from ..repository.users import UserRepository


class UserService:

    def __init__(self, db: MongoClient):
        self.repository = UserRepository(db)

    async def create(self, user_in: UserInCreate):
        user = await self.repository.find(email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists",
            )
        verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        user_hashed = UserInDB(**user_in.dict(),
                               hashed_password=get_password_hash(user_in.password),
                               is_active=False,
                               verification_code=verification_code,
                               is_deleted=False)
        user_hashed.created_at = datetime.now()
        user_hashed.updated_at = datetime.now()
        user = await self.repository.create(user_hashed.model_dump(exclude_none=True))
        user_hashed.id = str(user.inserted_id)
        await self._send_email(user_in.email, verification_code)
        return user_hashed

    @staticmethod
    async def _send_email(email: str, verification_code: str):
        email_service = EmailService()
        verification_link = f"/verify?code={verification_code}"
        _ = await email_service.send_email(
            EmailSchema(email=[email], body={"verification_link": verification_link}))

    async def verify(self, email: EmailStr, code: str):
        user = await self.repository.find(email=email, verification_code=code)
        if not user:
            raise HTTPException(status_code=404, detail="User not found or verification code incorrect")

        user = UserInDB(id=str(user["_id"]), **user)
        user.is_active = True
        user.updated_at = datetime.now()
        await self.repository.update(user.id, user.model_dump(exclude={"id"}))
        return {"message": "Email verified successfully"}

    async def update(self, current_user: User, user: UserInUpdate):
        user_hashed = UserInDB(**current_user.model_dump(), hashed_password=get_password_hash(user.password))
        user_hashed.updated_at = datetime.now()
        user_updated = await self.repository.update(current_user.id,
                                                    user_hashed.model_dump(exclude_none=True, exclude={"id"}))
        return User(**user_hashed.model_dump())
