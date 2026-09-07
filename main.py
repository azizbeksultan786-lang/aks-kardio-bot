#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

BOT_TOKEN = "8752299671:AAFAl6n_xB-pFqBZHtid1pg8wzfUupo6xws"
ADMIN_ID = 1410222406

CLINIC_NAME = "AKS.uz | Azizbek Kardio Senter"
CLINIC_PHONE = "+998 90 621 03 03"
CLINIC_PHONE2 = "+998 55 201 83 33"
CLINIC_ADDRESS = "Andijon vil., Shaxrixon tumani, Barkamolavlod MFY, Ortish ko'cha 231-uy"

SERVICES = {
    "ekg": {"name": "Yurak EKG", "price": 50000},
    "echo": {"name": "Ehokardiografiya", "price": 150000},
    "holter": {"name": "Holter monitoring", "price": 200000},
    "pressure": {"name": "Qon bosimi monitoring", "price": 80000},
    "load": {"name": "Yuklama testi", "price": 120000},
    "consult": {"name": "Konsultatsiya", "price": 100000},
    "ai": {"name": "AI Shifokor maslahati", "price": 25000},
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🩺 Xizmatlar va narxlar", callback_data='services')],
        [InlineKeyboardButton("📅 Qabulga yozilish", callback_data='book')],
        [InlineKeyboardButton("🤖 AI Shifokor", callback_data='ai_doctor')],
        [InlineKeyboardButton("💳 To'lov qilish", callback_data='payment')],
        [InlineKeyboardButton("📞 Aloqa va Manzil", callback_data='contact')],
        [InlineKeyboardButton("🏥 Shifoxona haqida", callback_data='about')],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"🏥 <b>{CLINIC_NAME}</b>\n\n"
        f"Assalomu alaykum, {user.first_name}!\n\n"
        f"Azizbek Kardio Senter rasmiy botiga xush kelibsiz.\n"
        f"Quyidagi bo'limlardan birini tanlang:"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard(), parse_mode='HTML')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'main_menu':
        await query.edit_message_text(f"🏥 <b>{CLINIC_NAME}</b>\n\nAsosiy menyu:", reply_markup=get_main_keyboard(), parse_mode='HTML')

    elif data == 'services':
        text = "🩺 <b>Bizning xizmatlar va narxlar:</b>\n\n"
        for key, service in SERVICES.items():
            text += f"• <b>{service['name']}</b>: {service['price']:,} so'm\n"
        keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data='main_menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

    elif data == 'contact':
        text = (
            f"📞 <b>Aloqa va Manzil:</b>\n\n"
            f"📍 Manzil: {CLINIC_ADDRESS}\n"
            f"📞 Tel: {CLINIC_PHONE}\n"
            f"📞 Tel 2: {CLINIC_PHONE2}\n"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data='main_menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

    elif data == 'about':
        text = f"🏥 <b>{CLINIC_NAME}</b>\n\nZamonaviy kardio-diagnostika va davolash markazi."
        keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data='main_menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    print("AKS Bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    main()
