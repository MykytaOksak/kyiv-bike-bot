from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callbacks import edit_tags_cb, update_rating_cb
from aiogram.utils.callback_data import CallbackData


# client menu keyboard
routes_btn = KeyboardButton('🗺️ Routes list')
add_route_btn = KeyboardButton('➕ Add route')

kb_menu_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu_client.row(routes_btn, add_route_btn)

# client inline route preview approve
correct_route_btn = InlineKeyboardButton(
    text='Yep', callback_data='correct route')
wrong_route_btn = InlineKeyboardButton(text='No', callback_data='wrong route')

kb_route_verif = InlineKeyboardMarkup(row_width=2)
kb_route_verif.row(correct_route_btn, wrong_route_btn)

# client cancel route keyboard
cancel_btn = KeyboardButton('❌ Stop adding route')

kb_cancel_route = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cancel_route.row(cancel_btn)


# client routes list kb
def create_routes_list_kb(route):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Open in Maps', url=route[1]),
        InlineKeyboardButton(text='Rate', callback_data=update_rating_cb.new(
            action='init', route_id=route[0], rating=0))
    ]])
    return kb

# client rate kb
def create_rate_kb(rating, id):
    buttons = []
    for i in range(5):
        if i < rating:
            btn_text = '⭐️'
        else:
            btn_text = '☆'
        buttons.append(InlineKeyboardButton(text=btn_text, callback_data=update_rating_cb.new(
            action='update', route_id=id, rating=i+1)))
    buttons.append(InlineKeyboardButton(text='Submit', callback_data=update_rating_cb.new(
        action='submit', route_id=id, rating=rating)))
    
    kb = InlineKeyboardMarkup(row_width=5)
    kb.add(*buttons)
    
    return kb

# client tags kb
def create_tags_kb(items: list[str]):
    buttons = []
    for i in range(0, (len(items) - 1), 2):
        button1 = InlineKeyboardButton(
            items[i], callback_data=edit_tags_cb.new(btn_text=items[i]))
        button2 = InlineKeyboardButton(
            items[i+1], callback_data=edit_tags_cb.new(btn_text=items[i+1]))
        buttons.append([button1, button2])

    buttons.append([InlineKeyboardButton(
        'Done', callback_data=edit_tags_cb.new(btn_text='submit tags'))])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb