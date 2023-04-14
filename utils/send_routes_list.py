from create_bot import bot
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from keyboards.client_kb import create_routes_list_kb

async def send_routes_list(message: types.Message, routes: list, callback: CallbackData, btn_text: str):
    if routes != []:
        await message.reply('Here is the list of proposed routes:')
        for route in routes:
            if btn_text != 'Rate':
                kb = InlineKeyboardMarkup(row_width=1).row(
                    InlineKeyboardButton(text=btn_text, callback_data=callback.new(
                            route_id=route[0],
                            message_id=message.from_user.id
                        )
                    )    
                )
            else:
                kb = create_routes_list_kb(route)    

            tags = route[3]  
            description = route[4]
            rating_str = '☆' * 5
            total_reviews = 0
            if route[5] != 'not rated':
                ratings = route[5].split(';')
                total_reviews = len(ratings)
                avg_rating = 0
                for rating_and_user in ratings:
                    rating = rating_and_user.split(':')[0] # get rating from 'user_id:rating'
                    avg_rating += int(rating)/len(ratings)
                rating_str = '★' * int(avg_rating)  + '☆' * (5 - int(avg_rating))
            rating = f'{rating_str} ({total_reviews} {("reviews", "review")[total_reviews == 1]})'

            caption = f'{tags}\n\n{description}\n\n{rating}'                     
            await bot.send_photo(message.chat.id, route[2], caption, reply_markup=kb)
    else:
        await message.reply('No routes available yet')        