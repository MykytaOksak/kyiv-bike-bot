from aiogram.utils.callback_data import CallbackData

remove_cb = CallbackData('remove', 'route_id', 'message_id')
approve_cb = CallbackData('approve', 'route_id', 'message_id')
restore_cb = CallbackData('restore', 'route_id', 'message_id')