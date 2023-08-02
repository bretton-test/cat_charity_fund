from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User, Donation, CharityProject
from app.schemas.donation import DonationDB, DonationCreate, DonationDbAdmin
from app.services.investments_handler import create_object

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    new_donation = await create_object(
        Donation, CharityProject, donation, session, user
    )
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDbAdmin],
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),)
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Возвращает список всех пожертвований.
    """

    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Вернуть список пожертвований пользователя, выполняющего запрос.
    """
    return await donation_crud.get_by_user(user.id, session)
