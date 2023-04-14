from aiogram import types, Dispatcher
from keyboards.admin_kb import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import ADMIN_ID, DATABASE_URL
from utils import send_routes_list
from callbacks.admin_callbacks import *
from database import Database


db = Database(DATABASE_URL)
db.connect()


async def command_admin(message: types.Message):
    if message.from_user.username == ADMIN_ID:
        await message.reply('Admin mode activated', reply_markup=kb_menu_admin)
    else:
        await message.reply('Only admin can perform this action')   


async def edit_routes(message: types.Message):
    routes = db.read_all('approved_routes')
    await send_routes_list(message, routes, remove_cb, 'Remove')


async def command_proposed_routes_list(message: types.Message):
    routes = db.read_all('proposed_routes')
    await send_routes_list(message, routes, approve_cb, 'Approve')


async def remove_route(query: types.CallbackQuery, callback_data: dict):
    route_id = callback_data['route_id']
    
    kb_restore = InlineKeyboardMarkup(row_width=1).row(
        InlineKeyboardButton(text='Restore', callback_data=restore_cb.new(
                route_id=route_id,
                message_id=query.from_user.id
            )
        )    
    )

    removed_route = db.read_one('approved_routes' ,route_id)
    db.remove_one('approved_routes', route_id)

    if db.read_one('removed_routes', route_id) is None: # if there is no route with this id in bin_db
        db.add_id('removed_routes', ((route_id,) + removed_route))    
    else:
        db.add('removed_routes', removed_route)     

    await query.message.edit_caption(caption='Deleted', reply_markup=kb_restore)
    await query.answer(f'route {route_id} removed')


async def restore_route(query: types.CallbackQuery, callback_data: dict):
    route_id = callback_data['route_id']
    
    kb_remove = InlineKeyboardMarkup(row_width=1).row(
        InlineKeyboardButton(text='Remove', callback_data=remove_cb.new(
                route_id=route_id,
                message_id=query.from_user.id
            )
        )    
    ) 

    route_to_restore = db.read_one('removed_routes', route_id)
    db.remove_one('removed_routes', route_id)
    
    if db.read_one('approved_routes', route_id) is None: # if there is no route with this id in main_db
        db.add_id('approved_routes', ((route_id,) + route_to_restore))      
    else:
        db.add('approved_routes', route_to_restore)
    
    caption = f'Restored'
    await query.message.edit_caption(caption=caption, reply_markup=kb_remove)
    await query.answer(f'route {route_id} restored')


async def approve_route(query: types.CallbackQuery, callback_data: dict):
    route_id = callback_data['route_id']
    
    route_to_add = db.read_one('proposed_routes', route_id)
    db.remove_one('proposed_routes', route_id)
    db.add('approved_routes', route_to_add)    
    
    await query.message.edit_caption(caption='Approved', reply_markup=None)
    await query.answer(f'route {route_id} approved')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(command_admin, commands=['admin', 'moderator'])
    dp.register_message_handler(edit_routes, text_contains='Edit routes')
    dp.register_message_handler(command_proposed_routes_list, text_contains='Approve routes')
    dp.register_callback_query_handler(remove_route, remove_cb.filter())
    dp.register_callback_query_handler(approve_route, approve_cb.filter())
    dp.register_callback_query_handler(restore_route, restore_cb.filter())
