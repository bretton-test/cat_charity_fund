from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_exists,
    check_project_investment,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.investments_handler import create_object
from app.models import Donation, CharityProject


router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""

    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),)
)
async def create_new_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Создаёт благотворительный проект.
    """

    await check_name_duplicate(project.name, session)
    new_project = await create_object(
        CharityProject, Donation, project, session, None
    )
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),)
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Удаляет проект. Нельзя удалить проект,
     в который уже были инвестированы средства, его можно только закрыть.
    """
    project = await check_project_exists(project_id, session)
    check_project_investment(project, delete=True)
    return await charity_project_crud.remove(project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),)
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await check_project_exists(project_id, session)
    update_data = obj_in.dict(exclude_unset=True)
    check_project_investment(project, obj_in.full_amount)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    project = charity_project_crud.update(
        db_obj=project, update_data=update_data, session=session
    )
    await session.commit()
    await session.refresh(project)
    return project
