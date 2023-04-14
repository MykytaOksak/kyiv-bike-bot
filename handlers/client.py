from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from data import BOT_USERNAME, DATABASE_URL
from keyboards.client_kb import *
from callbacks import *
from utils import *
from database import Database


TAGS = ['forest', 'lake', 'highway', 'bikepath', 'city', 'offroad', 'Done']
db = Database(DATABASE_URL)
db.connect()


class AddRoute(StatesGroup):
    adding_link = State()
    adding_image = State()
    adding_tags = State()
    adding_description = State()


async def command_stop(message: types.Message, state: FSMContext):
    if await state.get_state() != None:
        await message.reply('Route adding was canceled', reply_markup=kb_menu_client)
    else:
        await message.reply('Nothing to stop', reply_markup=kb_menu_client)
    await state.finish()


async def remove_keyboard(message: types.Message):
    await message.reply('Keyboard removed', reply_markup=types.ReplyKeyboardRemove())


async def any_msg(message: types.Message, state: FSMContext):
    if state != None:
        await message.reply('Please finish current step or cancel route adding')
    else:
        await message.reply('Not sure what\'s that')


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.chat.id, 'Hey! I can help you to find bike routes in Kyiv', reply_markup=kb_menu_client)
        await bot.send_message(message.chat.id, 'Use buttons below to navigate ⬇️')
    except:
        await message.reply(f'Please DM me first\nhttps://t.me/{BOT_USERNAME}')


async def command_routes_list(message: types.Message):
    routes = db.read_all('approved_routes')
    await send_routes_list(message, routes, update_rating_cb, 'Rate')


async def add_route_start(message: types.Message, state: FSMContext):
    await message.reply('Please navigate to google.com/maps, create a route on the map, and drop here the direction link', reply_markup=kb_cancel_route)
    await state.set_state(AddRoute.adding_link)  # set starting state


async def add_route_link(message: types.Message, state: FSMContext):
    if 'google.com/maps/dir' in message.text:
        await state.update_data(link=message.text)
        await message.reply('Get it. Uploading route preview...')

        url = (await state.get_data())['link']
        path = get_path(url)
        image = get_photo(path)

        preview = await message.reply_photo(image, 'Looks right?', reply_markup=kb_route_verif)
        await state.update_data(image=preview.photo[0].file_id)

        await state.set_state(AddRoute.adding_image)
    else:
        await message.reply('Doesn\'t look like a google maps link. Try again')


async def wrong_route_preview(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, 'Ahh :(\n\nYou may want to edit some waypoints on the map and send the link again')
    await state.set_state(AddRoute.adding_link)


async def add_route_tags(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, 'Good. Now let\'s add some details...')
    await state.set_state(AddRoute.adding_tags)
    await state.update_data(tags=TAGS)

    kb_route_tags = create_tags_kb(TAGS)
    await bot.send_message(query.message.chat.id, 'Pick appropriate tags below', reply_markup=kb_route_tags)


async def edit_tags(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    btn_text = callback_data['btn_text']
    state_tags = (await state.get_data())['tags']

    if btn_text == 'submit tags':
        checked_tags = [x.replace('✅', '') for x in state_tags if '✅' in x]
        result_tags_string = '#' + ' #'.join(checked_tags)
        await state.update_data(tags=result_tags_string)

        await state.set_state(AddRoute.adding_description)
        await bot.send_message(query.message.chat.id, 'Give your route a brief description\n\nEx. <em>Easy bike route through the city with lots of panoramic views</em>', parse_mode='HTML')

    else:
        if '✅' in btn_text:
            raw_tag = btn_text[:-2]
            index = state_tags.index(btn_text)
            state_tags[index] = raw_tag
        else:
            index = state_tags.index(btn_text)
            state_tags[index] = f'{btn_text} ✅'

        await state.update_data(tags=state_tags)

        kb_new_tags = create_tags_kb(state_tags)
        await query.message.edit_reply_markup(reply_markup=kb_new_tags)


async def add_route_desc(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)

    state_dict = await state.get_data()
    state_dict['rating'] = 'not rated'
    db.add('proposed_routes', tuple(state_dict.values()))

    await message.reply('The road has been added for review, thanks!', reply_markup=kb_menu_client)
    await state.finish()


async def udpate_rating(query: types.CallbackQuery, callback_data: dict):
    action = callback_data['action']
    rating = int(callback_data['rating'])
    route_id = int(callback_data['route_id'])

    if action == 'init':
        kb = create_rate_kb(0, route_id)
        await query.message.reply('How would you rate this route?', reply_markup=kb)
    elif action == 'update':
        kb = create_rate_kb(rating, route_id)
        await query.message.edit_reply_markup(reply_markup=kb)
    elif action == 'submit':
        rating_and_user_id = f'{rating}:{query.from_user.id}'
        db.update_rating('approved_routes', route_id, rating_and_user_id)
        await query.message.edit_text(text='Thanks for your feedback!', reply_markup=None)
        await query.answer('rating submitted')
    else:
        print('unknown action in udpate_rating_cb')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_stop, commands=['stop'])
    dp.register_message_handler(command_stop, Text(
        contains='stop', ignore_case=True), state='*')
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(
        command_routes_list, Text(contains='Routes list'))
    dp.register_message_handler(command_routes_list, commands=['routes'])
    dp.register_message_handler(add_route_start, commands=['add'], state=None)
    dp.register_message_handler(
        add_route_start, Text(contains='Add route'), state=None)
    dp.register_message_handler(add_route_link, state=AddRoute.adding_link)
    dp.register_callback_query_handler(add_route_tags, Text(
        equals='correct route'), state=AddRoute.adding_image)
    dp.register_callback_query_handler(wrong_route_preview, Text(
        equals='wrong route'), state=AddRoute.adding_image)
    dp.register_message_handler(
        remove_keyboard, Text(equals='remove keyboard'))
    dp.register_callback_query_handler(
        edit_tags, edit_tags_cb.filter(), state=AddRoute.adding_tags)
    dp.register_message_handler(
        add_route_desc, state=AddRoute.adding_description)
    dp.register_callback_query_handler(
        udpate_rating, update_rating_cb.filter(), state=None)
    dp.register_message_handler(any_msg)
    dp.register_message_handler(any_msg, state='*')
