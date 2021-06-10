# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.callback_query import CallbackQuery
from time import sleep
import random
import datetime
import asyncio
import time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardRemove
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import json 
import random

from pay_script import *
from config import api, admin
from data_car import dict_mark_car, dict_petrol, dict_kpp, dict_geo, dict_kpp_my, dict_petrol_my, dict_kpp_ria, dict_petrol_ria, reg_ria, dict_ria_marks, dict_ria_type_mark
from key import *
from db import *
from db_setup import add_setup, take_setup,upd_men,upd_cost,upd_cost_sell_auto

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

command1 = ''
command2 = ''

menedger = 'jaroskot'
cost = 30
cost_sell_auto = 15

add_setup(menedger, cost, cost_sell_auto)

all_user={}

class data_of_car(StatesGroup):
	geo = State() #Вкажіть область для пошуку
	price_from = State() #Вкажіть вартість авто в  доларх від
	price_to = State() #Вкажіть вартість авто в  доларх до
	mark = State() #Вкажіть бренд для пошуку
	type_mark = State() #Вкажіть модель для пошуку
	year_from = State() #Вкажіть рік авто для пошуку від:
	year_to = State() #Вкажіть рік авто для пошуку до:
	petrol = State() #Вкажіть тип пального:
	kpp = State() #Вкажіть тип КПП:
	mielege_from = State() #Вкажіть пробігв від: "Приклад 10000"
	mielege_to = State() #Вкажіть пробіг до: "Приклад 10000"

class mail(StatesGroup):
	way = State()
	info = State()
	sms = State()

class change_setup(StatesGroup):
	what = State()
	info = State()

async def olx(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE):
	if MARK == 'Будь-яка':
		MARK = ''
		TYPE_OF_MARK = ''		
	
	if TYPE_OF_MARK == 'Будь-якa' or 'будь-яка' == TYPE_OF_MARK:
		TYPE_OF_MARK = ''		

	if TYPE_OF_FUEL == 'Будь яке':
		general_request_olx = f'https://www.olx.ua/uk/transport/legkovye-avtomobili/{MARK}/{TYPE_OF_MARK}/{REGION}/?search[filter_float_price:from]={FROM_PRICE}&search[filter_float_price:to]={TO_PRICE}&search[filter_float_motor_year:from]={FROM_YEAR}&search[filter_float_motor_year:to]={TO_YEAR}&search[filter_float_motor_mileage:from]={FROM_MILEAGE}&search[filter_float_motor_mileage:to]={TO_MILEAGE}?search[filter_enum_transmission_type][0]={KPP}&currency=USD'
	
	if KPP == 'Будь яке':
		general_request_olx = f'https://www.olx.ua/uk/transport/legkovye-avtomobili/{MARK}/{TYPE_OF_MARK}/{REGION}/?search[filter_float_price:from]={FROM_PRICE}&search[filter_float_price:to]={TO_PRICE}&search[filter_float_motor_year:from]={FROM_YEAR}&search[filter_float_motor_year:to]={TO_YEAR}&search[filter_enum_fuel_type][0]={TYPE_OF_FUEL}&search[filter_float_motor_mileage:from]={FROM_MILEAGE}&search[filter_float_motor_mileage:to]={TO_MILEAGE}&currency=USD'
	
	# FUEL AND KPP
	if TYPE_OF_FUEL == 'Будь яке' and KPP == 'Будь яке':
		general_request_olx = f'https://www.olx.ua/uk/transport/legkovye-avtomobili/{MARK}/{TYPE_OF_MARK}/{REGION}/?search[filter_float_price:from]={FROM_PRICE}&search[filter_float_price:to]={TO_PRICE}&search[filter_float_motor_year:from]={FROM_YEAR}&search[filter_float_motor_year:to]={TO_YEAR}&search[filter_float_motor_mileage:from]={FROM_MILEAGE}&search[filter_float_motor_mileage:to]={TO_MILEAGE}&currency=USD'	

	# ALL
	if TYPE_OF_FUEL != 'Будь яке' and KPP != 'Будь яке':
		general_request_olx = f'https://www.olx.ua/uk/transport/legkovye-avtomobili/{MARK}/{TYPE_OF_MARK}/{REGION}/?search[filter_float_price:from]={FROM_PRICE}&search[filter_float_price:to]={TO_PRICE}&search[filter_float_motor_year:from]={FROM_YEAR}&search[filter_float_motor_year:to]={TO_YEAR}&search[filter_enum_fuel_type][0]={TYPE_OF_FUEL}&search[filter_float_motor_mileage:from]={FROM_MILEAGE}&search[filter_float_motor_mileage:to]={TO_MILEAGE}?search[filter_enum_transmission_type][0]={KPP}&currency=USD'

	print(general_request_olx)
	res = requests.get(general_request_olx)
	soup = BeautifulSoup(res.content, 'html.parser')
	r = soup.find_all('div',class_='offer-wrapper')
	no = soup.find_all('div',class_='wrapper')
			#print(no)
			#print()
	if 'Нічого' in no[3].get_text(strip=True):
		return 'Немає'
			
	if r:
		data = []
		for i in r:
			link = i.find('h3').find('a').get('href')
			data.append(link)
		return data
	else:
		return 'Немає'

async def my(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE):
	if TYPE_OF_FUEL == 'Будь яке':
		link = f'https://mymycars.com/catalog/page=1;o=propulsionAt:desc;category=legkovi;bm=price:{FROM_PRICE}00,{TO_PRICE}00&mileage:{FROM_MILEAGE},{TO_MILEAGE}&year:{FROM_YEAR},{TO_YEAR}&brand:{MARK}&model:{MARK}-{TYPE_OF_MARK};c=kpp:{KPP};region={REGION}'
	if KPP == 'Будь яке':
		link = f'https://mymycars.com/catalog/page=1;o=propulsionAt:desc;category=legkovi;fuelType={TYPE_OF_FUEL};bm=price:{FROM_PRICE}00,{TO_PRICE}00&mileage:{FROM_MILEAGE},{TO_MILEAGE}&year:{FROM_YEAR},{TO_YEAR}&brand:{MARK}&model:{MARK}-{TYPE_OF_MARK};region={REGION}'		
	if TYPE_OF_FUEL == 'Будь яке' and KPP == 'Будь яке':
		link = f'https://mymycars.com/catalog/page=1;o=propulsionAt:desc;category=legkovi;bm=price:{FROM_PRICE}00,{TO_PRICE}00&mileage:{FROM_MILEAGE},{TO_MILEAGE}&year:{FROM_YEAR},{TO_YEAR}&brand:{MARK}&model:{MARK}-{TYPE_OF_MARK};region={REGION}'

	if 'Будь-якa' == TYPE_OF_MARK or 'будь-яка' == TYPE_OF_MARK:
		link = f'https://mymycars.com/catalog/page=1;o=propulsionAt:desc;category=legkovi;fuelType={TYPE_OF_FUEL};bm=price:{FROM_PRICE}00,{TO_PRICE}00&mileage:{FROM_MILEAGE},{TO_MILEAGE}&year:{FROM_YEAR},{TO_YEAR}&brand:{MARK};c=kpp:{KPP};region={REGION}'
	if ('Будь-якa' == TYPE_OF_MARK or 'будь-яка' == TYPE_OF_MARK) and TYPE_OF_FUEL == 'Будь яке' and KPP == 'Будь яке':
		link = f'https://mymycars.com/catalog/page=1;o=propulsionAt:desc;category=legkovi;bm=price:{FROM_PRICE}00,{TO_PRICE}00&mileage:{FROM_MILEAGE},{TO_MILEAGE}&year:{FROM_YEAR},{TO_YEAR}&brand:{MARK};region={REGION}'

	if 'Будь-якa' != TYPE_OF_MARK and 'будь-яка' != TYPE_OF_MARK and TYPE_OF_FUEL != 'Будь яке' and KPP != 'Будь яке':
		link = f'https://mymycars.com/catalog/page=1;o=propulsionAt:desc;category=legkovi;fuelType={TYPE_OF_FUEL};bm=price:{FROM_PRICE}00,{TO_PRICE}00&mileage:{FROM_MILEAGE},{TO_MILEAGE}&year:{FROM_YEAR},{TO_YEAR}&brand:{MARK}&model:{MARK}-{TYPE_OF_MARK};c=kpp:{KPP};region={REGION}'
	print(f'LINK: {link}')
	#link = 'https://mymycars.com/catalog/page=1;o=propulsionAt:desc;category=legkovi;bm=price:30000,2350000000&mileage:,100000&year:2017,2021&brand:audi&model:audi-a4;region=12'
	options = Options()
	options.add_argument('--disable-gpu')
	options.add_argument("--disable-dev-shm-usage")
	#options.add_argument("start-maximized")
	options.add_argument("disable-infobars")
	options.add_argument("--disable-extensions")
	options.add_argument("--no-sandbox")
	options.add_argument('--headless')
	dr = webdriver.Chrome(chrome_options = options)
	dr.get(link)
	data = dr.find_elements_by_class_name('catalog-product__title-link')
	#await asyncio.sleep(6)
	dr.execute_script("window.stop();")
	try:
		dr.find_element_by_class_name('no-data-info__title').text
		print('NOOOOOOOOOOO')
		dr.close()
		return 'Немає'
	except:
		res = []
		for i in data:
			if i in res:
				continue
			res.append(i.get_attribute("href"))
		for i in res:
			print(i+'\n\n'+100*'*')
		dr.close()
		return res

async def ria(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE):
		if MARK == 'Будь-яка':
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&type[0]={TYPE_OF_FUEL}&gearbox[0]={KPP},&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'
		if TYPE_OF_MARK == 'Будь-якa' or 'будь-яка' == TYPE_OF_MARK:
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&marka_id[0]={MARK}&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&type[0]={TYPE_OF_FUEL}&gearbox[0]={KPP},&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'			
		if TYPE_OF_FUEL == 'Будь яке':
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&marka_id[0]={MARK}&model_id[0]={TYPE_OF_MARK}&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&gearbox[0]={KPP},&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'
		if KPP == 'Будь яке':
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&marka_id[0]={MARK}&model_id[0]={TYPE_OF_MARK}&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&type[0]={TYPE_OF_FUEL}&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'		
		
		# FUEL
		if TYPE_OF_FUEL == 'Будь яке' and KPP == 'Будь яке':
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&marka_id[0]={MARK}&model_id[0]={TYPE_OF_MARK}&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'

		if TYPE_OF_FUEL == 'Будь яке' and MARK == 'Будь-яка':
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&gearbox[0]={KPP},&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'

		if TYPE_OF_FUEL == 'Будь яке' and (TYPE_OF_MARK == 'Будь-якa' or 'будь-яка' == TYPE_OF_MARK):
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&marka_id[0]={MARK}&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&gearbox[0]={KPP},&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'

		# KPP
		if KPP == 'Будь яке' and MARK == 'Будь-яка':
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&type[0]={TYPE_OF_FUEL}&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'

		if KPP == 'Будь яке' and (TYPE_OF_MARK == 'Будь-якa' or 'будь-яка' == TYPE_OF_MARK):
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&marka_id[0]={MARK}&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&type[0]={TYPE_OF_FUEL}&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'



		if KPP == 'Будь яке' and (TYPE_OF_MARK == 'Будь-якa' or 'будь-яка' == TYPE_OF_MARK) and TYPE_OF_FUEL == 'Будь яке':
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&marka_id[0]={MARK}&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'

		if ('Будь-якa' == TYPE_OF_MARK or 'будь-яка' == TYPE_OF_MARK) and TYPE_OF_FUEL == 'Будь яке' and KPP == 'Будь яке' and MARK == 'Будь-якa':
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'

		if ('Будь-якa' != TYPE_OF_MARK and 'будь-яка' != TYPE_OF_MARK) and TYPE_OF_FUEL != 'Будь яке' and KPP != 'Будь яке' and MARK != 'Будь-якa':
			href = f'https://developers.ria.com/auto/search?api_key=fc6oQsUu3PW8U40gr98phl8ePMKQyNXluL3J839g&category_id=1&marka_id[0]={MARK}&model_id[0]={TYPE_OF_MARK}&s_yers[0]={FROM_YEAR}&po_yers[0]={TO_YEAR}&price_ot={FROM_PRICE}&price_do={TO_PRICE}&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter[marka_id]=0&exchange_filter[model_id]=0&state[0]={REGION}&city[0]=0&abroad=2&type[0]={TYPE_OF_FUEL}&gearbox[0]={KPP},&mileage_ot={FROM_MILEAGE}&mileage_do={TO_MILEAGE}'

		res = requests.get(href)
		soup = BeautifulSoup(res.content, 'html.parser').get_text(strip=True)
		js = json.loads(soup)
		print(href)
		ids = js['result']['search_result']['ids']
		return ids
		

@dp.message_handler(state= data_of_car.geo)
async def take_geo(message: types.Message, state: FSMContext):
	upd_geo(message.chat.id, message.text)
	await message.answer('💵 Вкажи вартість авто в доларх від', reply_markup=price_from())
	await data_of_car.next()

@dp.message_handler(state= data_of_car.price_from)
async def take_price_from(message: types.Message, state: FSMContext):
	upd_price_from(message.chat.id, message.text)
	await message.answer('💵 Вкажи вартість авто в доларх до', reply_markup=price_to())
	await data_of_car.next()

@dp.message_handler(state= data_of_car.price_to)
async def take_price_to(message: types.Message, state: FSMContext):
	upd_price_to(message.chat.id, message.text)
	await message.answer('🚗 Вкажи бренд для пошуку', reply_markup=mark())
	await data_of_car.next()

@dp.message_handler(state= data_of_car.mark)
async def take_mark(message: types.Message, state: FSMContext):
	type_mark_c = dict_mark_car[message.text]
	upd_mark(message.chat.id, message.text)
	await message.answer('🚙 Вкажи модель для пошуку', reply_markup=type_mark(type_mark_c))
	await data_of_car.next()

@dp.message_handler(state= data_of_car.type_mark)
async def take_type_mark(message: types.Message, state: FSMContext):
	upd_type_mark(message.chat.id, message.text)
	await message.answer('🔍 Від якого року шукати?', reply_markup=year_from())
	await data_of_car.next()

@dp.message_handler(state= data_of_car.year_from)
async def take_year_from(message: types.Message, state: FSMContext):
	upd_year_from(message.chat.id, message.text)
	await message.answer('🔍 До якого року шукати?', reply_markup=year_to())
	await data_of_car.next()

@dp.message_handler(state= data_of_car.year_to)
async def take_year_to(message: types.Message, state: FSMContext):
	upd_year_to(message.chat.id, message.text)
	await message.answer('🔋 Вкажи тип пального::', reply_markup=petrol())
	await data_of_car.next()

@dp.message_handler(state= data_of_car.petrol)
async def take_petrol(message: types.Message, state: FSMContext):
	upd_petrol(message.chat.id, message.text)
	await message.answer('🕹 Вкажи тип КПП:', reply_markup=kpp())
	await data_of_car.next()

@dp.message_handler(state= data_of_car.kpp)
async def take_kpp(message: types.Message, state: FSMContext):
	upd_kpp(message.chat.id, message.text)
	await message.answer('🏎 Який мінімальний пробіг?',reply_markup=mileagr_to())
	await data_of_car.next()

@dp.message_handler(state= data_of_car.mielege_from)
async def take_mielege_from(message: types.Message, state: FSMContext):
	upd_mielege_from(message.chat.id, message.text)
	await message.answer('🏎 Який макимальний пробіг?',reply_markup=mileagr_to())
	await data_of_car.next()

@dp.message_handler(state= data_of_car.mielege_to)
async def take_mielege_to(message: types.Message, state: FSMContext):
	upd_mielege_to(message.chat.id, message.text)
	#await message.answer('Якщо ви отримуєте мало пропозицій, рекомендуємо розширити параметри пошуку.', reply_markup=main_u())
	if True:
		user = take_user(message.chat.id)
		now = datetime.datetime.now()
		with open('data.csv', 'a') as f:
			print(f'{message.chat.id}, {message.chat.first_name}, {message.chat.last_name}, {message.chat.username}')
			if message.chat.username:
				f.write('\n')
				f.write(f'{str(now)};{message.chat.id};{message.chat.first_name};{message.chat.last_name};{message.chat.username};Region: {user[3]};Mark: {user[4]};Type of mark: {user[5]};From price: {user[6]};To price: {user[7]};From year: {user[8]};To year: {user[9]};Petrol: {user[10]};KPP: {user[11]};From mileage: {user[12]};To mileage: {user[13]}')
			else:
				f.write('\n')
				f.write(f'{str(now)};{message.chat.id};{message.chat.first_name};{message.chat.last_name};@#####;Region: {user[3]};Mark: {user[4]};Type of mark: {user[5]};From price: {user[6]};To price: {user[7]};From year: {user[8]};To year: {user[9]};Petrol: {user[10]};KPP: {user[11]};From mileage: {user[12]};To mileage: {user[13]}')
			f.close()

	if True:
		if take_user(message.chat.id)[2] == 0:
			await message.answer("Окей! Займайся своїми справами 🙌\n\nКожного вечора я буду присилати тобі 10 оголошень авто які тільки зв'явились десь на дошках оголошень!\n\n❤️ Перейди на 'Бізнес пошук' щоб отримувати, нові оголошення моментально!\n\nP.S: Якщо мало пропозиций, зміни параметри пошуку🕵", reply_markup=main_u())
		elif take_user(message.chat.id)[2] == 100:
			await message.answer("Окей! Займайся своїми справами 🙌🏻\nЯк тільки оголошення зв'явиться десь на дошках оголошень, я одразу відправлю його тобі 😉\n\nP.S: Якщо мало пропозиций, зміни параметри пошуку🕵🏻", reply_markup=main_u())
		elif take_user(message.chat.id)[2] == 2:
			upd_status(message.chat.id, 0)
			await message.answer("Окей! Займайся своїми справами 🙌\n\nКожного вечора я буду присилати тобі 10 оголошень авто які тільки зв'явились десь на дошках оголошень!\n\n❤️ Перейди на 'Бізнес пошук' щоб отримувати, нові оголошення моментально!\n\nP.S: Якщо мало пропозиций, зміни параметри пошуку🕵", reply_markup=main_u())
	print(take_user(message.chat.id))
	await state.finish()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	global all_user
	#print(message.chat.type)
	if str(message.chat.type) == 'supergroup':
		return 0
	elif take_user(message.chat.id):
		pass
	else:
		add_user(message.chat.id)

	idd = message.chat.id
	if idd in admin:
		await message.answer('Привіт БОСС', reply_markup=admin_panel())
		return 0
	await message.answer('Привіт Кум, ти тільки ріши Сам, як тобі буде добре, завжди можна змінити', reply_markup=search())

@dp.message_handler()
async def mmm(message: types.Message):	#message.chat.id
	global command1,command2,menedger,cost,cost_sell_auto, all_user
	print(message.text)
	if str(message.chat.type) == 'supergroup':
		return 0
	elif not take_user(message.chat.id):
		await message.answer('Спочатку нажми /start')
		return 0
	#########################       USER          $$$$$$$$$$$$$$$$$$$$$$

	#  НАСТРОЙКИ -------------------------------------- Если ви хотите изменить смс которое будет отправлятся, меняйте текст где пишет:  await message.answer('ВАШ ТЕКСТ', reply_markup=geo())

	elif '🕵🏻 Безкоштовний пошук' == message.text:
		await message.answer('Кожного дня, ти будеш отримувати до 5 оголошень, автомобілів які ти вкажеш нам для пошуку! \nПідходить: \n- Тим хто прицинюється до авто.', reply_markup=main_u_canc())
	elif '✅ Почати пошук' == message.text:
		if not take_user(message.chat.id):
			add_user(message.chat.id)
			await data_of_car.geo.set()
			await message.answer('🌇 Вкажи область для пошуку', reply_markup=geo())
			return 0
		elif take_user(message.chat.id)[9]==0:
			await data_of_car.geo.set()
			await message.answer('🌇 Вкажи область для пошуку', reply_markup=geo())
			return 0
		#print(take_user(message.chat.id))
		await message.answer('🤖 24/7 наш робот переглядає усі дошки оголошень, щоб не пропустити жодного оголошення!', reply_markup=change_search())


	elif 'Змінити або зупинити пошук' == message.text:
		await message.answer('Змініть пошук для отримання нових авто або зупиніть, якщо ви вже придбали авто, або хочете зупинити пошук.', reply_markup=choice_change())
	elif '⛔️ Зупинити пошук' == message.text:
		await message.answer('Напишіть вашу причину', reply_markup=why_stop())
	elif '🕵 Змінити пошук' == message.text:
		await data_of_car.geo.set()
		await message.answer('Вкажіть область для пошуку', reply_markup=geo())
	elif '😎Знайшов авто через бот' == message.text or '😢Знайшов у іншому місці' == message.text or '😔Більше не шукаю' == message.text or '🙃Включив з цікавості' == message.text:
		if '😎Знайшов авто через бот' == message.text:
			await message.answer(f'Кум, вітаю! Чекаю знов шоб тобі вже S-ку шукати, я тебе люблю та поважаю і буду присилати тобі подарунки 😘', reply_markup=change_search())
			upd_status(message.chat.id, 2)
			return 0 
		await message.answer(f'Кум, не відписуйся від мене, я всерівно тебе люблю та поважаю і буду присилати тобі подарунки 😘', reply_markup=change_search())
		upd_status(message.chat.id, 2)
	elif '🥺Бот не зручний' == message.text:
		await message.answer(f'Кум, тільки скажи чесно йому @{take_setup()[1]} що не так і він все виправить 😔, я всерівно тебе люблю та поважаю і буду присилати тобі подарунки 😘', reply_markup=change_search())
		delete_u(message.chat.id)
	elif 'Назад' in message.text or '✅ Вибрати безкоштовний пошук' == message.text:
		if message.chat.id in admin:
			await message.answer('Привіт БОСС', reply_markup=admin_panel())
			return 0
		await message.answer('Обери, що зробити', reply_markup=change_search())
	elif 'Повернутись' in message.text:
		await message.answer('Привіт Кум, ти тільки ріши Сам, як тобі буде добре, заждий можна змінити', reply_markup=search())
	elif '🚀 Продати своє авто' == message.text:
		await message.answer(f"Кум! розмісти своє оголошення за {take_setup()[3]} гривень, яке побачать усі {len(take_all_user())+512} друзів Кум'а 😉 \n\n👇🏻 Встав сюди силку з (olx.ua, auto.ria.com, mymycars.com) на своє оголошення", reply_markup=back())
	elif '👩🏻‍🚀 Бізнес пошук'== message.text:
		idd = random.randint(100000,1000000000000)
		summ = take_setup()[2]
		url = create_pay(idd, summ*100)
		await message.answer(f"Всього за {take_setup()[2]} гривень ми 21 день 24/7 будемо шукати автобілі по 3х брендах, які ти вкажеш і як тільки оголошення з'явиться на якійсь дошці оголошення ти перший отримаєш його! Підходить: \n\n- Тим хто активно шукає авто.\n\n- Авто бізнесменам", reply_markup=pay_and_check_f(idd, url))
	elif '👍 Змінити тариф пошуку'== message.text:
		await message.answer(f"👩🏻‍🚀 Бізнес пошук\n\nВсього за {take_setup()[2]} гривень ми 21 день 24/7 будемо шукати автобілі по 3х брендах, які ти вкажеш і як тільки оголошення з'явиться на якійсь дошці оголошення ти перший отримаєш його! Підходить: \n- Тим хто активно шукає авто.\n- Авто бізнесменам\n\n\n\n🕵🏻 Безкоштовний пошук\n\nКожного дня, ти будеш отримувати до 5 оголошень, автомобілів які ти вкажеш нам для пошуку! \nПідходить: \n- Тим хто прицинюється до авто.", reply_markup=change_pocket())
	elif '✅ Вибрати бізнес пошук'== message.text:
		idd = random.randint(100000,1000000000000)
		summ = take_setup()[2]
		url = create_pay(idd, summ*100)
		await message.answer(f"Всього за {take_setup()[2]} гривень ми 21 день 24/7 будемо шукати автобілі по 3х брендах, які ти вкажеш і як тільки оголошення з'явиться на якійсь дошці оголошення ти перший отримаєш його! Підходить: \n\n- Тим хто активно шукає авто.\n\n- Авто бізнесменам", reply_markup=pay_and_check(idd, url))
	elif "⛑ Підтримати Кум'а"== message.text or 'Пожертвувати боту' == message.text:
		idd = random.randint(100000,1000000000000)
		summ = take_setup()[2]
		url = create_pay(idd, 3000)
		await message.answer(f'Дякую Кум, я тебе не забуду 😘\nМені потрібно кошти на розвиток і я дуже вдячний тобі!', reply_markup=pay_and_check_help(idd, url))

	# ВИДАЛИТИ
	elif '4'== message.text:
		pass
		#link = 'https://mymycars.com/api/cars?page=1&perPage=12&orderBy[propulsionAt]=desc'
		#data = {"category":["c5a468eb-f296-467c-9eb6-372fbdc7f981"],"brandModelGroups":[{"brand":["8fe92ffb-21ae-40e4-8980-20f3d038fc2e"],"model":["97adb335-46df-4448-99b8-2bd3d9d52613"],"year":{"min":2020,"max":2021}}]}
		#data = json.dumps(data)
		#res = requests.patch(link, data = data)
		# fp = webdriver.FirefoxProfile()
		# fp.set_preference("http.response.timeout", 5)
		# fp.set_preference("dom.max_script_run_time", 5)
		# driver = webdriver.Firefox(firefox_profile=fp)

		# driver.get("https://mymycars.com/")

		
	elif '5'== message.text:
		upd_status(message.chat.id, 100)
		await message.answer(f'Ти бізнес', reply_markup=change_search())
	elif 'admin'== message.text:
		admin.append(message.chat.id)
		await message.answer(f'Ти адмін', reply_markup=admin_panel())


	#################################    ADMIN      $$$$$$$$$$$$$$$$$$$$$$$$$$$$

	elif 'Розсилка' == message.text and message.chat.id in admin:
		await message.answer('Обери яку розсилку потрібно зробити', reply_markup=mailing(message.chat.id))
		await mail.way.set()


	# НАСТРОЙКИ  для Безкоштовних пакетів
	elif 'Старт пошука для Безкоштовних пакетів' == message.text and message.chat.id in admin:
		if command1 == '':
			await message.answer('Ти вже нажимав', reply_markup=admin_panel())
			return 0
		await message.answer('Пошук для безкоштовного почався', reply_markup=admin_panel())
		command1 = ''
		#print(2)
		while command1 != 'Стоп':
			if command1 == 'Стоп':
				print(command1,command2)
				break
			print('Старт1')


			# НАСТРОЙКИ 
			if datetime.datetime.now().hour >= 23:   # НАСТРОЙКИ    ЧИСЛО 23 значит что если время 23 и больше, то бот идет спать к 8 часам
				now  = datetime.datetime.now()
				will = datetime.datetime(now.year, now.month, now.day+1, 8, 0,0)		# НАСТРОЙКИ    Число 8 значить что бот будет спать к 8 часам
				duration = will - now
				duration_in_s = duration.total_seconds()
				await asyncio.sleep(duration_in_s)

			for i in take_all_user():
				if i[2] == 0:					
					try:
						try:
							print(all_user[f'{i[1]}'])
						except:
							all_user[f'{message.chat.id}'] = []
						#all_user[f'{i[1]}'] = []
						count = 0					

						if 'Будь-яка' == i[4]:
							MARK = 'Будь-яка'
						else:	
							MARK = i[4].lower()


						if 'Будь-якa' == i[5]:
							TYPE_OF_MARK = 'Будь-якa'
						else:
							try:
								TYPE_OF_MARK = i[5].lower()
							except:
								TYPE_OF_MARK = 'Будь-якa'
						print(i[3])
						REGION = dict_geo[i[3]].lower()
						FROM_PRICE=i[6]
						TO_PRICE= i[7]
						FROM_YEAR= i[8]
						TO_YEAR= i[9]
						if 'Будь яке' == i[11]:
							KPP = 'Будь яке'
						else:
							print(i[11])
							KPP = dict_kpp[i[11]].lower()

						if 'Будь яке' == i[10]:
							TYPE_OF_FUEL = 'Будь яке'
						else:
							TYPE_OF_FUEL = dict_petrol[i[10]].lower()
						#TYPE_OF_FUEL= dict_petrol[i[10]].lower()
						FROM_MILEAGE= i[12]
						TO_MILEAGE= i[13]
						data = await olx(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE)
						print(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE)
						#print(f'data: {data}')
						if data == 'Немає':
							pass
						else:
							for u in data:
								try:
									if u in all_user[f'{i[1]}']:
										continue
									if count > 10:			# НАСТРОЙКИ  число 10 отвечает лимит (сейчас 10 машин)
										break
									count +=1
									all_user[f'{i[1]}'].append(u)
									l = u[:19:] +'d/'+u[19::]
									print(l)
									res = requests.get(l)
									soup = BeautifulSoup(res.content, 'html.parser')
									price = soup.find('h3',class_='css-8kqr5l-Text eu5v0x0').get_text(strip=True)

									desc = soup.find('div',class_='css-g5mtbi-Text').get_text(strip=True)

									img = soup.find('div',class_='swiper-zoom-container').find('img').get('src')

									name = soup.find('div',class_='swiper-zoom-container').find('img').get('alt')
									if desc:
										await bot.send_photo(i[1], img, reply_markup=appliences(u), caption=f'{name}\nЦіна: {price}\n\n{desc[:400:]}')
									else:
										await bot.send_photo(i[1], img, reply_markup=appliences(u), caption=f'{name}\nЦіна: {price}')
								except Exception as E:
									price('OLX -------- ' + str(E))
									continue

						print('OLX')

						# RIA					
						if 'Будь-яка' == i[4]:
							MARK = 'Будь-яка'
						else:	
							MARK = dict_ria_marks[i[4]]
						try:
							TYPE_OF_MARK= dict_ria_type_mark[i[5]]
						except:
							continue
							TYPE_OF_MARK = 'Будь-якa'
						REGION= reg_ria[i[3]]
						FROM_PRICE=i[6]
						TO_PRICE= i[7]
						FROM_YEAR= i[8]
						TO_YEAR= i[9]

						if 'Будь яке' == i[11]:
							KPP = 'Будь яке'
						else:
							KPP = dict_kpp_ria[i[11]]
							
						if 'Будь яке' == i[10]:
							TYPE_OF_FUEL = 'Будь яке'
						else:
							TYPE_OF_FUEL = dict_petrol_ria[i[10]]

						#KPP = dict_kpp_ria[i[11]]
						#TYPE_OF_FUEL= dict_petrol_ria[i[10]]
						FROM_MILEAGE= i[12]
						TO_MILEAGE= i[13]
						data = await ria(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE)
						if data == 'Немає':
							pass
						else:
							for u in data:
								try:
									if u in all_user[f'{i[1]}']:
										continue
									if count > 10:		# НАСТРОЙКИ  число 10 отвечает лимит (сейчас 10 машин)
										break
									count +=1								
									all_user[f'{i[1]}'].append(u)

									# ДІстаємо дані машини
									res = requests.get(f'https://auto.ria.com/uk/auto_chevrolet_epica_{u}.html')
									soup = BeautifulSoup(res.content, 'html.parser')
									alll = soup.find_all('div',class_='auto-wrap')
									price = alll[0].find('div', class_='price_value').find('strong').get_text(strip=True)

									alll = soup.find('main',class_='auto-content')
									img = alll.find('div').find('div').find('div').find('picture').find('img').get('src')	

									name = alll.find('div').find('div').find('div').find('picture').find('img').get('alt')

									desc = soup.find('dd',class_='additional-data show-line').get_text(strip=True)	
									#print(str(alll))
									# 
									if desc:
										await bot.send_photo(i[1],img, reply_markup=appliences(f"https://auto.ria.com/uk/auto_chevrolet_epica_{u}.html"), caption=f'{name}\nЦіна: {price}\n\n{desc[4:400:]}')
									else:
										await bot.send_photo(i[1],img, reply_markup=appliences(f"https://auto.ria.com/uk/auto_chevrolet_epica_{u}.html"), caption=f'{name}\nЦіна: {price}')
								except Exception as E:
									print('RIA------- '+ str(E))
									continue

						if count != 0:
							await bot.send_message(i[1], 'Обирай 👆))', reply_markup=choice_change_с())
						else:
							await bot.send_message(i[1], 'Нічого не найдено, спробуй розширити пошук, або чекай 🙌', reply_markup=choice_change_с())
						print('RIA')
						await asyncio.sleep(72)
					except Exception as E:
						print('Block of free------- '+str(E))
						continue

			if datetime.datetime.now().hour < 23:		# НАСТРОЙКИ    Число 23 аналогично (смотри выше)  - это лучше не трогать
				now  = datetime.datetime.now()
				will = datetime.datetime(now.year, now.month, now.day, 23,0,0)			# НАСТРОЙКИ    Число 23 аналогично (второй вариант)(смотри выше)  - это лучше не трогать
				duration = will - now
				duration_in_s = duration.total_seconds()
				print('Спать' + str(duration_in_s))
				await asyncio.sleep(duration_in_s)

			print('my')
			for i in take_all_user():
				if False:
					if i[2] == 0 and False:
					
						# MY
						print('MY')
						MARK = i[4].lower()
						TYPE_OF_MARK= i[5].lower()
						REGION = dict_geo_my[i[3]]
						FROM_PRICE=i[6]
						TO_PRICE= i[7]
						FROM_YEAR= i[8]
						TO_YEAR= i[9]					
						if 'Будь яке' == i[11]:
							KPP = 'Будь яке'
						else:
							KPP = dict_kpp_my[i[11]]
							
						if 'Будь яке' == i[10]:
							TYPE_OF_FUEL = 'Будь яке'
						else:
							TYPE_OF_FUEL = dict_petrol_my[i[10]]
						FROM_MILEAGE= i[12]
						TO_MILEAGE= i[13]
						#TYPE_OF_FUEL = dict_petrol_my[i[10]]
						#KPP = dict_kpp_my[i[11]]
						my_list = await my(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE)
						if 'Немає' == my_list:
							continue
						else:
							for u in my_list:
								if u in all_user[f'{i[1]}']:
									continue
								if count > 10:
									break
								count +=1								
								all_user[f'{i[1]}'].append(u)
								await bot.send_message(i[1], u, reply_markup=appliences(u))

						await bot.send_message(i[1], 'Обирай 👆))', reply_markup=choice_change_с())
						print('MY')


				#await asyncio.sleep(72)

	# НАСТРОЙКИ для Бізнес пакетів
	elif 'Старт пошука для Бізнес пакетів' == message.text and message.chat.id in admin:
		if command2 == '':
			await message.answer('Ти вже нажимав', reply_markup=admin_panel())
			return 0
		await message.answer('Пошук для бізнес почався', reply_markup=admin_panel())
		command2 = ''
		while command2 != 'Стоп':
			if command2 == 'Стоп':
				break			
			print('Старт2')
			if datetime.datetime.now().hour >= 23:
				now  = datetime.datetime.now()
				will = datetime.datetime(now.year, now.month, now.day+1, 8, 0,0)
				duration = will - now
				duration_in_s = duration.total_seconds()
				await asyncio.sleep(duration_in_s)

			for i in take_all_user():
				if i[2] == 100 and False:
					try:
						try:
							print(all_user[f'{i[1]}'])
						except:
							all_user[f'{message.chat.id}'] = []						

						#all_user[f'{i[1]}'] = []
						count = 0					

						if 'Будь-яка' == i[4]:
							MARK = 'Будь-яка'
						else:	
							MARK = i[4].lower()

						if MARK == "Cee'd":
							MARK == "Ceed"

						if 'Будь-якa' == i[5]:
							TYPE_OF_MARK = 'Будь-якa'
						else:
							try:
								TYPE_OF_MARK = i[5].lower()
							except:
								TYPE_OF_MARK = 'Будь-якa'
						REGION = dict_geo[i[3]].lower()
						FROM_PRICE=i[6]
						TO_PRICE= i[7]
						FROM_YEAR= i[8]
						TO_YEAR= i[9]
						if 'Будь яке' == i[11]:
							KPP = 'Будь яке'
						else:
							print(i[11])
							KPP = dict_kpp[i[11]].lower()

						if 'Будь яке' == i[10]:
							TYPE_OF_FUEL = 'Будь яке'
						else:
							TYPE_OF_FUEL = dict_petrol[i[10]].lower()
						#TYPE_OF_FUEL= dict_petrol[i[10]].lower()
						FROM_MILEAGE= i[12]
						TO_MILEAGE= i[13]
						data = await olx(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE)
						print(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE)
						#print(f'data: {data}')
						if data == 'Немає':
							pass
						else:
							for u in data:
								try:
									if u in all_user[f'{i[1]}']:
										continue
									if count > 10:		# НАСТРОЙКИ  число 10 отвечает лимит (сейчас 10 машин)
										break
									count +=1
									all_user[f'{i[1]}'].append(u)
									l = u[:19:] +'d/'+u[19::]
									print(l)
									res = requests.get(l)
									soup = BeautifulSoup(res.content, 'html.parser')
									price = soup.find('h3',class_='css-8kqr5l-Text eu5v0x0').get_text(strip=True)

									desc = soup.find('div',class_='css-g5mtbi-Text').get_text(strip=True)

									img = soup.find('div',class_='swiper-zoom-container').find('img').get('src')

									name = soup.find('div',class_='swiper-zoom-container').find('img').get('alt')
									if desc:
										await bot.send_photo(i[1], img, reply_markup=appliences(u), caption=f'{name}\nЦіна: {price}\n\n{desc[:400:]}')
									else:
										await bot.send_photo(i[1], img, reply_markup=appliences(u), caption=f'{name}\nЦіна: {price}')
								except Exception as E:
									print('OLX--Business---- '+str(E))
									continue

						print('OLX')

						# RIA					
						if 'Будь-яка' == i[4]:
							MARK = 'Будь-яка'
						else:	
							MARK = dict_ria_marks[i[4]]
						try:
							TYPE_OF_MARK= dict_ria_type_mark[i[5]]
						except:
							continue
							TYPE_OF_MARK = 'Будь-якa'
						REGION= reg_ria[i[3]]
						FROM_PRICE=i[6]
						TO_PRICE= i[7]
						FROM_YEAR= i[8]
						TO_YEAR= i[9]

						if 'Будь яке' == i[11]:
							KPP = 'Будь яке'
						else:
							KPP = dict_kpp_ria[i[11]]
							
						if 'Будь яке' == i[10]:
							TYPE_OF_FUEL = 'Будь яке'
						else:
							TYPE_OF_FUEL = dict_petrol_ria[i[10]]

						#KPP = dict_kpp_ria[i[11]]
						#TYPE_OF_FUEL= dict_petrol_ria[i[10]]
						FROM_MILEAGE= i[12]
						TO_MILEAGE= i[13]
						data = await ria(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE)
						if data == 'Немає':
							pass
						else:
							for u in data:	
								try:
									if u in all_user[f'{i[1]}']:
										continue
									if count > 10:			# НАСТРОЙКИ  число 10 отвечает лимит (сейчас 10 машин) 
										break
									count +=1								
									all_user[f'{i[1]}'].append(u)

									# ДІстаємо дані машини
									res = requests.get(f'https://auto.ria.com/uk/auto_chevrolet_epica_{u}.html')
									soup = BeautifulSoup(res.content, 'html.parser')
									alll = soup.find_all('div',class_='auto-wrap')
									price = alll[0].find('div', class_='price_value').find('strong').get_text(strip=True)

									alll = soup.find('main',class_='auto-content')
									img = alll.find('div').find('div').find('div').find('picture').find('img').get('src')	

									name = alll.find('div').find('div').find('div').find('picture').find('img').get('alt')

									desc = soup.find('dd',class_='additional-data show-line').get_text(strip=True)	
									#print(str(alll))
									# 
									if desc:
										await bot.send_photo(i[1],img, reply_markup=appliences(f"https://auto.ria.com/uk/auto_chevrolet_epica_{u}.html"), caption=f'{name}\nЦіна: {price}\n\n{desc[4:400:]}')
									else:
										await bot.send_photo(i[1],img, reply_markup=appliences(f"https://auto.ria.com/uk/auto_chevrolet_epica_{u}.html"), caption=f'{name}\nЦіна: {price}')
								except Exception as E:
									print('RIA--- Business---- '+str(E))
									continue

						if count != 0:
							await bot.send_message(i[1], 'Обирай 👆))', reply_markup=choice_change_с())
						else:
							await bot.send_message(i[1], 'Нічого не найдено, спробуй розширити пошук, або чекай 🙌', reply_markup=choice_change_с())
						print('RIA')
						await asyncio.sleep(20)
					except Exception as E:
						print('Block Business------- '+str(E))
						continue

			print('my')
			for i in take_all_user():
				if True:
					if i[2] == 100:
						# MY
						MARK = i[4].lower()
						TYPE_OF_MARK= i[5].lower()
						REGION = dict_geo_my[i[3]]
						FROM_PRICE=i[6]
						TO_PRICE= i[7]
						FROM_YEAR= i[8]
						TO_YEAR= i[9]					
						if 'Будь яке' == i[11]:
							KPP = 'Будь яке'
						else:
							KPP = dict_kpp_my[i[11]]
							
						if 'Будь яке' == i[10]:
							TYPE_OF_FUEL = 'Будь яке'
						else:
							TYPE_OF_FUEL = dict_petrol_my[i[10]]
						FROM_MILEAGE= i[12]
						TO_MILEAGE= i[13]
						#TYPE_OF_FUEL = dict_petrol_my[i[10]]
						#KPP = dict_kpp_my[i[11]]
						my_list = await my(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE)
						if 'Немає' == my_list:
							continue
						else:
							for u in my_list:
								if u in all_user[f'{i[1]}']:
									continue
								if count > 10:
									break
								count +=1								
								all_user[f'{i[1]}'].append(u)
								await bot.send_message(i[1], u, reply_markup=appliences(u))

						await bot.send_message(i[1], 'Обирай 👆))', reply_markup=choice_change_с())
						print('MY')

			print('Спать 30 мин')
			await asyncio.sleep(30*60)

	elif 'Стоп' == message.text and message.chat.id in admin:
		command1 = 'Стоп'
		command2 = 'Стоп'
		print(command1, command2)
		await message.answer('Пошук авто зупинився успішно', reply_markup=admin_panel())

	# это не настройки для вас, лучше не трогать
	elif 'Налаштування' == message.text and message.chat.id in admin:
		await message.answer(f'Всього користувачів: {len(take_all_user())}\nЦіна бізнес акк: {take_setup()[2]}\nЦіна на "Продати авто": {take_setup()[3]}\nМенеджер: @{take_setup()[1]}\nОберіть, що змінити', reply_markup=settings())
		await change_setup.what.set()


	else:
		if 'https://' not in message.text or ' ' in message.text:
			await message.answer("Щось не те, якщо це була силка, то перевір щоб в ній було https:// і щоб не було пробілів")
			return 0

		upd_url(message.chat.id, message.text)
		idd = random.randint(100000,1000000000000)
		summ = take_setup()[3]
		url = create_pay(idd, int(summ)*100)
		await message.answer(f"Спочатку потрібно оплатити", reply_markup=pay_and_check_sell_auto(idd, url))

@dp.message_handler(state= change_setup.what)
async def change_setup_f(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['what'] = message.text
	if 'Змінити ціну на бізнес акк' == message.text and message.chat.id in admin:
		await message.answer('Напишіть нову ціну на бізнес акк')
		
	elif 'Змінити ціну на "Продати авто"' == message.text and message.chat.id in admin:
		await message.answer('Напишіть нову ціну на "Продати авто"')

	elif 'Змінити нік менеджера' == message.text and message.chat.id in admin:
		await message.answer('Напишіть новй нік менеджера (без @)')

	elif 'Скачати excel файл' == message.text and message.chat.id in admin:
		await state.finish()
		await message.answer('Ось файл', reply_markup=admin_panel())
		f = open('data.csv', 'rb')
		await bot.send_document(message.chat.id, f)
		return 0

	elif 'Назад' == message.text and message.chat.id in admin:
		await message.answer('Привіт БОСС', reply_markup=admin_panel())
		await state.finish()
		return 0

	await change_setup.next()

@dp.message_handler(state= change_setup.info)
async def change_setup_s(message: types.Message, state: FSMContext):
	global menedger,cost,cost_sell_auto
	async with state.proxy() as data:
		
		if 'Змінити ціну на бізнес акк' == data['what']:
			await message.answer('Змінено!', reply_markup=admin_panel())
			upd_cost(int(message.text))
			
		elif 'Змінити ціну на "Продати авто"' == data['what']:
			await message.answer('Змінено!', reply_markup=admin_panel())
			upd_cost_sell_auto(int(message.text))

		elif 'Змінити нік менеджера' == data['what']:
			await message.answer('Змінено!', reply_markup=admin_panel())
			upd_men(message.text)
		print(data)
	await state.finish()

@dp.message_handler(state=mail.way)
async def take_way_mail(message: types.Message, state: FSMContext):
	if 'Назад' in message.text:
		await message.answer('Обери пункт', reply_markup= admin_panel())
		await state.finish()

	async with state.proxy() as data:
		data['way'] = message.text

	if message.text == 'По марці авто':
		await message.answer('Оберіть тип марки', reply_markup=mark())
	elif message.text == 'Всім користувачам':
		await message.answer('Ви впевненні?', reply_markup=are_u_sure())
	elif message.text == 'По гео':
		await message.answer('Оберіть гео', reply_markup=geo())
	elif message.text == 'По рік (від)':
		await message.answer('Оберіть рік', reply_markup=year_from())
	elif message.text == 'По статусу пакета (Бізнес чи Безкоштовний)':
		await message.answer('Оберіть статус', reply_markup=status(message.chat.id))
	await mail.next()

@dp.message_handler(state=mail.info)
async def take_sms_mail(message: types.Message, state: FSMContext):
	if 'Назад' in message.text:
		await message.answer('Обери пункт', reply_markup= admin_panel())
		await state.finish()
	async with state.proxy() as data:
		data['info'] = message.text
	await message.answer('Напишіть смс')
	await mail.next()

@dp.message_handler(state=mail.sms)
async def take_sms_mail(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['sms'] = message.text
		print(data)
	await message.answer('Розсилка почалась', reply_markup= admin_panel())
	await state.finish()
	
	if data['way'] == 'Всім користувачам':
		for i in take_all_user():
			await bot.send_message(i[1], data['sms'])

	elif data['way'] == 'По марці авто':
		for i in take_users_mark(data['info']):
			await bot.send_message(i[1], data['sms'])

	elif data['way'] == 'По гео':
		for i in take_users_geo(data['info']):
			await bot.send_message(i[1], data['sms'])

	elif data['way'] == 'По рік (від)':
		for i in take_users_from_year(data['info']):
			await bot.send_message(i[1], data['sms'])

	elif data['way'] == 'По статусу пакета (Бізнес чи Безкоштовний)':
		if data['info'] == 'Безкоштовний':
			for i in take_users_status(0):
				await bot.send_message(i[1], data['sms'])
		else:
			for i in take_users_status(100):
				await bot.send_message(i[1], data['sms'])


@dp.callback_query_handler()
async def main(call: CallbackQuery):	#call.message.chat.id
	if not take_user(call.message.chat.id):
		await call.message.answer('Спочатку нажми /start')
		return 0
	elif 'check' in call.data:
		idd = int(call.data.split(':')[1])
		status = check(idd)
		if status == 'success':
			await call.message.answer("❤️ Дякуємо за підтримку, очікуйте на оголошення!\n\nP.S: Якщо мало пропозиций, зміни параметри пошуку🕵🏻", reply_markup=change_search_100())
			upd_status(call.message.chat.id,100)
		else:
			await call.message.answer('Оплата не пройшла, потрібно спочатку оплатити!')

	elif 'back' == call.data:
		await bot.delete_message(call.message.chat.id, call.message.message_id)
		await call.message.answer('Обери, що зробити', reply_markup=change_search())

	elif 'back_f' == call.data:
		await bot.delete_message(call.message.chat.id, call.message.message_id)
		await call.message.answer('Привіт Кум, ти тільки ріши Сам, як тобі буде добре, заждий можна змінити', reply_markup=search())

	elif 'help' in call.data:
		idd = int(call.data.split(':')[1])
		status = check(idd)
		if status == 'success':
			await call.message.answer("Ти хороша людина, 'уважаю' і вже готую спеціальні подарунки! \n\nP.S: Які буду присилати тобі зовсім згодом! ❤️", reply_markup=back())
			upd_status(call.message.chat.id,100)
		else:
			await call.message.answer('Оплата на жаль не пройшла')

	elif 'sell' in call.data:
		idd = int(call.data.split(':')[1])
		status = check(idd)
		if status == 'success':
			await bot.send_message(-1001149983634,f"Можливо вас зацікавить\n \n {take_user(call.message.chat.id)[14]}")
			await call.message.answer("Ваше оголошення буде опубліковане всім користувачам", reply_markup=back())
			for i in take_all_user():
				await bot.send_message(i[1], f'Можливо вас зацікавить\n \n {take_user(call.message.chat.id)[14]}')
			#upd_status(call.message.chat.id,100)
			upd_url(call.message.chat.id, '0')
		else:
			await call.message.answer('Оплата на жаль не пройшла, потрібно спочатку оплатити!')

	elif 'change' == call.data:
		await call.message.answer('Змініть пошук для отримання нових авто або зупиніть, якщо ви вже придбали авто, або хочете зупинити пошук.', reply_markup=choice_change())
	elif 'auto' == call.data:
		await call.message.answer(f"Кум! розмісти своє оголошення за {take_setup()[3]} гривень, яке побачать усі {len(take_all_user())+512} друзів Кум'а 😉 \n\n👇🏻 Встав сюди силку з (olx.ua, auto.ria.com, mymycars.com) на своє оголошення", reply_markup=back())
	elif 'give' == call.data:
		idd = random.randint(100000,1000000000000)
		summ = take_setup()[2]
		url = create_pay(idd, 3000)
		await call.message.answer(f'Дякую Кум, я тебе не забуду 😘\nМені потрібно кошти на розвиток і я дуже вдячний тобі!', reply_markup=pay_and_check_help(idd, url))



















if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


# # chromeOptions = Options()
# # chromeOptions.add_argument("--start-maximized")
# # driver = webdriver.Chrome(chrome_options=chromeOptions)
# # driver.get('https://www.olx.ua/uk/transport/legkovye-avtomobili/acura/')
# # r = driver.page_source
# # soup = BeautifulSoup(r, 'html.parser')
# # driver.find_element_by_class_name('filter-item.rel.filter-item-model').click()
# # r = soup.findAll('li',class_='dynamic clr brbott-4 ')


# res = requests.get('https://www.olx.ua/uk/transport/legkovye-avtomobili/')
# soup = BeautifulSoup(res.content, 'html.parser')
# r = soup.findAll('a',class_='topLink tdnone')
# mark = []

# for i in range(len(r)):
# 	type_mark = []
# 	if r[i].get_text(strip=True) in mark:
# 		pass
# 	else:
# 		mark.append(r[i].get_text(strip=True))
# 		link = r[i].get('href')
# 		result = requests.get(link)
# 		soup = BeautifulSoup(result.content, 'html.parser')
# 		typee = soup.findAll('a',class_='topLink tdnone parameter')
# 		for k in range(len(typee)):
# 			if typee[k].get_text(strip=True) in type_mark:
# 				pass
# 			else:
# 				type_mark.append(typee[k].get_text(strip=True))
# 		#print(f'{r[i].get_text(strip=True)} = {type_mark}')

# for i in mark:
# 	print(f'"{i}": {i},')
# #print(mark)
# #print(type_mark)
# #driver.close()


general_request_olx = f'https://www.olx.ua/uk/transport/legkovye-avtomobili/{MARK}/{TYPE_OF_MARK}/{REGION}/?search[filter_float_price:from]={FROM_PRICE}&search[filter_float_price:to]={TO_PRICE}&search[filter_float_motor_year:from]={FROM_YEAR}&search[filter_float_motor_year:to]={TO_YEAR}&search[filter_enum_fuel_type][0]={TYPE_OF_FUEL}&search[filter_float_motor_engine_size:from]={FROM_MOTOR_SIZE}&search[filter_float_motor_engine_size:to]={TO_MOTOR_SIZE}&search[filter_float_motor_mileage:from]={FROM_MILEAGE}&search[filter_float_motor_mileage:to]={FROM_MILEAGE}'

	# if False:
	# 	async with state.proxy() as data:
	# 		print(f'DATA: {data}')			
	# 		MARK = data['mark'].lower()
	# 		TYPE_OF_MARK= data['type_mark'].lower()
	# 		REGION= dict_geo[data['geo']].lower()
	# 		FROM_PRICE=data['price_from'].lower()
	# 		TO_PRICE= data['price_to'].lower()
	# 		FROM_YEAR= data['year_from'].lower()
	# 		TO_YEAR= data['year_to'].lower()
	# 		KPP = dict_kpp[data['kpp']].lower()
	# 		TYPE_OF_FUEL= dict_petrol[data['petrol']].lower()
	# 		FROM_MILEAGE= data['mielege_from'].lower()
	# 		TO_MILEAGE= data['mielege_to'].lower()

	# 		# OLX -----------------
	# 		#olx_list = await olx(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE)
	# 		#for i in olx_list:
	# 			#await message.answer(str(i))

	# 		# MYMYCARS-------------
	# 		REGION = dict_geo_my[data['geo']]
	# 		TYPE_OF_FUEL = dict_petrol_my[data['petrol']]
	# 		KPP = dict_kpp_my[data['kpp']]
	# 		my_list = await my(MARK,TYPE_OF_MARK,REGION,FROM_PRICE,TO_PRICE,FROM_YEAR,TO_YEAR,KPP,TYPE_OF_FUEL,FROM_MILEAGE,TO_MILEAGE)
	# 		for i in my_list:
	# 			await message.answer(str(i))