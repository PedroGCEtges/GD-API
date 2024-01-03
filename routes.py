from fastapi import APIRouter
from controllers import user_controller as user, gd_controller as gd

route = APIRouter()

route.include_router(user.route, prefix='/users', tags=['Users'])
route.include_router(gd.route, prefix='/gd', tags=['GD'])