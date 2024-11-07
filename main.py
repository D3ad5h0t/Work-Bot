import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import types


TOKEN = '7638178693:AAHWMhIW_6Xt5Gp2T5_pQ8fybWqthl_1DlE'
dp = Dispatcher()
bot = Bot(TOKEN)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # await message.answer(f'Hello, {message.from_user.full_name}')
    await message.reply('Hello!')

    # file = open('./pics/Space Octopus.png', 'rb')
    # await message.answer_photo(file)

@dp.message(Command('inline'))
async def info(message: Message) -> None:
    builder = InlineKeyboardBuilder()

    btn1 = InlineKeyboardButton(text='Site', callback_data='site')
    btn2 = InlineKeyboardButton(text='Hello', callback_data='hello')
    builder.add(btn1, btn2)

    await message.reply("Choose an option", reply_markup=builder.as_markup())


@dp.message(Command('reply'))
async def reply(message: Message) -> None:
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # markup.add(types.KeyboardButton(text='Site'))
    # markup.add(types.KeyboardButton(text="Website"))
    #
    # await message.reply("Choose an option", reply_markup=markup)
    builder = ReplyKeyboardBuilder()

    builder.button(text="Site")
    builder.button(text="Website")

    await message.reply("Choose an option", reply_markup=builder.as_markup())


async def callback_handler(callback_query: types.CallbackQuery) -> None:
    if callback_query.data == 'site':
        await callback_query.message.answer("You clicked Site")
    elif callback_query.data == 'hello':
        await callback_query.message.answer("You clicked Hello")

    await callback_query.answer()


async def main() -> None:
    dp.callback_query.register(callback_handler)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())