from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# admin kb
edit_routes_btn = KeyboardButton('🗺️ Edit routes')
approve_route_btn = KeyboardButton('Approve routes')

kb_menu_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu_admin.row(edit_routes_btn, approve_route_btn)

