import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message             # ловим все обновления этого типа 
from aiogram.filters.command import Command # обрабатываем команды /start, /help и другие
from transliterate import translit

# 2. Инициализация объектов
TOKEN = os.getenv("TOKEN")
bot = Bot(token="7706552456:AAHnWE2gkq5BsbVUhDx7IWtDqb_oDvf5vdQ")                       # Создаем объект бота
dp = Dispatcher()     # Создаем объект диспетчера. Все хэндлеры(обработчики) должны быть подключены к диспетчеру

logging.info('Hello')

#Логирование в файл.

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # Создаём папку
logfile_path = os.path.join(log_dir, "mylog.log")
logging.basicConfig(
    level=logging.DEBUG,
    filename = "mylog.log", 
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", 
    datefmt='%H:%M:%S',
    )    

# Домашнее Задание
# - Включить запись log в файл
# - Бот принимает кириллицу отдаёт латиницу в соответствии с Приказом МИД по транслитерации
# - Бот работает из-под docker контейнера
transliteration_dict = {
    "а": 'А', 'б': 'B', 'в': 'V', 'г': 'G', 'д': 'D', 'е': 'E', 'ё': 'E',
    'ж': 'ZH', 'з': 'Z', 'и': 'I', 'й': 'I', 'к': 'K', 'л': 'L', 'м': 'M',
    'н': 'N', 'о': 'O', 'п': 'P', 'р': 'R', 'с': 'S', 'т': 'T', 'у': 'U',
    'ф': 'F', 'х': 'KH', 'ц': 'TS', 'ч': 'CH', 'ш': 'SH', 'щ': 'SHCH', 'ь': '',
    'ы': 'Y', 'ъ': 'ID', 'э': 'E', 'ю': 'YU', 'я': 'YA',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
    'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M',
    'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ь': '',
    'Ы': 'Y', 'Ъ': 'IE', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA'
}

def transliterate(text):
    return ''.join(transliteration_dict.get(char, char) for char in text)

# 3. Обработка/Хэндлер на команду /start
@dp.message(Command(commands=['start']))
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Привет, {user_name}!Напиши своё ФИО на русском, а я переведу его в латиницу, в соответствии с Приказом МИД от 12.02.2020 №2113!'
    logging.info(f'{user_name} {user_id} запустил бота')
    await bot.send_message(chat_id=user_id, text=text)
    
# 4. Обработка/Хэндлер на любые сообщения
@dp.message()
async def send_transliteration(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text
    transliterated_text = transliterate(text) 
    logging.info(f'{user_name} {user_id}: {text} -> {transliterated_text}')
    await message.answer(text=transliterated_text)

# 5. Запуск процесса пуллинга
if __name__ == '__main__':
    dp.run_polling(bot)

