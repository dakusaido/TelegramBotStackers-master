from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data.config import ADMINS_ID
from loader import dp
from states import Mail, Upload
from utils.sql_commands import select_users, get_list_student
import handlers.admin.makups as nav
from handlers.admin.createQR import createQR as cQR


@dp.message_handler(Text(equals='mail'), user_id=ADMINS_ID, state='*')
async def mail(message: types.Message):
    await message.answer(
        '<b>💌 Отправьте сообщение для рассылки:</b>'
    )
    await Mail.mail.set()


@dp.message_handler(state=Mail.mail, content_types=types.ContentType.ANY)
async def mail_on(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    if types.ContentType.TEXT == message.content_type:  # Если админ отправил текст
        for user in select_users():
            try:
                await dp.bot.send_message(
                    chat_id=user.tg_id,
                    text=message.html_text
                )
                await sleep(0.33)
            except Exception:
                pass
        else:
            await message.answer(
                '<b>✅ Рассылка завершена!</b>', reply_markup=nav.mainMenu
            )

    elif types.ContentType.PHOTO == message.content_type:  # Если админ отправил фото
        for user in select_users():
            try:
                await dp.bot.send_photo(
                    chat_id=user.tg_id,
                    photo=message.photo[-1].file_id,
                    caption=message.html_text if message.caption else None
                )
                await sleep(0.33)
            except Exception:
                pass
        else:
            await message.answer(
                '<b>✅ Рассылка завершена!</b>', reply_markup=nav.mainMenu
            )

    elif types.ContentType.VIDEO == message.content_type:  # Если админ отправил видео
        for user in select_users():
            try:
                await dp.bot.send_video(
                    chat_id=user.tg_id,
                    video=message.video.file_id,
                    caption=message.html_text if message.caption else None
                )
                await sleep(0.33)
            except Exception:
                pass
        else:
            await message.answer(
                '<b>✅ Рассылка завершена!</b>', reply_markup=nav.mainMenu
            )

    elif types.ContentType.ANIMATION == message.content_type:  # Если админ отправил gif
        for user in select_users():
            try:
                await dp.bot.send_animation(
                    chat_id=user.tg_id,
                    animation=message.animation.file_id,
                    caption=message.html_text if message.caption else None
                )
                await sleep(0.33)
            except Exception:
                pass
        else:
            await message.answer(
                '<b>✅ Рассылка завершена!</b>', reply_markup=nav.mainMenu
            )
    elif types.ContentType.STICKER == message.content_type:  # Если админ отправил sticker
        for user in select_users():
            try:
                await dp.bot.send_sticker(
                    chat_id=user.tg_id,
                    sticker=message.sticker.file_id,
                )
                await sleep(0.33)
            except Exception:
                pass
        else:
            await message.answer(
                '<b>✅ Рассылка завершена!</b>', reply_markup=nav.mainMenu
            )

    else:
        await message.answer(
            '<b>❗️ Данный формат контента не поддерживается для рассылки!</b>', reply_markup=nav.mainMenu
        )


@dp.message_handler(commands=['create_QR'], user_id=ADMINS_ID, state='*')
async def createQR(message: types.Message):
    cQR()  # IM DOING IT
    await sleep(2)
    await message.answer_photo(
        photo=open('qr_code/1.png', 'rb')
    )


@dp.message_handler(commands=['uploadTest'], user_id=ADMINS_ID, state='*', content_types=types.ContentType.TEXT)
async def uploadTest(message: types.Message):
    await message.answer(
        '<b>Выберите тип файла: </b>', reply_markup=nav.CSVFile
    )

    await Upload.uploading.set()


@dp.message_handler(state=Upload.uploading, content_types=types.ContentType.TEXT)
async def upload_on(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)

    if message.text == '⬅️ Главное меню.':
        await message.answer('⬅️ Главное меню', reply_markup=nav.mainMenu)
        return

    elif message.text == "Загрузить CSV файл":
        await message.answer("Загрузите CSV файл")
        await state.set_state(Upload.uploading.state)

    else:
        await message.reply('Неизвестная команда')


@dp.message_handler(state=Upload.uploading, content_types=types.ContentType.DOCUMENT)
async def upload_CSV(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)

    if message.document.file_name[-4:] != '.csv':
        await message.answer("Загрузите файл правильного типа!", reply_markup=nav.CSVFile)
        return

    try:
        await message.answer(f"Загрузка документа {message.document.file_name}")
        await message.document.download(destination_file=f"data/testFiles/{message.document.file_name}")
    except Exception() as e:
        print(e)
        await message.answer('Упс... Произошла ошибка')
    else:
        await message.answer('Файл успешно загружен', reply_markup=nav.mainMenu)


@dp.message_handler(commands=['getStudentList'], user_id=ADMINS_ID, state='*', content_types=types.ContentType.TEXT)
async def getStudentList(message: types.Message):
    try:
        lst = get_list_student()
    except:
        await message.answer("Что-то пошло не так...")
        return

    output_text = ""
    i = 1
    for user in lst:

        if i > 5:
            break

        output_text += f"{i}. {user.tg_id} | {user.second_name} {user.first_name} | {user.result}\n"

        i += 1

    await message.answer(output_text, reply_markup=nav.mainMenu)


@dp.message_handler(commands=['menu'], user_id=ADMINS_ID)
async def command_menu(message: types.Message):
    await message.answer('Главное Меню', reply_markup=nav.mainMenu)


@dp.message_handler(user_id=ADMINS_ID)
async def bot_message(message: types.Message):
    if message.text == '⬅️ Главное меню.':
        await message.answer('⬅️ Главное меню', reply_markup=nav.mainMenu)

    elif message.text == '♦️ Создать код':
        await createQR(message)

    elif message.text == "Отправить уведомление":
        await mail(message)

    elif message.text == "Загрузить тест":
        await uploadTest(message)

    elif message.text == "Получить список лучших студентов":
        await getStudentList(message)

    else:
        await message.reply('Неизвестная команда')
