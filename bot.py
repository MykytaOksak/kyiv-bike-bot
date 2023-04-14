import os
from aiogram.utils import executor
from create_bot import dp, bot
from data import config
from database import Database

async def on_startup(_):
    await bot.set_webhook(config.URL_APP)
    
    db = Database(config.DATABASE_URL)
    db.connect()
    db.create_table('approved_routes')
    db.create_table('proposed_routes')
    db.create_table('removed_routes')

    from handlers import client, admin

    admin.register_handlers_admin(dp)
    client.register_handlers_client(dp)

async def on_shutdown(_):
    await bot.delete_webhook()

executor.start_webhook(
    dispatcher=dp, 
    webhook_path='', 
    on_startup=on_startup, 
    on_shutdown=on_shutdown, 
    skip_updates=True, 
    host=config.APP_HOST, 
    port = int(os.environ.get('PORT', 5000))
)