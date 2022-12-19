from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from os import listdir
from os.path import isfile, join

mypath = "data/testFiles"
btnMain = KeyboardButton('⬅️ Главное меню')


def get_names_files():
    return (f for f in listdir(mypath) if isfile(join(mypath, f)))


def gen_keybord():
    _activeTestKeybord = ReplyKeyboardMarkup(resize_keyboard=True)

    only_files = get_names_files()
    for file in only_files:
        button = KeyboardButton(file)
        _activeTestKeybord.add(button)

    _activeTestKeybord.add(btnMain)

    return _activeTestKeybord


activeTestKeybord = gen_keybord

# Main Menu
btnTest = KeyboardButton('📝 Посмотреть активные тесты')
btnTop = KeyboardButton('📈 Посмотреть рейтинг')
btnCode = KeyboardButton('♦️ Ввести код')
btnInfo = KeyboardButton('✉ Наши соцсети')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTest, btnTop, btnCode, btnInfo)

# Tests
btnFirst = KeyboardButton('🎄 Новогодний хакатон')
btnSecond = KeyboardButton('🍲 Beautiful Soup')
testsMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnFirst, btnSecond, btnMain)

# Tests 2
btnTg = KeyboardButton('📨 Телеграмм')
btnVk = KeyboardButton('👥 Вконтакте')
btnInst = KeyboardButton('📸 Инстаграмм')
tests2Menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTg, btnVk, btnInst, btnMain)
