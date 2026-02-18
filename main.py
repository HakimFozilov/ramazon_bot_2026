import logging
import requests
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from geopy.distance import geodesic

# ================== 1. SOZLAMALAR ==================
BOT_TOKEN = "8530943208:AAEajaRL3UFD6jNqkAUs5POFpD9WO03wDGE"
CHANNEL_USERNAME = "@Sangzoruz1"

# Toshkent vaqti (Asosiy jadval - Muslim.uz / 2026-yil)
TASHKENT_BASE = {
    "19-02": {"sah": "05:51", "ift": "18:04", "day": 1},
    "20-02": {"sah": "05:50", "ift": "18:05", "day": 2},
    "21-02": {"sah": "05:49", "ift": "18:06", "day": 3},
    "22-02": {"sah": "05:48", "ift": "18:08", "day": 4},
    "23-02": {"sah": "05:46", "ift": "18:09", "day": 5},
    "24-02": {"sah": "05:45", "ift": "18:10", "day": 6},
    "25-02": {"sah": "05:43", "ift": "18:11", "day": 7},
    "26-02": {"sah": "05:42", "ift": "18:12", "day": 8},
    "27-02": {"sah": "05:41", "ift": "18:13", "day": 9},
    "28-02": {"sah": "05:39", "ift": "18:14", "day": 10},
    "01-03": {"sah": "05:38", "ift": "18:15", "day": 11},
    "02-03": {"sah": "05:36", "ift": "18:16", "day": 12},
    "03-03": {"sah": "05:35", "ift": "18:17", "day": 13},
    "04-03": {"sah": "05:33", "ift": "18:18", "day": 14},
    "05-03": {"sah": "05:32", "ift": "18:20", "day": 15},
    "06-03": {"sah": "05:30", "ift": "18:21", "day": 16},
    "07-03": {"sah": "05:29", "ift": "18:22", "day": 17},
    "08-03": {"sah": "05:27", "ift": "18:23", "day": 18},
    "09-03": {"sah": "05:34", "ift": "18:24", "day": 19},
    "10-03": {"sah": "05:32", "ift": "18:25", "day": 20},
    "11-03": {"sah": "05:30", "ift": "18:26", "day": 21},
    "12-03": {"sah": "05:29", "ift": "18:27", "day": 22},
    "13-03": {"sah": "05:27", "ift": "18:28", "day": 23},
    "14-03": {"sah": "05:25", "ift": "18:29", "day": 24},
    "15-03": {"sah": "05:24", "ift": "18:30", "day": 25},
    "16-03": {"sah": "05:22", "ift": "18:31", "day": 26},
    "17-03": {"sah": "05:12", "ift": "18:32", "day": 27},
    "18-03": {"sah": "05:11", "ift": "18:33", "day": 28},
    "19-03": {"sah": "05:09", "ift": "18:34", "day": 29},
    "20-03": {"sah": "05:07", "ift": "18:36", "day": 30}
}

# Viloyat offsetlari
REGIONS_OFFSET = {
    "Toshkent": 0, "Andijon": -12, "Namangan": -10, "Farg'ona": -10,
    "Guliston": 2, "Jizzax": 8, "Samarqand": 9, "Buxoro": 21,
    "Navoiy": 15, "Qarshi": 22, "Termiz": 25, "Urganch": 35, "Nukus": 35
}

user_data = {}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# ================== 2. FUNKSIYALAR ==================

async def is_subscribed(user_id):
    try:
        chat_member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

def add_mins(t_str, m):
    return (datetime.strptime(t_str, "%H:%M") + timedelta(minutes=m)).strftime("%H:%M")

def get_external_api_times(lat, lon):
    url = f"https://api.aladhan.com/v1/timings/{int(datetime.now().timestamp())}"
    params = {"latitude": lat, "longitude": lon, "method": 3}
    try:
        r = requests.get(url, params=params).json()
        return r['data']['timings']['Fajr'], r['data']['timings']['Maghrib']
    except:
        return None, None

# ================== 3. TEXTLAR ==================

SAHARLIK_DUO = (
    "<b>Saharlik duosi:</b>\n"
    "Navaytu an asuma sovma shahri ramazona minal fajri ilal mag‘ribi, xolisan lillahi ta’ala. Allohu akbar.\n\n"
    "<i>Ramazon oyining ro‘zasini subhdan to kun botguncha tutmoqni niyat qildim. Xolis Alloh uchun.</i>"
)

IFTORLIK_DUO = (
    "<b>Iftorlik duosi:</b>\n"
    "Allohumma laka sumtu va bika amantu va a’layka tavakkaltu va a’la rizqika aftartu, fag‘firli ya g‘offaru ma qoddamtu va ma axxortu.\n\n"
    "<i>Ey Alloh, ushbu Ro‘zamni Sen uchun tutdim va Senga iymon keltirdim va Senga tavakkal qildim.</i>"
)

# ================== 4. HANDLERLAR ==================

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if not await is_subscribed(message.from_user.id):
        btn = InlineKeyboardMarkup().add(InlineKeyboardButton("Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
        btn.add(InlineKeyboardButton("Tekshirish", callback_data="check"))
        return await message.answer(f"Botdan foydalanish uchun {CHANNEL_USERNAME} kanaliga obuna bo'ling!", reply_markup=btn)
    
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("📍 Joylashuv yuborish", request_location=True))
    await message.answer(f"Assalomu alaykum, {message.from_user.first_name}! Viloyatni aniqlash uchun joylashuv yuboring:", reply_markup=kb)

@dp.callback_query_handler(text="check")
async def check_sub(call: types.CallbackQuery):
    if await is_subscribed(call.from_user.id):
        await call.message.delete()
        await cmd_start(call.message)
    else:
        await call.answer("Hali obuna bo'lmabsiz ❌", show_alert=True)

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    if not await is_subscribed(message.from_user.id):
        return await cmd_start(message)
        
    lat, lon = message.location.latitude, message.location.longitude
    # Eng yaqin viloyatni aniqlash (oddiy usulda)
    user_data[message.from_user.id] = {'lat': lat, 'lon': lon, 'city': 'Aniqlanmoqda...'}
    
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add("🕌 Namoz vaqtlari", "🌙 Ramazon taqvimi", "📍 Joylashuvni yangilash")
    await message.answer("Joylashuv saqlandi! Quyidagilardan birini tanlang:", reply_markup=kb)

@dp.message_handler(lambda m: m.text == "🕌 Namoz vaqtlari")
async def show_times(message: types.Message):
    user_id = message.from_user.id
    if not await is_subscribed(user_id):
        return await cmd_start(message)
        
    today = datetime.now().strftime("%d-%m")
    # Bu yerda Jizzaxni misol qilib olamiz yoki offsetni hisoblaymiz
    if today in TASHKENT_BASE:
        t_data = TASHKENT_BASE[today]
        # Jizzax offseti (+8 daqiqa rasmga ko'ra)
        sah = add_mins(t_data['sah'], 8)
        ift = add_mins(t_data['ift'], 8)
        
        res = (
            f"📅 {datetime.now().strftime('%d.%m.%Y')}\n"
            f"📍 Jizzax viloyati\n"
            f"🌙 {t_data['day']}-Ramazon\n\n"
            f"⏰ Saharlik: <b>{sah}</b>\n"
            f"🌇 Iftorlik: <b>{ift}</b>\n\n"
            f"{SAHARLIK_DUO}\n\n"
            f"{IFTORLIK_DUO}"
        )
        await message.answer(res, parse_mode="HTML")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)