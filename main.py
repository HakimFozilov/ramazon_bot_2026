import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ================== 1. SOZLAMALAR ==================
BOT_TOKEN = "8530943208:AAEajaRL3UFD6jNqkAUs5POFpD9WO03wDGE"
CHANNEL_USERNAME = "@Sangzoruz1"

# Toshkent vaqti asosida 30 kunlik jadval (2026-yil)
TASHKENT_BASE = {
    "19-02": {"sah": "05:51", "ift": "18:04", "day": 1}, "20-02": {"sah": "05:50", "ift": "18:05", "day": 2},
    "21-02": {"sah": "05:49", "ift": "18:06", "day": 3}, "22-02": {"sah": "05:48", "ift": "18:08", "day": 4},
    "23-02": {"sah": "05:46", "ift": "18:09", "day": 5}, "24-02": {"sah": "05:45", "ift": "18:10", "day": 6},
    "25-02": {"sah": "05:43", "ift": "18:11", "day": 7}, "26-02": {"sah": "05:42", "ift": "18:12", "day": 8},
    "27-02": {"sah": "05:41", "ift": "18:13", "day": 9}, "28-02": {"sah": "05:39", "ift": "18:14", "day": 10},
    "01-03": {"sah": "05:38", "ift": "18:15", "day": 11}, "02-03": {"sah": "05:36", "ift": "18:16", "day": 12},
    "03-03": {"sah": "05:35", "ift": "18:17", "day": 13}, "04-03": {"sah": "05:33", "ift": "18:18", "day": 14},
    "05-03": {"sah": "05:32", "ift": "18:20", "day": 15}, "06-03": {"sah": "05:30", "ift": "18:21", "day": 16},
    "07-03": {"sah": "05:29", "ift": "18:22", "day": 17}, "08-03": {"sah": "05:27", "ift": "18:23", "day": 18},
    "09-03": {"sah": "05:26", "ift": "18:24", "day": 19}, "10-03": {"sah": "05:24", "ift": "18:25", "day": 20},
    "11-03": {"sah": "05:22", "ift": "18:26", "day": 21}, "12-03": {"sah": "05:21", "ift": "18:27", "day": 22},
    "13-03": {"sah": "05:19", "ift": "18:28", "day": 23}, "14-03": {"sah": "05:17", "ift": "18:29", "day": 24},
    "15-03": {"sah": "05:16", "ift": "18:30", "day": 25}, "16-03": {"sah": "05:14", "ift": "18:31", "day": 26},
    "17-03": {"sah": "05:12", "ift": "18:32", "day": 27}, "18-03": {"sah": "05:11", "ift": "18:33", "day": 28},
    "19-03": {"sah": "05:09", "ift": "18:34", "day": 29}, "20-03": {"sah": "05:07", "ift": "18:36", "day": 30}
}

# O'zbekiston viloyatlari offsetlari
REGIONS = {
    "Toshkent": 0, "Andijon": -12, "Namangan": -10, "Farg'ona": -10,
    "Guliston": 2, "Jizzax": 8, "Samarqand": 9, "Buxoro": 21,
    "Navoiy": 15, "Qarshi": 22, "Termiz": 25, "Urganch": 35, "Nukus": 35
}

user_settings = {}
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# ================== 2. FUNKSIYALAR ==================

async def check_sub(user_id):
    try:
        m = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return m.status in ("member", "administrator", "creator")
    except: return False

def shift_time(t_str, m):
    t = datetime.strptime(t_str, "%H:%M")
    return (t + timedelta(minutes=m)).strftime("%H:%M")

# ================== 3. DUOLAR ==================

SAHARLIK_DUO = (
    "<b>🌙 Saharlik (og'iz yopish) duosi:</b>\n"
    "<i>Navaytu an asuma sovma shahri ramazona minal fajri ilal mag‘ribi, xolisan lillahi ta’ala. Allohu akbar.</i>\n\n"
    "<b>Ma'nosi:</b> Ramazon oyining ro‘zasini subhdan to kun botguncha tutmoqni niyat qildim. Xolis Alloh uchun. Alloh buyukdir."
)

IFTORLIK_DUO = (
    "<b>🌇 Iftorlik (og'iz ochish) duosi:</b>\n"
    "<i>Allohumma laka sumtu va bika amantu va a’layka tavakkaltu va a’la rizqika aftartu, fag‘firli ya g‘offaru ma qoddamtu va ma axxortu.</i>\n\n"
    "<b>Ma'nosi:</b> Ey Alloh, ushbu Ro‘zamni Sen uchun tutdim va Senga iymon keltirdim va Senga tavakkal qildim va bergan rizqing bilan iftor qildim. Gunohlarni kechiruvchi Zot, avvalgi va keyingi gunohlarimni mag‘firat qilgin."
)

# ================== 4. HANDLERLAR ==================

def get_regions_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for city in REGIONS.keys():
        kb.add(KeyboardButton(city))
    return kb

def get_main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(KeyboardButton("🕌 Bugungi taqvim"), KeyboardButton("📍 Hududni o'zgartirish"))
    return kb

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not await check_sub(message.from_user.id):
        btn = InlineKeyboardMarkup().add(InlineKeyboardButton("➕ Obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
        btn.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check"))
        return await message.answer(f"Botdan foydalanish uchun {CHANNEL_USERNAME} kanaliga obuna bo'ling!", reply_markup=btn)
    await message.answer("Assalomu alaykum! Viloyatingizni tanlang:", reply_markup=get_regions_kb())

@dp.callback_query_handler(text="check")
async def check_cb(call: types.CallbackQuery):
    if await check_sub(call.from_user.id):
        await call.message.delete()
        await call.message.answer("Obuna tasdiqlandi! Viloyatni tanlang:", reply_markup=get_regions_kb())
    else:
        await call.answer("Siz hali kanalga a'zo emassiz! ❌", show_alert=True)

@dp.message_handler(lambda m: m.text in REGIONS)
async def set_region(message: types.Message):
    user_settings[message.from_user.id] = message.text
    await message.answer(f"✅ Hudud <b>{message.text}</b> qilib belgilandi!", parse_mode="HTML", reply_markup=get_main_menu())

@dp.message_handler(lambda m: m.text == "📍 Hududni o'zgartirish")
async def change_reg(message: types.Message):
    await message.answer("Yangi viloyatni tanlang:", reply_markup=get_regions_kb())

@dp.message_handler(lambda m: m.text == "🕌 Bugungi taqvim")
async def show_daily(message: types.Message):
    user_id = message.from_user.id
    if not await check_sub(user_id): return await start(message)

    city = user_settings.get(user_id)
    if not city: return await message.answer("Iltimos, avval viloyatingizni tanlang!", reply_markup=get_regions_kb())

    today = datetime.now().strftime("%d-%m")
    
    if today in TASHKENT_BASE:
        data = TASHKENT_BASE[today]
        offset = REGIONS[city]
        
        sah = shift_time(data['sah'], offset)
        ift = shift_time(data['ift'], offset)
        
        resp = (
            f"📅 <b>Bugun: {datetime.now().strftime('%d.%m.%Y')}</b>\n"
            f"📍 Hudud: <b>{city}</b>\n"
            f"🌙 Ramazonning <b>{data['day']}-kuni</b>\n"
            f"──────────────────\n"
            f"🍽 Saharlik: <b>{sah}</b>\n"
            f"🌇 Iftorlik: <b>{ift}</b>\n"
            f"──────────────────\n\n"
            f"{SAHARLIK_DUO}\n\n"
            f"{IFTORLIK_DUO}"
        )
        await message.answer(resp, parse_mode="HTML")
    else:
        # Ramazon kunlaridan tashqari vaqt bo'lsa
        await message.answer("⚠️ Bugungi sana uchun Ramazon taqvimi mavjud emas (Ramazon hali boshlanmagan yoki tugagan).")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)