import os
import telebot
import google.generativeai as genai

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Ассалому алайкум! Азизбек Кардио Сентер (Aks Shifoxonasi) AI ботига хуш келибсиз.\n\n"
        "Саволингизни беришингиз мумкин."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Хатолик юз берди. Илтимос, қайтадан уриниб кўринг.")

if __name__ == "__main__":
    bot.infinity_polling()
