from typing import Optional
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        name, session
    )

    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Проект не найден!'
        )
    return project


def check_project_investment(
    project: CharityProject, amount: Optional[int] = 0, delete=False
) -> None:
    status_code = HTTPStatus.BAD_REQUEST
    if delete and project.invested_amount > 0:
        raise HTTPException(
            status_code=status_code,
            detail='В проект были внесены средства, не подлежит удалению!',
        )

    if project.fully_invested:
        raise HTTPException(
            status_code=status_code,
            detail='Закрытый проект нельзя редактировать!',
        )

    if amount is not None and project.invested_amount > amount:
        raise HTTPException(
            status_code=status_code,
            detail=(
                'Нельзя установить требуемую'
                ' сумму меньше внесённой в проект!'
            ),
        )
