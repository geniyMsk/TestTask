from config import ADMINS
from loader import bot, dp, provider_token

from aiogram import types
import json
from DBCommands import DBCommands



db = DBCommands()
#КОРЗИНА(КОМАНДА START С АРГУМЕНТОМ 1)
@dp.message_handler(commands=['start'], state='*')
async def start(message:types.Message):
    chatid = message.from_user.id
    if message.get_args() != '':

        #ПОЛУЧАЕМ СПИСОК С ТОВАРАМИ В КОРЗИНЕ
        zakaz=json.loads((await db.select_zakaz(chatid=(f'{chatid}',))).fetchone()[0])

        #ПРОВЕРКА НА ПУСТОТУ КОРЗИНЫ
        if zakaz==[]:
            await message.answer('Вашу корзина пуста')
        else:
            await message.answer("Ваша корзина:")
            sum=0

            #ОТПРАВКА КОРЗИНЫ
            for i in zakaz:

                id = (f'{i}',)
                photo = (await db.select_photo(id)).fetchone()[0]
                caption_text = (await db.select_caption(id)).fetchone()[0]
                caption_price = (await db.select_price(id)).fetchone()[0]
                
                #ПОДПИСЬ К ФОТО ТОВАРА
                if caption_text == 'None':
                    caption = f'Цена: {caption_price}'
                else:
                    caption = caption_text + '\n\nЦена: ' + f'{caption_price}'

                await message.answer_photo(photo, caption=caption)
                sum+=caption_price

            #ОТПРАВКА ПЛАТЕЖНОЙ КНОПКИ
            prices = [{"label": 'RUB', "amount": sum * 100}]
            await bot.send_invoice(chat_id=message.chat.id, title='Ваша корзина', payload=f'{sum}',
                                       provider_token=provider_token, description="Ваши товары товары в корзине",
                                       currency='RUB', prices=prices)
            await message.answer(
                    "Это тестовый платеж. Для оплаты используйте данные тестовой карты: 1111 1111 1111 1026, 12/22, CVC 000.")

#HANDLER ПЛАТЕЖЕЙ
@dp.pre_checkout_query_handler(state='*')
async def pre_check(checkout:types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=checkout.id, ok=False,
                                        error_message='Это тестовый платёж, поэтому платеж не прошел, ваша корзина пуста')

    #ОТПРАВКА КОРЗИНЫ АДМИНУ
    for admin in ADMINS:
        sum=checkout.invoice_payload

        await bot.send_message(chat_id=admin,
                               text=f'Пользователь {checkout.from_user.full_name} сделал заказ на сумму {sum} RUB\nЕго корзина:')

        chatid = checkout.from_user.id
        zakaz = json.loads((await db.select_zakaz(chatid=(f'{chatid}',))).fetchone()[0])
        for i in zakaz:
            id = (f'{i}',)
            photo = (await db.select_photo(id)).fetchone()[0]
            caption = (await db.select_caption(id)).fetchone()[0]
            price = (await db.select_price(id)).fetchone()[0]

            await bot.send_photo(photo=photo, caption=caption + '\n\nЦена: ' + f'{price}', chat_id=admin)
        #ОБНУЛЕНИЕ КОРЗИНЫ ПОСЛЕ ОПЛАТЫ
        par = ('[]', chatid)
        await db.update_zakaz(par=par)

