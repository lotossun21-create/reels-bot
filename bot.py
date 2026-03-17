import telebot
from yt_dlp import YoutubeDL
import os

TOKEN = 'ТОТ_ТОКЕН_ОТ_BOTFATHER'          # ← замени
CHANNEL_ID = '@твой_канал_или_группа'     # ← замени (например @reelsfrominsta или -1001234567890)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: 'instagram.com' in (m.text or ''))
def download_reel(message):
    url = message.text.strip()
    if not url.startswith('http'):
        url = 'https://' + url

    bot.reply_to(message, "Скачиваю Reels... ⏳")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': 'reel_%(id)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(CHANNEL_ID, video, caption=f"Reels из Instagram\n🔗 {url}")

        bot.reply_to(message, "✅ Готово!")
        os.remove(filename)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)[:150]}")

print("Бот запущен...")
bot.infinity_polling()