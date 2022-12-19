from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from asyncio import sleep

from loader import dp, bot
from utils.sql_commands import register_user
import handlers.users.makups as nav
from handlers.admin.makups import mainMenu as adminMainMenu
from data.config import ADMINS_ID
from states.user import Read, RegUser
from utils.sql_commands import add_coin_user, get_user, send_result_ques, rank_counter
# from utils.Helper import Helper
from csv import reader

# rep_helper = Helper(0)
# coin = 0


@dp.message_handler(CommandStart(), state='*')
async def start_bot(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS_ID:
        await message.answer(
            'Привет, Владелец!', reply_markup=adminMainMenu
        )
        return

    await message.answer(
        'Привет!\nВведите свое имя и фамилию для регистрации'
    )

    await RegUser.reg_user.set()


@dp.message_handler(state=RegUser.reg_user, content_types=types.ContentType.TEXT)
async def reg_user(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)

    if (user := message.text.split(' ')).__len__() == 2:
        register_user(tg_id=message.from_user.id, first_name=user[0], second_name=user[1])
        await message.answer("Регистрация прошла успешно!", reply_markup=nav.mainMenu)

    else:
        await message.answer("Упс... Что-то пошло не так, попробуйте еще.")


@dp.message_handler(commands=['includeKey'], state='*')
async def readKey(message: types.Message):
    await message.answer("Введите ключ")
    await Read.reading.set()


@dp.message_handler(state=Read.reading, content_types=types.ContentType.TEXT)
async def readKey_on(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    if types.ContentType.TEXT == message.content_type:
        file = open('qr_code/key.txt', 'r')

        await sleep(1)

        if file.read().strip() == message.text.strip():
            add_coin_user(message.from_user.id, 1)
            await message.answer("Спасибо что сегодня пришли!")
        else:
            await message.answer("Увы... Ключ не тот")

        file.close()

    else:
        await message.answer(
            '<b>❗️ Данный формат контента не поддерживается!</b>'
        )


@dp.message_handler(commands=['menu'])
async def command_menu(message: types.Message):
    await message.answer('Главное Меню', reply_markup=nav.mainMenu)


# @dp.poll_answer_handler()
# async def pool_action(poll_answer: types.PollAnswer):
#     pool = await bot.stop_poll(chat_id=poll_answer.user.id, message_id=rep_helper.get_msg())
#     global coin
#     if pool.options.__getitem__(pool.correct_option_id)["voter_count"] == 1:
#         coin += 1


@dp.message_handler(commands=['createQuiz'], state='*')
async def createQuiz(message: types.Message):
    # global coin
    coin = 0
    questions_count = 0
    lst_msg_id = []
    with open('data/testFiles/' + message.text, mode='r', encoding='utf-8') as file:
        csv_writer = reader(file)
        for res in csv_writer:
            if res:
                msg = await message.answer_poll(question=res[0][:100], options=res[1:-1],
                                                is_anonymous=False,
                                                correct_option_id=res[1:-1].index(res[-1]), type=types.PollType.QUIZ)
                lst_msg_id.append(msg.message_id)
                questions_count += 1
                await sleep(8)

    for msg_id in lst_msg_id:
        pool = await bot.stop_poll(chat_id=message.from_user.id, message_id=msg_id)

        if pool.options.__getitem__(pool.correct_option_id)["voter_count"] == 1:
            coin += 1

    await message.answer(f"Тест Завершен. Кол-во Баллов {coin} из {questions_count}", reply_markup=nav.mainMenu)
    send_result_ques(message.from_user.id, coin, questions_count)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == '⬅️ Главное меню':
        await message.answer('⬅️ Главное меню', reply_markup=nav.mainMenu)

    elif message.text == '📈 Посмотреть рейтинг':

        user_b = 0

        try:
            user_b = rank_counter(message.from_user.id)
        except:
            pass
        await message.answer(f"Ваш рейтинг - {user_b}")

    elif message.text == '♦️ Ввести код':
        await readKey(message)

    elif message.text == '✉ Наши соцсети':
        await message.answer('✉ Наши соцсети', reply_markup=nav.tests2Menu)

    elif message.text == '📨 Телеграмм':
        await message.answer('Телеграмм - https://t.me/stackers_team')

    elif message.text == '👥 Вконтакте':
        await message.answer('Вконтакте - https://vk.com/stackers.team')

    elif message.text == '📸 Инстаграмм':
        await message.answer('Инстаграмм - https://www.instagram.com/stackers.team/')

    elif message.text == '📝 Посмотреть активные тесты':
        await message.answer('📝 Активные тесты', reply_markup=nav.activeTestKeybord())
    #
    # elif message.text == '🎄 Новогодний хакатон':
    #     await message.answer('🎄 Новогодний хакатон - какой-то тест №1')
    #
    # elif message.text == '🍲 Beautiful Soup':
    #     await message.answer('🍲 Beautiful Soup - какой-то тест №2')

    elif message.text in nav.get_names_files():
        await createQuiz(message)

    else:
        await message.reply('Неизвестная команда')
