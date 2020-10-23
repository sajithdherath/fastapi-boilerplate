import logging

from fastapi import HTTPException

from ..config import database_name, items_collection, DEBUG
from ..models import Item


async def save_item(con, item: Item):
    try:
        await con[database_name][items_collection].insert_one(item.dict())
        return
    except Exception as e:
        if DEBUG:
            logging.exception(e)
        else:
            logging.error(e)
        raise HTTPException(500, detail="database error")


async def get_item(con, id_):
    try:
        item = con[database_name][items_collection].find_one({"_id": id_})
        return Item(**item)
    except Exception as e:
        if DEBUG:
            logging.exception(e)
        else:
            logging.error(e)
        raise HTTPException(500, detail="database error")


async def get_all(con):
    try:
        res = []
        items = con[database_name][items_collection].find({})
        async for item in items:
            res.append(Item(**item))
        return res
    except Exception as e:
        if DEBUG:
            logging.exception(e)
        else:
            logging.error(e)
        raise HTTPException(500, detail="database error")
