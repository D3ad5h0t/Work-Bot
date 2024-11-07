import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo

TOKEN = '7638178693:AAHWMhIW_6Xt5Gp2T5_pQ8fybWqthl_1DlE'
dp = Dispatcher()
bot = Bot(TOKEN)


@dp.message(Command('start'))
async def start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="Открыть веб страницу", web_app=WebAppInfo(url='https://itproger.com/'))

    await message.reply('Привет, мой друг!', reply_markup=builder.as_markup())


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())