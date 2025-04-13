# src/users/service.py
from src.users.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import or_, select
from src.users.schema import UserCreateModel
from src.utils.auth import generate_password_hash

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()

        return user
    
    async def user_exists(self, email: str, username: str, session: AsyncSession) -> bool:
        # user = await self.get_user_by_email(email, session)
        statement = select(User).where(
            or_(
                User.email == email,
                User.username == username
            )
        )

        result = await session.exec(statement)
        user = result.first()

        # return True if user is not None else False
        return user is not None
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(user_data_dict['password'])
        
        session.add(new_user)
        await session.commit()

        return new_user