from aiogram.utils.callback_data import CallbackData

edit_tags_cb = CallbackData('add_tag', 'btn_text')
update_rating_cb = CallbackData('update_rating', 'action', 'route_id', 'rating')
init_rating_cb = CallbackData('init_rating', 'route_id')