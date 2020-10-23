from ..crud.item import save_item, get_item, get_all


class ItemService:
    @staticmethod
    async def save(db, item):
        return await save_item(db, item)

    @staticmethod
    async def fetch(con, id_):
        return await get_item(con, id_)

    @staticmethod
    async def fetch_all(con):
        return await get_all(con)
