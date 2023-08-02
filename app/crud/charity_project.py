from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CrudCharityProject(CRUDBase):
    @staticmethod
    async def get_project_id_by_name(
        name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == name)
        )
        return db_project_id.scalars().first()


charity_project_crud = CrudCharityProject(CharityProject)
