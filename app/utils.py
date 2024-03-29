from app.db.mongodb_utils import connect_to_mongo


async def startup():
    await connect_to_mongo()
