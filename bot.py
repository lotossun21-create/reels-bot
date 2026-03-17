import telebot
from yt_dlp import YoutubeDL
import os
import sys

# Читаем переменные окружения (Render их передаст автоматически)
TOKEN = os.environ.get('TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

# Проверка: если переменные не заданы — сразу выходим с понятной ошибкой в логах
if not TOKEN:
    print("ОШИБКА: Переменная окружения TOKEN не задана!")
    sys.exit(1)

if ':' not in TOKEN:
    print("ОШИБКА: TOKEN выглядит неправильно (должно быть что-то вроде 123456:ABCdef...)")
    sys.exit(1)

if not CHANNEL_ID:
    print("ОШИБКА: Переменная окружения CHANNEL_ID не задана!")
    sys.exit(1)

print(f"Запускаем бота с CHANNEL_ID = {CHANNEL_ID}")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: message.text and 'instagram.com' in message.text)
def handle_instagram_link(message):
    url = message.text.strip()

    # На всякий случай добавляем https, если пользователь просто вставил instagram.com/...
    if not url.startswith('http'):
        url = 'https://' + url

    try:
        bot.reply_to(message, "Скачиваю Reels... подожди 10–40 секунд ⏳")

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': 'reel_%(id)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Отправляем видео в канал
        with open(filename, 'rb') as video_file:
            bot.send_video(
                chat_id=CHANNEL_ID,
                video=video_file,
                caption=f"Reels из Instagram\n\n🔗 {url}\n\nот @{message.from_user.username or 'аноним'}",
                supports_streaming=True
            )

        bot.reply_to(message, "✅ Видео отправлено в канал!")

        # Удаляем временный файл
        os.remove(filename)

    except Exception as e:
        error_text = f"Ошибка: {str(e)}"
        print(error_text)  # в логи Render
        bot.reply_to(message, error_text[:200] + "..." if len(error_text) > 200 else error_text)

print("Бот успешно стартовал и ждёт сообщений...")
bot.infinity_polling(allowed_updates=["message"])
