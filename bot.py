from flask import Flask
import threading
import telebot
from telebot import types
import random
from datetime import datetime

app = Flask(__name__)
@app.route('/')
def home(): return "NAYeL Bot Running 24/7"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()

TOKEN = "8964409122:AAF9M4bJGXKxFiQmmqwKy3eEO9DCR5wH450"
ADMIN_ID = 8460089959
BARIDI = "00799999001377604197"
FLEXY = "0674477994"

PACKS = {"13k":{"label":"13,000","b":500,"f":650},"26k":{"label":"26,000","b":1000,"f":1300},"52k":{"label":"52,000","b":2000,"f":2600},"100k":{"label":"100,000","b":3850,"f":5000},"130k":{"label":"130,000","b":5000,"f":6500},"260k":{"label":"260,000","b":10000,"f":13000},"500k":{"label":"500,000","b":19000,"f":25000},"1M":{"label":"1,000,000","b":38000,"f":50000},"2M":{"label":"2,000,000","b":76000,"f":100000},"4M":{"label":"4,000,000","b":150000,"f":200000}}

bot = telebot.TeleBot(TOKEN)
user_data = {}

def main_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    for k in PACKS: kb.add(types.InlineKeyboardButton(f"💎 {k}", callback_data=f"pack_{k}"))
    kb.add(types.InlineKeyboardButton("💳 طرق الدفع", callback_data="howtopay"), types.InlineKeyboardButton("📜 القوانين", callback_data="rules"))
    return kb

def pay_method_kb(pack_key):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(f"💳 بريدي - {PACKS[pack_key]['b']} دج", callback_data=f"pay_baridi_{pack_key}"))
    kb.add(types.InlineKeyboardButton(f"📱 فليكسي - {PACKS[pack_key]['f']} دج", callback_data=f"pay_flexy_{pack_key}"))
    kb.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_home"))
    return kb

@bot.message_handler(commands=['start'])
def start(m):
    txt = f"🔥 NAYeL STORE 🔥\nمرحبا {m.from_user.first_name} 👋\n\n⚡ شحن فوري 10 دقايق\n💯 ضمان 100%\n👇 اختر الكمية:"
    bot.send_message(m.chat.id, txt, reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: c.data.startswith("pack_"))
def choose_pack(c):
    pack_key = c.data.split("_")[1]
    user_data[c.from_user.id] = {"pack": pack_key}
    bot.edit_message_text(f"📦 اخترت: {PACKS[pack_key]['label']}\nاختر الدفع 👇", c.message.chat.id, c.message.message_id, reply_markup=pay_method_kb(pack_key))

@bot.callback_query_handler(func=lambda c: c.data.startswith("pay_"))
def choose_pay(c):
    _, method, pack_key = c.data.split("_")
    data = PACKS[pack_key]
    order_id = random.randint(10000, 99999)
    price = data['b'] if method == 'baridi' else data['f']
    if method == 'baridi':
        txt = f"✅ فاتورة #{order_id}\n📦 {data['label']} سوجو\n💵 {price} دج\n\n🔢 بريدي:\n`{BARIDI}`\n\nبعد الدفع ابعث ID + صورة"
    else:
        txt = f"✅ فاتورة #{order_id}\n📦 {data['label']} سوجو\n💵 {price} دج\n\n📱 فليكسي:\n`{FLEXY}`\n\n⚠️ لازم تصور كابتير كامل فيه التاريخ والوقت\n❌ ممنوع الصورة المقطعة"
    bot.send_message(c.message.chat.id, txt, parse_mode="Markdown")
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: True)
def other_cb(c):
    if c.data == "back_home":
        txt = f"🔥 NAYeL STORE 🔥\n👇 اختر الكمية:"
        bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, reply_markup=main_kb())
    elif c.data == "howtopay": bot.send_message(c.message.chat.id, f"💳 بريدي: `{BARIDI}`\n📱 فليكسي: `{FLEXY}`\nلازم كابتير كامل بالوقت والتاريخ", parse_mode="Markdown")
    elif c.data == "rules": bot.send_message(c.message.chat.id, "📜 القوانين:\n1- تأكد من ID\n2- فليكسي كابتير كامل + تاريخ ووقت\n3- الصور المقطعة مرفوضة")
    bot.answer_callback_query(c.id)

@bot.message_handler(content_types=['text','photo'])
def order_handler(m):
    if m.text and m.text.startswith('/'): return
    info = user_data.get(m.from_user.id, {})
    admin_msg = f"🔥 طلب جديد\n👤 {m.from_user.first_name} @{m.from_user.username}\n🆔 {m.from_user.id}\n📦 {info.get('pack','غير محدد')}\n💬 {m.text if m.text else 'صورة'}\n⏰ {datetime.now()}"
    try:
        if m.content_type == 'photo': bot.send_photo(ADMIN_ID, m.photo[-1].file_id, caption=admin_msg)
        else: bot.send_message(ADMIN_ID, admin_msg)
        bot.send_message(m.chat.id, "✅ تم الاستلام، سيتم الشحن قريبا.")
    except: pass

print("Bot Running...")
bot.infinity_polling()
