from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDdonation(CRUDBase):
    @staticmethod
    async def get_by_user(user_id: int, session: AsyncSession):
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return donations.scalars().all()


donation_crud = CRUDdonation(Donation)
