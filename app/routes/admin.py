from typing import Optional, List

from fastapi import APIRouter, Depends

from app.models.order import StatusEnum
from app.schemas.users import UserCreate, TokenBase, AuthData, UserBase, User
from app.schemas.order import Order, OrderCreate, OrderShow
from app.utils.dependecies import get_current_user, check_admin_role
from app.utils.logger import get_logger
from app.utils.order import create_order_util, get_orders_filter, updating_order, get_one_order, delete_softly_order

admin_router = APIRouter(prefix="/admin")
logger = get_logger(__name__)


@admin_router.post("/orders")
async def create_order(order: OrderCreate, admin_user: User = Depends(check_admin_role),):
    logger.info("Creating a new order")
    return await create_order_util(order, admin_user)


@admin_router.get("/orders", response_model=List[Order])
async def get_orders(status: Optional[StatusEnum] = None,
                     min_price: Optional[float] = None,
                     max_price: Optional[float] = None, admin_user: User = Depends(check_admin_role)):
    logger.info(f"User:{admin_user.id} GET orders")
    return await get_orders_filter(status, min_price, max_price, admin_user)


@admin_router.put("/orders", response_model=Order)
async def update_order(order_id: int,
                       status: Optional[StatusEnum], admin_user: User = Depends(check_admin_role)):
    logger.info(f"Updating order id:{order_id}")
    return await updating_order(order_id, status, admin_user)


@admin_router.get("/orders/{order_id}", response_model=OrderShow)
async def get_order(order_id: int, admin_user: User = Depends(check_admin_role)):
    return await get_one_order(order_id, admin_user)


@admin_router.delete("/orders")
async def delete_order(order_id: int, current_user: User = Depends(get_current_user)):
    return await delete_softly_order(order_id,current_user)