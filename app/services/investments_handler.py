from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User


def calculate_investment(objects, full_amount, session):
    invested_amount = 0
    update_data = {}
    object_for_update = CRUDBase(objects[0])

    for obj in objects:
        if full_amount <= 0:
            break
        free_amount = obj.full_amount - obj.invested_amount
        full_amount -= free_amount
        investment = (
            free_amount + full_amount if full_amount <= 0 else free_amount
        )
        invested_amount += investment
        update_data['invested_amount'] = obj.invested_amount + investment
        object_for_update.update(obj, update_data, session)

    return invested_amount


async def create_object(
    cls_for_create,
    cls_for_update,
    data_in,
    session: AsyncSession,
    user: Optional[User] = None,
):
    objects_for_update = await CRUDBase(cls_for_update).get_by_attribute(
        'fully_invested', False, session
    )
    full_amount = data_in.dict().get('full_amount')
    invested_amount = (
        calculate_investment(objects_for_update, full_amount, session)
        if objects_for_update
        else 0
    )
    fully_invested = full_amount == invested_amount

    new_object = CRUDBase(cls_for_create).create(
        data_in,
        session,
        user=user,
        fully_invested=fully_invested,
        invested_amount=invested_amount,
    )
    await session.commit()
    await session.refresh(new_object)
    return new_object
