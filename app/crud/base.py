from datetime import datetime
from typing import Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: Union[str, bool],
        session: AsyncSession,
    ):
        attr = getattr(self.model, attr_name)
        order_attr = getattr(self.model, 'create_date')
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value).with_for_update().order_by(order_attr)
        )
        return db_obj.scalars().all()

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
        fully_invested: bool = False,
        invested_amount: int = 0,
    ):

        obj_in_data = obj_in.dict()
        obj_in_data['fully_invested'] = fully_invested
        obj_in_data['invested_amount'] = invested_amount
        if fully_invested:
            obj_in_data['close_date'] = datetime.now()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        return db_obj

    @staticmethod
    def update(
        db_obj,
        update_data,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        invested_amount = getattr(db_obj, 'invested_amount')
        full_amount = getattr(db_obj, 'full_amount')
        if full_amount == invested_amount:
            setattr(db_obj, 'close_date', datetime.now())
            setattr(db_obj, 'fully_invested', True)
        session.add(db_obj)
        return db_obj

    @staticmethod
    async def remove(
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
