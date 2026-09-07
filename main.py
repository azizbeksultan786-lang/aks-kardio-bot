import os
import google.generativeai as genai
from telebot import TeleBot

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_KEY)

system_instruction = """
Сиз "Aks Shifoxonasi" нинг тиббий сунъий интеллект ассистентисиз.
Вазифаларингиз:
1. Кардиология ва умумий тиббиёт бўйича аниқ, асосланган маълумот бериш.
2. МКБ-10 (ICD-10) кодларини тавсифлаш ва касаллик номидан МКБ-10 кодини топиш.
3. Бемор ёки шифокор ЭКГ, лаборатория таҳлили ёки УЗИ хулосаси суратини юборса, суратдаги кўрсаткичларни таҳлил қилиб, нормадан четлашишларни кўрсатиш ва дастлабки мулоҳаза бериш.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", system_instruction=system_instruction
)
bot = TeleBot(TELEGRAM_TOKEN)


# Матнли хабарлар (МКБ-10 ва тиббий маслаҳат)
@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_text(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Хатолик: {e}")


# Суратлар (ЭКГ ва таҳлил натижалари)
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        image_data = [{"mime_type": "image/jpeg", "data": downloaded_file}]

        prompt = "Ушбу тиббий таҳлил, ЭКГ ёки хулоса суратини диққат билан ўрганиб чиқ ва асосий кўрсаткичларни, нормадан четлашишларни таҳлил қилиб бер."

        response = model.generate_content([prompt, image_data[0]])
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Суратни таҳлил қилишда хатолик: {e}")


if __name__ == "__main__":
    bot.infinity_polling()
