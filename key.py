from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from data_car import *
from config import admin


# НАСТРОЙКИ  если ви хотите изменить текст кнопки, то сначало смените тут и обязательно смените текст (который ви сменили здесь) в файле main.py


def appliences(url):
	key = InlineKeyboardMarkup()
	b1 = InlineKeyboardButton(text='📲 Відкрити сайт', url=url)
	b2 = InlineKeyboardButton(text='🚗Відкрити базар', url='https://t.me/kym_avtobazar')
	b3 = InlineKeyboardButton(text='Змінити або зупинити пошук', callback_data='change')
	b4 = InlineKeyboardButton(text='🚀 Продати своє авто', callback_data='auto')
	b5 = InlineKeyboardButton(text="⛑ Підтримати Кум'а", callback_data='give')
	key.insert(b1)
	key.insert(b2)
	key.row(b3)
	key.row(b4)
	key.insert(b5)
	return key

def pay_and_check(idd, url):
	key = InlineKeyboardMarkup()
	b1 = InlineKeyboardButton(text='💵 Оплатити', url=url)
	b2 = KeyboardButton(f'👨🏻‍💻 Перевірити оплату', callback_data=f'check:{idd}')
	b3 = KeyboardButton(f'⬅️ Назад', callback_data=f'back')
	key.row(b1)
	key.row(b2)
	key.row(b3)
	return key

def pay_and_check_f(idd, url):
	key = InlineKeyboardMarkup()
	b1 = InlineKeyboardButton(text='💵 Оплатити', url=url)
	b2 = KeyboardButton(f'👨🏻‍💻 Перевірити оплату', callback_data=f'check:{idd}')
	b3 = KeyboardButton(f'⬅️ Назад', callback_data=f'back_f')
	key.row(b1)
	key.row(b2)
	key.row(b3)
	return key

def pay_and_check_help(idd, url):
	key = InlineKeyboardMarkup()
	b1 = InlineKeyboardButton(text='Допомогти ✅', url=url)
	b2 = KeyboardButton(f'👨🏻‍💻 Перевірити оплату', callback_data=f'help:{idd}')
	b3 = KeyboardButton(f'⬅️ Назад', callback_data=f'back')
	key.row(b1)
	key.row(b2)
	key.row(b3)
	return key

def pay_and_check_sell_auto(idd, url):
	key = InlineKeyboardMarkup()
	b1 = InlineKeyboardButton(text='💵 Оплатити', url=url)
	b2 = KeyboardButton(f'👨🏻‍💻 Перевірити оплату', callback_data=f'sell:{idd}')
	b3 = KeyboardButton(f'⬅️ Назад', callback_data=f'back')
	key.row(b1)
	key.row(b2)
	key.row(b3)
	return key

def options():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton(f'Змінити або зупинити пошук')
	b2 = KeyboardButton(f'Обновити пакет послуг')
	key.row(b1)
	key.row(b2)
	return key

def status(idd):
	if idd in admin:
		key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
		b1 = KeyboardButton(f'Бізнес')
		b2 = KeyboardButton(f'Безкоштовний')
		key.insert(b1)
		key.insert(b2)
	return key

def are_u_sure():
	if True:
		key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
		b1 = KeyboardButton(f'Так')
		b2 = KeyboardButton(f'Назад')
		key.insert(b1)
		key.insert(b2)
	return key

def mailing(idd):
	if idd in admin:
		key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
		b1 = KeyboardButton('Всім користувачам')
		b2 = KeyboardButton('По марці авто')
		b3 = KeyboardButton('По гео')
		b4 = KeyboardButton('По рік (від)')
		b5 = KeyboardButton('По статусу пакета (Бізнес чи Безкоштовний)')
		b6 = KeyboardButton('Назад')
		key.insert(b1)
		key.insert(b2)
		key.insert(b3)
		key.insert(b4)
		key.insert(b5)
		key.row(b6)
	return key

def admin_panel():
	if True:
		key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False) #one_tme_keyboard=True
		b1 = KeyboardButton('Розсилка')
		b2 = KeyboardButton('Старт пошука для Безкоштовних пакетів')
		b3 = KeyboardButton('Старт пошука для Бізнес пакетів')
		b4 = KeyboardButton('Стоп')
		b5 = KeyboardButton('Налаштування')
		key.row(b1)
		key.row(b2)
		key.row(b3)
		key.row(b4)
		key.row(b5)
	return key

def settings():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton(f'Змінити ціну на бізнес акк')
	b2 = KeyboardButton(f'Змінити ціну на "Продати авто"')
	b3 = KeyboardButton(f'Змінити нік менеджера')
	b4 = KeyboardButton(f"Скачати excel файл")
	b5 = KeyboardButton(f"Назад")
	key.row(b1)
	key.row(b2)
	key.row(b3)
	key.row(b4)
	key.row(b5)
	return key

def change_search():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton(f'Змінити або зупинити пошук')
	b2 = KeyboardButton(f'👍 Змінити тариф пошуку')
	b3 = KeyboardButton(f'🚀 Продати своє авто')
	b4 = KeyboardButton(f"⛑ Підтримати Кум'а")
	key.row(b1)
	key.insert(b2)
	key.row(b3)
	key.row(b4)
	return key

def change_search_100():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton(f'Змінити або зупинити пошук')
	b3 = KeyboardButton(f'🚀 Продати своє авто')
	b4 = KeyboardButton(f"⛑ Підтримати Кум'а")
	key.row(b1)
	key.row(b3)
	key.row(b4)
	return key

def back():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b3 = KeyboardButton('⬅️ Назад')
	key.row(b3)
	return key


def help():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton("⛑ Підтримати Кум'а")
	b2 = KeyboardButton('🚀 Продати своє авто')
	b3 = KeyboardButton('⬅️ Назад')
	key.row(b1)
	key.row(b2)
	key.row(b3)
	return key

def why_stop():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton(f'😎Знайшов авто через бот')
	b2 = KeyboardButton(f'😢Знайшов у іншому місці')
	b7 = KeyboardButton(f'😔Більше не шукаю')
	b8 = KeyboardButton(f'🥺Бот не зручний')
	b9 = KeyboardButton(f'🙃Включив з цікавості')
	b10 = KeyboardButton(f'⬅️ Назад')
	key.row(b7)
	key.row(b8)
	key.row(b9)
	key.row(b1)
	key.row(b2)
	key.row(b10)
	return key

def choice_change_с():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton(f'🕵 Змінити пошук')
	b2 = KeyboardButton(f'⛔️ Зупинити пошук')
	key.insert(b1)
	key.insert(b2)
	return key

def choice_change():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton(f'🕵 Змінити пошук')
	b2 = KeyboardButton(f'⛔️ Зупинити пошук')
	b3 = KeyboardButton(f'🚀 Продати своє авто')
	key.insert(b1)
	key.insert(b2)
	key.row(b3)
	return key

def change_pocket():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton(f'✅ Вибрати бізнес пошук')
	b2 = KeyboardButton(f'✅ Вибрати безкоштовний пошук')
	b3 = KeyboardButton(f'⬅️ Назад')
	key.insert(b1)
	key.insert(b2)
	key.row(b3)
	return key

def search():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton(f'🕵🏻 Безкоштовний пошук')
	b2 = KeyboardButton(f'👩🏻‍🚀 Бізнес пошук')
	key.insert(b1)
	key.insert(b2)
	return key

def main_u():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton(f'✅ Почати пошук')
	key.insert(b1)
	return key
def main_u_canc():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	b1 = KeyboardButton(f'✅ Почати пошук')
	b10 = KeyboardButton(f'⬅️ Повернутись')
	key.row(b1)
	key.row(b10)
	return key

def geo():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_tme_keyboard=True
	for i in geo_list:
		b1= KeyboardButton(f'{i}')
		key.insert(b1)
	return key

def mark():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_time_keyboard=True
	for i in all_marks:
		b1 = KeyboardButton(f'{i}')
		key.insert(b1)
	return key

def type_mark(type_mark_list):
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_time_keyboard=True
	for i in type_mark_list:
		b1 = KeyboardButton(f'{i}')
		key.insert(b1)
	return key

def price_from():
	l = [1000, 2000, 3000, 4000, 5000, 7000, 9000, 10000, 12500, 15000, 20000, 22500, 25000, 27500, 30000, 35000, 40000, 45000, 50000, 60000, 70000]
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_time_keyboard=True
	for i in l:
		b1 = KeyboardButton(f"{i}")
		key.insert(b1)
	return key

def price_to():
	l = [1000, 2000, 3000, 4000, 5000, 7000, 9000, 10000, 12500, 15000, 20000, 22500, 25000, 27500, 30000, 35000, 40000, 45000, 50000, 60000, 70000]
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_time_keyboard=True
	for i in l:
		b1 = KeyboardButton(f"{i}")
		key.insert(b1)
	return key

def mileagr_to():
	l = [0, 1000, 5000, 10000, 25000, 50000, 75000, 100000, 125000, 150000, 175000, 200000, 250000, 300000, 300000]
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_time_keyboard=True
	for i in l:
		b1 = KeyboardButton(f"{i}")
		key.insert(b1)
	return key

def year_from():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_time_keyboard=True
	for i in range(2005,2022):
		b1 = KeyboardButton(f"{i}")
		key.insert(b1)
	return key

def year_to():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_time_keyboard=True
	for i in range(2005,2022):
		b1 = KeyboardButton(f"{i}")
		key.insert(b1)
	return key

def petrol():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_time_keyboard=True
	b1 = KeyboardButton(f'Бензин')
	key.insert(b1)
	b1 = KeyboardButton(f'Дизель')
	key.insert(b1)
	b1 = KeyboardButton(f'Газ / бензин')
	key.insert(b1)
	b1 = KeyboardButton(f'Електро')
	key.insert(b1)
	b1 = KeyboardButton(f'Гібрид')
	key.insert(b1)
	b1 = KeyboardButton(f'Будь яке')
	key.insert(b1)
	return key

def kpp():
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_time_keyboard=True
	b1 = KeyboardButton(f'Механічна')
	key.insert(b1)
	b1 = KeyboardButton(f'Автоматична')
	key.insert(b1)
	b1 = KeyboardButton(f'Варіатор')
	key.insert(b1)
	b1 = KeyboardButton(f'Адаптивна')
	key.insert(b1)
	b1 = KeyboardButton(f'Типтронік')
	key.insert(b1)
	b1 = KeyboardButton(f'Будь яке')
	key.insert(b1)
	return key