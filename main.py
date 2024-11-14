import asyncio
import logging
import time
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
import config
from db import DataBase
import day_conf

db = DataBase("db.db")
bot = Bot(token=config.TOKEN)
dp = Dispatcher()
stat = 0

class Form(StatesGroup):
    mailing_message = State()

@dp.message(CommandStart())
async def send_welcome(message: Message):
    if message.chat.type == "private":
        if db.user_info(message.from_user.id):
            await message.reply(config.ALREADY_MESSAGE_TXT)
        else:
            db.add_user(message.from_user.id) 
            await message.answer(config.START_MESSAGE_TXT, parse_mode=ParseMode.HTML)
    else: 
        if db.user_info(message.chat.id):
            await message.reply(config.ALREADY_MESSAGE_TXT)
        else:
            db.add_user(message.chat.id) 
            await message.answer(config.START_MESSAGE_TXT, parse_mode=ParseMode.HTML)

@dp.message(Command('admin_help'))
async def admin_help(message: Message):
    if message.from_user.id in db.list_admin():
        await message.reply(f'Ти можеш попросити допомоги у @dixtri136, чи сам знайти відповідь на питання <a href="https://telegra.ph/Pravila-ispolzovaniya-admin-komand-v-Shedule-23-Bot-11-09"> тут </a>', parse_mode=ParseMode.HTML)
    else:
        await message.reply(config.ADMIN_ERROR_TXT, parse_mode=ParseMode.HTML)

@dp.message(Command('all'))
async def all_commands(message: Message):
    if message.from_user.id in db.list_admin():
        if message.chat.type == "private":
            await message.reply(config.ALL_ADMIN_COMMANDS, parse_mode=ParseMode.HTML)
        else:
            await message.answer(config.ALL_COMMANDS_TXT, parse_mode=ParseMode.HTML)
    else:
        await message.answer(config.ALL_COMMANDS_TXT, parse_mode=ParseMode.HTML)

@dp.message(Command('teachers'))
async def all_teachers(message: Message):
    await message.reply(config.TEACHERS_LIST_MESSAGE_TXT + db.all_teacher(), parse_mode=ParseMode.HTML)

@dp.message(Command('links'))
async def all_links(message: Message):
    await message.reply(config.LINKS_LIST_MESSAGE_TXT + db.all_link(), parse_mode=ParseMode.HTML)

@dp.message(Command('schedule'))
async def send_schedule(message: Message):
    if len(day_conf.id_days("schedule")) <= 40:
        await message.reply(day_conf.id_days("schedule"))
    else:
        await message.reply(config.SCHEDULE_TODAY_TXT + day_conf.id_days("schedule"), parse_mode=ParseMode.HTML)  

@dp.message(Command('schedule_tomorrow'))
async def send_schedule_tomorrow(message: Message):
    if len(day_conf.id_days("schedule_tomorrow")) <= 40:
        await message.reply(day_conf.id_days("schedule_tomorrow"))
    else:
        await message.reply(config.SCHEDULE_TOMORROW_TXT + day_conf.id_days("schedule_tomorrow"), parse_mode=ParseMode.HTML)  

@dp.message(Command('mailing'))
async def mailing(message: Message, state: FSMContext):
    if message.from_user.id in db.list_admin():
        try:
            if message.chat.type == "private":
                await message.answer("Введіть інформацію для розсилки:")
                await state.set_state(Form.mailing_message)
            else: 
                await message.reply(config.TYPE_CHAT_ERROR)
        except Exception as ex:
            await message.reply(f"Виникла помилка: {ex}")
    else:
        await message.reply(config.ADMIN_ERROR_TXT)

@dp.message(Command('schedule_update'))
async def schedule_update(message: Message, command: CommandObject):
    if message.from_user.id in db.list_admin():
        try:
            if message.chat.type: 
                txt = command.args.split("|")
                await message.reply(db.schedule_update(int(txt[0]), txt[1],  txt[2]))
            else: 
                await message.reply(config.TYPE_CHAT_ERROR)
        except Exception as ex:
            await message.reply(f"Виникла помилка: {ex}")
    else:
        await message.answer(config.ADMIN_ERROR_TXT)

@dp.message(Command('update_link'))
async def link_updating(message: Message, command: CommandObject):
    if message.from_user.id in db.list_admin():
        try:
            if message.chat.type == "private":
                txt = command.args.split("|")
                await message.reply(db.link_update(int(txt[0]), txt[1]))
            else:
                await message.reply(config.TYPE_CHAT_ERROR)
        except Exception as ex:
            await message.reply(f"Виникла помилка: {ex}")
    else:
        await message.reply(config.ADMIN_ERROR_TXT)

@dp.message(Command('add_admin'))
async def add_admin(message: Message, command: CommandObject):
    if message.from_user.id in db.list_admin():
        try:
            if message.chat.type == "private":
                txt = command.args.split("|")
                await message.reply(db.add_admin(int(txt[0])))
            else:
                await message.reply(config.TYPE_CHAT_ERROR)
        except Exception as ex:
            await message.reply(f"Виникла помилка: {ex}")
    else:
        await message.reply(config.ADMIN_ERROR_TXT)

@dp.message(Form.mailing_message)
async def mailing_message(message: Message, state: FSMContext):
    try:
        for i in db.all_user_id():
            try:
                await message.copy_to(chat_id=int(i[0]))
            except Exception as ex:
                if ex == "Telegram server says - Bad Request: chat not found":
                    time.sleep(2)
        await message.reply("Розсилка успішно завершено!")
        await state.clear()
    except Exception as ex:
        await message.reply(f"Виникла помилка: {ex}")
        await state.clear()


@dp.message()
async def messages_text(message: Message):
    if message.chat.type == "private":
        await message.reply(config.TEXT_ERROR_TXT)
    else:
        pass

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="logging.log", encoding="utf-8", filemode="w")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit!")