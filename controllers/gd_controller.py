import datetime
from typing import Annotated
from fastapi import APIRouter
from typing import Annotated

from fastapi import Depends, HTTPException, status

from database.mongodb import create_dict_with_tupled_values, gd_command_history, get_station_status, get_station_working_status_interval, query_time_and_value_in_mongo, user_collection, gd_station_collection
from database.utils import failures, total_production
from models.station import Station
from models.tag import TagUpdate

from models.user import User, UserInDB
from security import get_current_user, hash_password, is_admin
from utils.get_tag_value import create_stop_tag, get_stop_value

route = APIRouter()


@route.post("/stop_station", response_description="Stop specific station in GD", 
            status_code=status.HTTP_200_OK,)
            # response_model=TagUpdate)
async def stop_station(station: str, admin: Annotated[get_current_user, Depends(is_admin)]):
    if admin.role != 'admin':
         print(admin)
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    station_in_db = gd_station_collection(station).find_one(sort=[('datetime', -1)])
    
    if not station_in_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Station {station} not found")

    if not get_stop_value(station_in_db):
        raise ValueError('Station already stopped')
    
    tag = create_stop_tag()
    up_tag = tag.model_dump()
    up_tag["updated"] = True
    up_tag["station"] = station
    up_tag["user"] = admin.username[:]
    new_tag = TagUpdate(**up_tag)
    gd_command_history().insert_one(new_tag.model_dump())

    return new_tag #{"message": "Station Stopped"}#

@route.get("/getAllStatus", response_description="Get status from all stations", 
            status_code=status.HTTP_200_OK)
async def getAllStatus(user: Annotated[get_current_user, Depends()]):
    try:
        status = {}

        dist = gd_station_collection("Distributing")#.find().limit(1).sort([('$natural',-1)])
        pickplace = gd_station_collection("PickAndPlace")#.find().limit(1).sort([('$natural',-1)])
        sort = gd_station_collection("Sorting").find()#.limit(1).sort([('$natural',-1)])

        dist_status = get_station_status(dist)
        pickplace_status = get_station_status(pickplace)
        sort_status = get_station_status(sort)

        status["Distributing"] = dist_status
        status["PickAndPlace"] = pickplace_status
        status["Sorting"] = sort_status
        
        return status                  
        
    except Exception as e:
         raise(e)

@route.get("/getStatus", response_description="Get status from specific station", 
            status_code=status.HTTP_200_OK)
async def getStatus(station):
     return get_station_status(station)

@route.get("/getTotalWorkTime", response_description="Get total work time from specific station", 
            status_code=status.HTTP_200_OK)
async def getTotalWorkTime(start,end,station):
    return get_station_working_status_interval(start, end, station)

@route.get("/getTotalProduction", response_description="Get total piece production", 
            status_code=status.HTTP_200_OK)
async def getTotalProduction(start, end):
    resultado = query_time_and_value_in_mongo(start=start, end=end)
    aux_dict = create_dict_with_tupled_values(resultado)
    return total_production(aux_dict)

@route.get("/getTotalFails", response_description="Get total stops", 
            status_code=status.HTTP_200_OK)
async def getTotalFails(start, end):
    resultado = query_time_and_value_in_mongo(start=start, end=end)
    aux_dict = create_dict_with_tupled_values(resultado)
    return failures(aux_dict)


def get_station_status_personal(station):
    status_dict = {}
    time_now = datetime.datetime.now()
    five_minutes_ago = time_now - datetime.timedelta(minutes=5)
    
    for tag in station["tags"]:
        if tag.timestamp <= five_minutes_ago:
            if tag.name =="M_STATUS" and tag.value == False:
                status_dict[station.name] = 'Not Working'
            else:
                status_dict[station.name] = 'Working'
        else:
            status_dict[station.name] = "Last update passed 5 minutes"
    
    return status_dict