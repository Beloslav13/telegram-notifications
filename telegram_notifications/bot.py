import logging
from threading import Thread
from time import sleep
import time
import aiogram.utils.markdown as md
import schedule
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from vkontakte_api.vkontakte import VkontaktePublication

logging.basicConfig(level=logging.INFO)

API_TOKEN = '1079047912:AAF3XlI6BFZ8-PVYHxspWEF-mi8TYrdUtGY'


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    init = State()
    send = State()
    exit = State()
    help = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.init.set()
    print(message)
    await message.reply("Привет, кидай ссылку на какое сообщество(человека) нужно подписаться?")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    schedule.cancel_job(job())
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


publications = []


def job(vk=None):
    global publications
    publications = vk.get_publications()


@dp.message_handler(state=Form.init)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['url'] = message.text
    print(data)
    await Form.next()
    await message.reply("Подписался, проверка новых публикаций производится каждые 15 минут...")

    result = []
    vk = VkontaktePublication(data['url'])
    # schedule.every(5).seconds.do(job, vk)
    # while 1:
    #     schedule.run_pending()
    #     time.sleep(5)
    #     print('&&&&&&&&&&', message)
    #     print('STATE', state.proxy())
    #     print('PUB===', publications)
    #     if publications:
    #         print('result====', result)
    #         for publication in publications:
    #             if not result:
    #                 print('not result')
    #                 await message.answer(publication)
    #                 result.append(publication)
    #             elif publication not in result:
    #                 print('send pub=====')
    #                 await message.answer(publication)
    #                 result.append(publication)
    #             elif publication in result:
    #                 print('break pub')
    #                 break
    #             time.sleep(2)
    #             print('!!!!!!!!!11', result)
    #     else:
    #         print('else')
    #         result = []


@dp.message_handler(state=Form.send)
async def process_name(message: types.Message, state: FSMContext):
    print('=====send=====')
    print(message)
    schedule.cancel_job(job())
    await state.finish()

# # Check age. Age gotta be digit
# @dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
# async def process_age_invalid(message: types.Message):
#     """
#     If age is invalid
#     """
#     return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")
#
#
# @dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
# async def process_age(message: types.Message, state: FSMContext):
#     # Update state and data
#     await Form.next()
#     await state.update_data(age=int(message.text))
#
#     # Configure ReplyKeyboardMarkup
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
#     markup.add("Male", "Female")
#     markup.add("Other")
#
#     await message.reply("What is your gender?", reply_markup=markup)
#
#
# @dp.message_handler(lambda message: message.text not in ["Male", "Female", "Other"], state=Form.gender)
# async def process_gender_invalid(message: types.Message):
#     """
#     In this example gender has to be one of: Male, Female, Other.
#     """
#     return await message.reply("Bad gender name. Choose your gender from the keyboard.")
#
#
# @dp.message_handler(state=Form.gender)
# async def process_gender(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['gender'] = message.text
#
#         # Remove keyboard
#         markup = types.ReplyKeyboardRemove()
#
#         # And send message
#         await bot.send_message(
#             message.chat.id,
#             md.text(
#                 md.text('Hi! Nice to meet you,', md.bold(data['name'])),
#                 md.text('Age:', md.code(data['age'])),
#                 md.text('Gender:', data['gender']),
#                 sep='\n',
#             ),
#             reply_markup=markup,
#             parse_mode=ParseMode.MARKDOWN,
#         )
#
#     # Finish conversation
#     await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
