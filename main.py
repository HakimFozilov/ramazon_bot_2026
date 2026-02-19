import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ================== 1. SOZLAMALAR ==================
BOT_TOKEN = "8530943208:AAEajaRL3UFD6jNqkAUs5POFpD9WO03wDGE"
CHANNEL_USERNAME = "@Sangzoruz1"

# O'zbekiston vaqti (Toshkent bazasi)
TASHKENT_BASE = {
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
} 

# Turkiya vaqti (Istanbul bazasi - Rasmdan olindi)
ISTANBUL_BASE = {
    ISTANBUL_BASE = {
    "19-02": {"sah": "06:22", "ift": "18:50", "day": 1},
    "20-02": {"sah": "06:20", "ift": "18:51", "day": 2},
    "21-02": {"sah": "06:19", "ift": "18:53", "day": 3},
    "22-02": {"sah": "06:18", "ift": "18:54", "day": 4},
    "23-02": {"sah": "06:16", "ift": "18:55", "day": 5},
    "24-02": {"sah": "06:15", "ift": "18:56", "day": 6},
    "25-02": {"sah": "06:13", "ift": "18:57", "day": 7},
    "26-02": {"sah": "06:12", "ift": "18:59", "day": 8},
    "27-02": {"sah": "06:10", "ift": "19:00", "day": 9},
    "28-02": {"sah": "06:09", "ift": "19:01", "day": 10},
    "01-03": {"sah": "06:08", "ift": "19:02", "day": 11},
    "02-03": {"sah": "06:06", "ift": "19:03", "day": 12},
    "03-03": {"sah": "06:04", "ift": "19:04", "day": 13},
    "04-03": {"sah": "06:03", "ift": "19:05", "day": 14},
    "05-03": {"sah": "06:01", "ift": "19:07", "day": 15},
    "06-03": {"sah": "06:00", "ift": "19:08", "day": 16},
    "07-03": {"sah": "05:58", "ift": "19:09", "day": 17},
    "08-03": {"sah": "05:56", "ift": "19:10", "day": 18},
    "09-03": {"sah": "05:55", "ift": "19:11", "day": 19},
    "10-03": {"sah": "05:53", "ift": "19:12", "day": 20},
    "11-03": {"sah": "05:51", "ift": "19:13", "day": 21},
    "12-03": {"sah": "05:50", "ift": "19:14", "day": 22},
    "13-03": {"sah": "05:48", "ift": "19:15", "day": 23},
    "14-03": {"sah": "05:46", "ift": "19:17", "day": 24},
    "15-03": {"sah": "05:45", "ift": "19:18", "day": 25},
    "16-03": {"sah": "05:43", "ift": "19:19", "day": 26},
    "17-03": {"sah": "05:41", "ift": "19:20", "day": 27},
    "18-03": {"sah": "05:39", "ift": "19:21", "day": 28},
    "19-03": {"sah": "05:38", "ift": "19:22", "day": 29},
    "20-03": {"sah": "05:36", "ift": "19:24", "day": 30} # Qadr kechasi/Hayit arafasi
}

# Hududlar
REGIONS_UZ = {
    "Toshkent": 0, "Andijon": -12, "Namangan": -10, "Farg'ona": -10,
    "Guliston": 2, "Jizzax": 8, "Samarqand": 9, "Buxoro": 21,
    "Navoiy": 15, "Qarshi": 22, "Termiz": 25, "Urganch": 35, "Nukus": 35
}

REGIONS_TR = {
    # Shahar nomi: Istanbulga nisbatan farqi (minutlarda)
    "Istanbul": 0,
    "Anqara": -14,       # Istanbuldan 14 daqiqa oldin
    "Izmir": 14,         # Istanbuldan 14 daqiqa keyin
    "Bursa": 2,          # Istanbuldan 2 daqiqa keyin
    "Antalya": 4,        # Istanbuldan 4 daqiqa keyin
    "Adana": -20,        # Istanbuldan 20 daqiqa oldin
    "Konya": -10,        # Istanbuldan 10 daqiqa oldin
    "Gaziantep": -28,    # Istanbuldan 28 daqiqa oldin
    "Kayseri": -19,      # Istanbuldan 19 daqiqa oldin
    "Erzurum": -42,      # Istanbuldan 42 daqiqa oldin (Sharqiy hudud)
    "Samsun": -21,       # Istanbuldan 21 daqiqa oldin
    "Trabzon": -31,      # Istanbuldan 31 daqiqa oldin
    "Eskishehir": -4,    # Istanbuldan 4 daqiqa oldin
    "Denizli": 9,        # Istanbuldan 9 daqiqa keyin
    "Mersin": -18,       # Istanbuldan 18 daqiqa oldin
    "Diyarbakir": -37,   # Istanbuldan 37 daqiqa oldin
    "Shanliurfa": -31    # Istanbuldan 31 daqiqa oldin
} 

user_settings = {} # {user_id: {'country': 'UZ', 'city': 'Toshkent'}}

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

# ================== 3. KEYBOARDLAR ==================

def get_country_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🇺🇿 O'zbekiston"), KeyboardButton("🇹🇷 Turkiya"))
    return kb

def get_regions_kb(country):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    regions = REGIONS_UZ if country == "UZ" else REGIONS_TR
    for city in regions.keys():
        kb.add(KeyboardButton(city))
    kb.add(KeyboardButton("⬅️ Orqaga"))
    return kb

def get_main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(KeyboardButton("🕌 Bugungi taqvim"), KeyboardButton("🕌 Ertangi taqvim"))
    kb.add(KeyboardButton("📍 Hududni o'zgartirish"))
    return kb

# ================== 4. HANDLERLAR ==================

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not await check_sub(message.from_user.id):
        btn = InlineKeyboardMarkup().add(InlineKeyboardButton("➕ Obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
        btn.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check"))
        return await message.answer(f"Botdan foydalanish uchun {CHANNEL_USERNAME} kanaliga obuna bo'ling!", reply_markup=btn)
    await message.answer(f"Assalomu alaykum! Davlatni tanlang:", reply_markup=get_country_kb())

@dp.message_handler(lambda m: m.text in ["🇺🇿 O'zbekiston", "🇹🇷 Turkiya"])
async def select_country(message: types.Message):
    country = "UZ" if "O'zbekiston" in message.text else "TR"
    user_settings[message.from_user.id] = {'country': country}
    await message.answer("Hududni tanlang:", reply_markup=get_regions_kb(country))

@dp.message_handler(lambda m: m.text == "⬅️ Orqaga")
async def go_back(message: types.Message):
    await start(message)

@dp.message_handler(lambda m: m.text in list(REGIONS_UZ.keys()) + list(REGIONS_TR.keys()))
async def set_region(message: types.Message):
    if message.from_user.id not in user_settings:
        return await start(message)
    
    user_settings[message.from_user.id]['city'] = message.text
    await message.answer(f"✅ <b>{message.text}</b> tanlandi!", parse_mode="HTML", reply_markup=get_main_menu())

@dp.message_handler(lambda m: m.text == "📍 Hududni o'zgartirish")
async def change_reg(message: types.Message):
    await start(message)

async def send_calendar(message, date_obj, title_prefix):
    user_id = message.from_user.id
    settings = user_settings.get(user_id)
    if not settings or 'city' not in settings: 
        return await message.answer("Iltimos, avval hududni tanlang!", reply_markup=get_country_kb())

    date_str = date_obj.strftime("%d-%m")
    country = settings['country']
    city = settings['city']
    
    # Ma'lumotlar bazasini tanlash
    base_data = TASHKENT_BASE if country == "UZ" else ISTANBUL_BASE
    offsets = REGIONS_UZ if country == "UZ" else REGIONS_TR

    if date_str in base_data:
        data = base_data[date_str]
        offset = offsets[city]
        
        sah = shift_time(data['sah'], offset)
        ift = shift_time(data['ift'], offset)
        
        # Duolarni kodga qo'shib qo'yish kerak (avvalgi kodingizdagi SAHARLIK_DUO va h.k)
        from __main__ import SAHARLIK_DUO, IFTORLIK_DUO 

        resp = (
            f"📅 <b>{title_prefix}: {date_obj.strftime('%d.%m.%Y')}</b>\n"
            f"📍 Hudud: <b>{city} ({'Oʻzbekiston' if country=='UZ' else 'Turkiya'})</b>\n"
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
        await message.answer(f"⚠️ {date_obj.strftime('%d.%m.%Y')} sanasi uchun taqvim kiritilmagan.")

# ... (Qolgan handlerlar bir xil qoladi)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)