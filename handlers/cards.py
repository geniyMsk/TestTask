from config import ADMINS
from loader import bot, dp

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
from DBCommands import DBCommands


class ADD(StatesGroup):
    add = State()
    price = State()


db = DBCommands()

for admin in ADMINS:
    @dp.message_handler(user_id=admin, commands=['add'], state='*')
    async def admin(message: types.Message):
        await message.answer("Отправьте карточку товара(без цены)")
        await ADD.add.set()


@dp.message_handler(content_types=['photo'], state=ADD.add)
async def album_handler(message: types.Message):
    photo = message.photo[-1].file_id
    await db.create()

    ids = (await db.select_id()).fetchall()
    try:
        id = max(ids)[0] + 1
    except:
        id = 1

    caption = message.caption
    par = (id, f'{photo}', f'{caption}')
    await db.add_card(par=par)
    await message.answer("Напишите цену товара")
    await ADD.price.set()


@dp.message_handler(state=ADD.price)
async def add_price(message: types.Message):
    try:
        price = int(message.text)
    except:
        await message.answer("Пожалуйста, укажите правильную цену")
        return

    ids = (await db.select_id()).fetchall()
    id = max(ids)[0]

    par = (price, id,)
    await db.update_price(par=par)

    photo = (await db.select_photo(id=(id,))).fetchone()[0]
    caption_text = (await db.select_caption(id=(id,))).fetchone()[0]
    caption_price = f'Цена: {price}'

    #ПОДПИСЬ К ТОВАРУ
    if caption_text == 'None':
        caption = caption_price
    else:
        caption = caption_text + '\n\n' + caption_price

    username = (await bot.get_me()).username

    inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить в корзину', callback_data=f'{id}')
            ],
            [
                InlineKeyboardButton(text='Перейти в корзину', url=f't.me/' + username + '?start=1')
            ]
        ])

    await bot.send_photo(chat_id='@channel_test12345', photo=photo, caption=caption, reply_markup=inline)


# HANDLER КНОПКИ ДОБАВЛЕНИЕ В КОРЗИНУ
@dp.callback_query_handler()
async def add_in(callback_query: types.CallbackQuery):
    data = callback_query.data
    chatid = callback_query.from_user.id
    ids = (await db.select_id()).fetchall()
    for i in ids:
        id = i[0]

        if (data == f'{id}'):
            user = (await db.select_user(chatid=(chatid,))).fetchall()[0][0]
            if user == 0:
                a = [0]
                par = (f'{callback_query.from_user.full_name}', f'{callback_query.from_user.username}',
                       f'{callback_query.from_user.id}', '[]')
                await db.add_user(par=par)
            zakaz = json.loads((await db.select_zakaz(chatid=(f'{chatid}',))).fetchone()[0])
            zakaz.append(id)
            par = (f'{zakaz}', chatid)
            await db.update_zakaz(par=par)


for admin in ADMINS:

    #ВСЕ КАРТОЧКИ
    @dp.message_handler(commands=['all'], user_id=admin, state='*')
    async def all(message: types.Message):
        ids = (await db.select_id()).fetchall()
        for id in ids:
            photo = (await db.select_photo(id)).fetchone()[0]
            caption_text = (await db.select_caption(id)).fetchone()[0]
            caption_price = (await db.select_price(id)).fetchone()[0]

            if caption_text == 'None':
                caption = f'Цена: {caption_price}\n\nid = {id[0]}'
            else:
                caption = caption_text + '\n\nЦена: ' + f'{caption_price}\n\nid = {id[0]}'

            await message.answer_photo(photo, caption=caption)

    #УДАЛЕНИЕ КАРТОЧКИ
    @dp.message_handler(commands=['delete'], user_id=admin, state='*')
    async def delete(message: types.Message):
        id = message.get_args()
        if id == '':
            await message.answer("Вы не указали id")
            return
        try:
            await db.delete_card(id=(id,))
            await message.answer("Карточка успешно удалена")
        except:
            await message.answer("Произошла ошибка")