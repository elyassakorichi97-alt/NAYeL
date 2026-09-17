from flask import Flask
import threading, telebot
from telebot import types
import os
from datetime import datetime

app = Flask(__name__)
@app.route('/')
def home(): return "NAYeL Bot 24/7 - OK"
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()

TOKEN = "8964409122:AAF9M4bJGXKxFiQmmqwKy3eEO9DCR5wH450"
ADMIN_ID = 8460089959
BARIDI = "00799999001377604197"
FLEXY = "0674477994"

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(m):
    user_data[m.chat.id] = {}
    bot.send_message(m.chat.id, "🎮 مرحبا بيك في متجر NAYeL 🔥\n\n📱 ابعث الـ ID تاعك في اللعبة:")
    bot.register_next_step_handler(m, step_id)

def step_id(m):
    user_data[m.chat.id]['game_id'] = m.text
    bot.send_message(m.chat.id, f"✅ ID: {m.text}\n\n💎 واش من عرض حاب؟")
    bot.register_next_step_handler(m, step_offer)

def step_offer(m):
    user_data[m.chat.id]['offer'] = m.text
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add("💳 بريدي موب", "📱 فليكسي")
    bot.send_message(m.chat.id, "💰 كيفاش تخلص؟", reply_markup=kb)
    bot.register_next_step_handler(m, step_pay)

def step_pay(m):
    user_data[m.chat.id]['pay'] = m.text
    txt = f"💳 بريدي موب:\n`{BARIDI}`\n\nخلص وابعت سكرين 📸" if "بريدي" in m.text else f"📱 فليكسي:\n`{FLEXY}`\n\nخلص وابعت سكرين 📸"
    bot.send_message(m.chat.id, txt, parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(content_types=['photo'])
def get_photo(m):
    if m.chat.id not in user_data: return bot.send_message(m.chat.id, "/start")
    d = user_data[m.chat.id]
    cap = f"🔥 طلب NAYeL 🔥\n👤 @{m.from_user.username or 'بدون'}\n🆔 {m.chat.id}\n🎮 {d['game_id']}\n💎 {d['offer']}\n💳 {d['pay']}\n⏰ {datetime.now():%Y-%m-%d %H:%M}"
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(ADMIN_ID, cap)
    bot.send_message(m.chat.id, "✅ تم! راح نشحنولك ضرك ⏳")
    user_data.pop(m.chat.id, None)

bot.infinity_polling()
