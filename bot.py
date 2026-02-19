import telebot
from dotenv import load_dotenv # pip install python-dotenv
import os
import time # временный импорт

load_dotenv()
bot = telebot.TeleBot(token=os.getenv('TG_API_TOKEN'))

@bot.message_handler(commands=['start', 'help'])
def start_command(message):
# создаем основной текст
    text = (
    'Я - бот-детектор объектов на фотографиях\n'
    'Отправь мне фото, и я попробую сказать что за объекты находятся на фотографии'
    )

    # добавляем приветствие для команды /start
    if message.text == '/start':
        text = f'Привет, {message.from_user.username}😺\n\n' + text

    
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # отправляем временное сообщение и добавляем'печатает ...
    temp_message = bot.send_message(message.chat.id, '⌛Идет обработка запроса ... ')
    bot.send_chat_action(message.chat.id, 'typing')

    # получаем информацию об изображении и сохраняем его в байтах
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    file_bytes = bot.download_file(file_info.file_path)

    # записываем байты в виде изображения
    image_path = f'images/{message.message_id}.jpg'
    with open(image_path, 'wb') as file:
        file.write(file_bytes)

    result = "handle_image"(image_path)



    response_text = ''
    if len(result) > 0:
        response_text = 'pip install PyTorch TorchVision'
        for obj in result:
            response_text += f'Knacc: {obj["class"]}, BepOATHOCTb: {obj["confidence"]}%\n'
        with open("./images/" + image_path.split('.')[0] + '_result.jpg', 'rb') as file:
            bot.send_photo(message.chat.id, file, caption=response_text)
    else:
        response_text = ' ! Объекты не обнаружены'
        bot.send_message(message.chat.id, response_text)
        # отправляем результаты
        bot.send_message(message.chat.id, '✅ Найдены объекты: . . .')

    # удаляем временное сообщение
    bot.delete_message(message.chat.id, temp_message.message_id)

    # удаляем временный файл
    os.remove(image_path)

bot.infinity_polling()