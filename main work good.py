import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters,
    CallbackContext, ConversationHandler
)

# Состояния для ConversationHandler
STATE_LANGUAGE_SELECT = 1000
STATE_LOCATION = 0
STATE_CITY = 1
STATE_TRANSLATE = 2
STATE_CONVERT = 3
STATE_CONVERT_FROM = 4
STATE_CONVERT_TO = 5
STATE_CONVERT_AMOUNT = 6
STATE_SELECT_EXCURSION_CATEGORY = 10
STATE_TRANSLATE_FROM = 21
STATE_TRANSLATE_INPUT = 22
STATE_TRANSLATE_TO = 23

LANGUAGES = {
    "en": "Английский",
    "ru": "Русский",
    "fr": "Французский",
    "de": "Немецкий",
    "es": "Испанский",
    "it": "Итальянский",
    "ja": "Японский",
    "zh": "Китайский",
    "pt": "Португальский",
    "ar": "Арабский",
    "bg": "Български"
}
ISO_639_1_TO_3 = {
    "en": "eng",
    "es": "spa",
    "pt": "por",
    "ru": "rus",
    "fr": "fra",
    "uk": "ukr",
    "pl": "pol",
    # добавьте другие необходимые пары
}
SUPPORTED_PAIRS = {
    ("eng", "spa"),
    ("spa", "eng"),
    ("eng", "por"),
    ("por", "eng"),
    ("eng", "fra"),
    ("fra", "eng"),
    ("eng", "ukr"),
    ("ukr", "eng"),
    ("eng", "pol"),
    ("pol", "eng"),
}

# Токены и заголовки
BOT_TOKEN = "7172554336:AAGq9dBFe049P5kFa7DlyX1VPom4zBTo0Sw"
LOCATIONIQ_TOKEN = "pk.be776699fbad9b419e09755dc6fdcc67"

HEADERS = {
    "User-Agent": "TelegramTravelBot/1.0 (example@example.com)"
}

translations = {
    "en": {
        "start_menu": [
            "📍 Send location",
            "🏨 Find hotels",
            "🗽 Find attractions",
            "🚍 Transport info",
            "🎫 Choose excursions",
            "🌤 City weather",
            "💱 Currency converter",
            "🌐 Text translation",
            "🚪 Exit"
        ],
        "greeting": "Hello! Choose an action:",
        "back": "Back to menu",
        "location_received": "Location received. What would you like to do next?",
        "goodbye": "Goodbye!",
        "invalid_choice": "Please choose an action using the button.",
        "select_excursion_category": "Choose excursion category:",
        "excursion_museums": "🏛 Museums",
        "excursion_galleries": "🖼 Galleries",
        "excursion_parks": "🎢 Parks/Attractions",
        "excursion_historic": "🏰 Historical places",
        "select_source_language": "Choose source language:",
        "enter_text_to_translate": "Enter text to translate:",
        "select_target_language": "Choose target language:",
        "translation_cancelled": "Translation cancelled.",
        "choose_language_list": "Please choose a language from the list.",
        "translation_result_prefix": "Translation:",
        "translation_failed": "Translation was unsuccessful.",
        "enter_amount_and_currencies": "💱 Enter amount and currencies, e.g. `100 USD in EUR`",
        "amount_not_recognized": "❌ The amount could not be recognized.",
        "currency_not_supported": "❌ Currency must be one of: {}",
        "conversion_failed": "Conversion failed. Please try again later.",
        "cancel": "Cancel"
    },
    "ru": {
        "start_menu": [
            "📍 Отправить локацию",
            "🏨 Найти отели",
            "🗽 Найти достопримечательности",
            "🚍 Информация о транспорте",
            "🎫 Выбор экскурсий",
            "🌤 Погода в городе",
            "💱 Калькулятор валют",
            "🌐 Перевод текста",
            "🚪 Выход"
        ],
        "greeting": "Здравствуйте! Выберите действие:",
        "back": "Назад в меню",
        "location_received": "Локация получена. Что хотите сделать дальше?",
        "goodbye": "До свидания!",
        "invalid_choice": "Пожалуйста, выберите действие с помощью кнопок.",
        "select_excursion_category": "Выберите категорию экскурсий:",
        "excursion_museums": "🏛 Музеи",
        "excursion_galleries": "🖼 Галереи",
        "excursion_parks": "🎢 Парки/Аттракционы",
        "excursion_historic": "🏰 Исторические места",
        "select_source_language": "Выберите язык оригинала:",
        "enter_text_to_translate": "Введите текст для перевода:",
        "select_target_language": "Выберите язык перевода:",
        "translation_cancelled": "Перевод отменён.",
        "choose_language_list": "Пожалуйста, выберите язык из списка.",
        "translation_result_prefix": "Перевод:",
        "translation_failed": "Перевод не был успешным.",
        "enter_amount_and_currencies": "💱 Введите сумму и валюты, например: `100 USD в EUR`",
        "amount_not_recognized": "❌ Сумма не распознана.",
        "currency_not_supported": "❌ Валюта должна быть одной из: {}",
        "conversion_failed": "Конвертация не удалась. Попробуйте позже.",
        "cancel": "Отмена"
    },
    "bg": {
        "start_menu": [
            "📍 Изпрати локация",
            "🏨 Намери хотели",
            "🗽 Намери забележителности",
            "🚍 Информация за транспорта",
            "🎫 Избор на екскурзии",
            "🌤 Времето в града",
            "💱 Валутен калкулатор",
            "🌐 Превод на текст",
            "🚪 Изход"
        ],
        "greeting": "Здравейте! Изберете действие:",
        "back": "Назад в менюто",
        "location_received": "Локацията е получена. Какво искате да направите след това?",
        "goodbye": "Довиждане!",
        "invalid_choice": "Моля, изберете действие с бутон.",
        "select_excursion_category": "Изберете категория екскурзия:",
        "excursion_museums": "🏛 Музеи",
        "excursion_galleries": "🖼 Галерии",
        "excursion_parks": "🎢 Паркове/Атракции",
        "excursion_historic": "🏰 Исторически места",
        "select_source_language": "Изберете езика на оригиналния текст:",
        "enter_text_to_translate": "Въведете текст за превод:",
        "select_target_language": "Изберете езика, на който да преведете:",
        "translation_cancelled": "Преводът е отменен.",
        "choose_language_list": "Моля, изберете език от списъка.",
        "translation_result_prefix": "Превод:",
        "translation_failed": "Преводът не бе успешен.",
        "enter_amount_and_currencies": "💱 Въведете сума и валути, например: `100 USD в EUR`",
        "amount_not_recognized": "❌ Сумата не може да бъде разпозната.",
        "currency_not_supported": "❌ Валутата трябва да бъде една от: {}",
        "conversion_failed": "Неуспешна конверсия. Опитайте по-късно.",
        "cancel": "Отмяна"
    }
}

user_locations = {}

def language_selection_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🇷🇺 Русский"), KeyboardButton("🇧🇬 Български"), KeyboardButton("🇬🇧 English")]
    ], resize_keyboard=True)

def language_selection(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Выберите язык / Изберете език / Choose a language:",
        reply_markup=language_selection_keyboard()
    )
    return STATE_LANGUAGE_SELECT

def set_language(update: Update, context: CallbackContext):
    choice = update.message.text
    if "Русский" in choice:
        context.user_data["lang"] = "ru"
    elif "Български" in choice:
        context.user_data["lang"] = "bg"
    elif "English" in choice:
        context.user_data["lang"] = "en"
    else:
        update.message.reply_text("Неверный выбор языка.")
        return STATE_LANGUAGE_SELECT
    return start(update, context)

def start(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    update.message.reply_text(translations[lang]["greeting"], reply_markup=start_keyboard(lang))
    return STATE_LOCATION


def start_keyboard(lang):
    menu = translations[lang]["start_menu"]
    keyboard = []
    for button in menu:
        if "📍" in button:
            keyboard.append([KeyboardButton(button, request_location=True)])
        else:
            keyboard.append([KeyboardButton(button)])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Диалогът е отменен.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def location_handler(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    text = update.message.text
    if update.message.location:
        user_id = update.message.from_user.id
        loc = update.message.location
        user_locations[user_id] = (loc.latitude, loc.longitude)
        update.message.reply_text(translations[lang]["location_received"], reply_markup=start_keyboard(lang))
        return STATE_LOCATION
    elif text == translations[lang]["start_menu"][6]:
        return handle_currency_conversion(update, context)
    elif text == translations[lang]["start_menu"][2]:
        return find_attractions(update, context)
    elif text == translations[lang]["start_menu"][4]:
        return select_excursion_category(update, context)
    elif (text == translations[lang]["excursion_museums"] or text == translations[lang]["excursion_galleries"]
          or text == translations[lang]["excursion_parks"] or text == translations[lang]["excursion_historic"]):
        return filtered_excursions(update, context)
    elif text == translations[lang]["start_menu"][3]:
        return find_transport(update, context)
    elif text == translations[lang]["start_menu"][5]:
        return ask_city(update, context, purpose="weather")
    elif text == translations[lang]["start_menu"][1]:
        return find_hotels(update, context)
    elif text == translations[lang]["start_menu"][7]:
        return start_translate(update, context)
    elif text == translations[lang]["start_menu"][8]:
        update.message.reply_text(translations[lang]["goodbye"], reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        update.message.reply_text(translations[lang]["invalid_choice"], reply_markup=start_keyboard(lang))
        return STATE_LOCATION

def ask_city(update: Update, context: CallbackContext, purpose):
    lang = context.user_data.get("lang", "en")
    context.user_data["purpose"] = purpose
    # "enter_city_name" not in translations by default; using fallback text
    prompt = translations[lang].get("enter_city_name", "Enter city name:")
    update.message.reply_text(prompt,
                              reply_markup=ReplyKeyboardMarkup([[KeyboardButton(translations[lang]["back"])]], resize_keyboard=True))
    return STATE_CITY
def get_weather_description_localized(code, lang):
    descriptions = {
        "en": {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Rain showers: slight",
            81: "Rain showers: moderate",
            82: "Rain showers: violent"
        },
        "ru": {
            0: "Ясно",
            1: "Преимущественно ясно",
            2: "Переменная облачность",
            3: "Пасмурно",
            45: "Туман",
            48: "Инейный туман",
            51: "Лёгкая морось",
            53: "Умеренная морось",
            55: "Сильная морось",
            61: "Лёгкий дождь",
            63: "Умеренный дождь",
            65: "Сильный дождь",
            71: "Лёгкий снег",
            73: "Умеренный снег",
            75: "Сильный снег",
            80: "Лёгкий ливень",
            81: "Умеренный ливень",
            82: "Сильный ливень"
        },
        "bg": {
            0: "Ясно небе",
            1: "Преобладаващо ясно",
            2: "Разкъсана облачност",
            3: "Облачно",
            45: "Мъгла",
            48: "Мразовита мъгла",
            51: "Лек дъждец",
            53: "Умерен дъждец",
            55: "Силен дъждец",
            61: "Лек дъжд",
            63: "Умерен дъжд",
            65: "Силен дъжд",
            71: "Лек сняг",
            73: "Умерен сняг",
            75: "Силен сняг",
            80: "Лек порой",
            81: "Умерен порой",
            82: "Силен порой"
        }
    }
    return descriptions.get(lang, descriptions["en"]).get(code, "Unknown")

def send_weather(update: Update, context: CallbackContext, city_name):
    lat, lon = get_city_coordinates(city_name)
    if not lat or not lon:
        update.message.reply_text("Не удалось найти координаты города.", reply_markup=start_keyboard(context.user_data.get('lang', 'en')))
        return STATE_LOCATION

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        weather = data.get("current_weather", {})

        temperature = weather.get("temperature")
        windspeed = weather.get("windspeed")
        weather_code = weather.get("weathercode")

        lang = context.user_data.get("lang", "en")
        weather_desc = get_weather_description_localized(weather_code, lang)

        text = f"""Погода в городе {city_name}:
        🌡 Температура: {temperature}°C
        💨 Ветер: {windspeed} км/ч
☁       {weather_desc}"""


        update.message.reply_text(text, reply_markup=start_keyboard(context.user_data.get('lang', 'en')))
    except Exception as e:
        print(f"[❌ Ошибка Open-Meteo]: {e}")
        update.message.reply_text("Не удалось получить данные о погоде.", reply_markup=start_keyboard(context.user_data.get('lang', 'en')))

    return STATE_LOCATION

def handle_city(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    city_name = update.message.text.strip()
    if city_name == translations[lang]["back"]:
        return start(update, context)
    lat, lon = get_city_coordinates(city_name)
    if not lat or not lon:
        msg = translations[lang].get("city_not_found", "City not found. Try again.")
        update.message.reply_text(msg,
                                  reply_markup=ReplyKeyboardMarkup([[KeyboardButton(translations[lang]["back"])]], resize_keyboard=True))
        return STATE_CITY
    purpose = context.user_data.get("purpose")
    if purpose == "weather":
        return send_weather(update, context, city_name)
    return STATE_LOCATION
    return STATE_LOCATION

def select_excursion_category(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    keyboard = [
        [KeyboardButton(translations[lang]["excursion_museums"]), KeyboardButton(translations[lang]["excursion_galleries"])],
        [KeyboardButton(translations[lang]["excursion_parks"]), KeyboardButton(translations[lang]["excursion_historic"])],
        [KeyboardButton(translations[lang]["back"])]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(translations[lang]["select_excursion_category"], reply_markup=reply_markup)
    return STATE_SELECT_EXCURSION_CATEGORY

def filtered_excursions(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    user_id = update.message.from_user.id
    coords = user_locations.get(user_id)
    if not coords:
        msg = translations[lang].get("send_location_first", "Please send your location first.")
        update.message.reply_text(msg, reply_markup=start_keyboard(lang))
        return STATE_LOCATION
    user_lat, user_lon = coords
    text = update.message.text
    categories = {
        translations[lang]["excursion_museums"]: 'node["tourism"="museum"]',
        translations[lang]["excursion_galleries"]: 'node["tourism"="gallery"]',
        translations[lang]["excursion_parks"]: 'node["tourism"="theme_park"]; node["tourism"="attraction"]; node["tourism"="zoo"]',
        translations[lang]["excursion_historic"]: 'node["historic"]'
    }
    if text == translations[lang]["back"]:
        return start(update, context)
    if text not in categories:
        msg = translations[lang].get("choose_category_error", "Please choose a category from the menu.")
        update.message.reply_text(msg)
        return STATE_SELECT_EXCURSION_CATEGORY
    overpass_query = f"""
    [out:json][timeout:25];
    (
      {categories[text]}(around:7000,{user_lat},{user_lon});
    );
    out body 15;
    """
    try:
        response = requests.post("https://overpass-api.de/api/interpreter", data={"data": overpass_query})
        response.raise_for_status()
        data = response.json().get("elements", [])
        if not data:
            msg = translations[lang].get("no_excursions_found", "No places found in this category.")
            update.message.reply_text(msg, reply_markup=start_keyboard(lang))
            return STATE_LOCATION
        result_text = f"📍 {translations[lang].get('places_in_category', 'Places in category')} «{text}»:\n"
        buttons = []
        for elem in data[:5]:
            name = elem.get("tags", {}).get("name", "No name")
            lat = elem.get("lat")
            lon = elem.get("lon")
            wiki = get_wikipedia_description(name)
            route_url = f"https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route={user_lat},{user_lon};{lat},{lon}"
            result_text += f"• {name}\n"
            if wiki:
                result_text += f"  📝 {wiki}\n"
            result_text += f"  🚗 [Route]({route_url})\n\n"
            buttons.append([InlineKeyboardButton(f"{translations[lang].get('to_route', 'To')} {name}", url=route_url)])
        update.message.reply_text(result_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        print(f"[❌ Excursion filter error]: {e}")
        msg = translations[lang].get("excursion_error", "An error occurred while searching excursions.")
        update.message.reply_text(msg, reply_markup=start_keyboard(lang))
    return STATE_LOCATION

def get_city_coordinates(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
        "accept-language": "ru"
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None, None
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    except Exception as e:
        print(f"[❌ Nominatim error]: {e}")
        return None, None

def find_hotels(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    user_id = update.message.from_user.id
    coords = user_locations.get(user_id)
    if not coords:
        update.message.reply_text("Please send your location first.", reply_markup=start_keyboard(lang))
        return STATE_LOCATION
    lat, lon = coords
    url = f"https://eu1.locationiq.com/v1/nearby.php?key={LOCATIONIQ_TOKEN}&lat={lat}&lon={lon}&tag=hotel&radius=5000&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        hotels = response.json()
        if not hotels:
            update.message.reply_text("No hotels found nearby.", reply_markup=start_keyboard(lang))
            return STATE_LOCATION
        buttons = []
        result_text = "🏨 Found hotels:\n"
        for hotel in hotels[:5]:
            name = hotel.get("name", "Unnamed")
            lat_h = hotel.get("lat")
            lon_h = hotel.get("lon")
            phone = hotel.get("tags", {}).get("phone") or hotel.get("tags", {}).get("contact:phone") or "No phone"
            route_url = f"https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route={lat},{lon};{lat_h},{lon_h}"
            result_text += f"• {name}\n  Phone: {phone}\n  [Route]({route_url})\n\n"
            buttons.append([InlineKeyboardButton(text=f"Route to {name}", url=route_url)])
        update.message.reply_text(result_text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode='Markdown')
    except Exception as e:
        print(f"[❌ LocationIQ error]: {e}")
        update.message.reply_text("Error searching for hotels.", reply_markup=start_keyboard(lang))
    return STATE_LOCATION

def get_wikipedia_description(title):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            extract = data.get("extract")
            if extract:
                return extract[:200] + "..." if len(extract) > 200 else extract
        return None
    except Exception as e:
        print(f"[❌ Wikipedia error]: {e}")
        return None

def find_attractions(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    coords = user_locations.get(user_id)
    if not coords:
        update.message.reply_text("Please send your location first.", reply_markup=start_keyboard(lang))
        return STATE_LOCATION
    user_lat, user_lon = coords
    radius = 5000  # 5 km
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:25];
    (
      node["tourism"="attraction"](around:{radius},{user_lat},{user_lon});
      node["historic"](around:{radius},{user_lat},{user_lon});
      node["amenity"="place_of_worship"](around:{radius},{user_lat},{user_lon});
    );
    out body 15;
    """
    try:
        response = requests.post(overpass_url, data={"data": query})
        response.raise_for_status()
        data = response.json().get("elements", [])
        if not data:
            update.message.reply_text("No attractions found nearby.", reply_markup=start_keyboard(lang))
            return STATE_LOCATION
        result_text = "🗺 Attractions nearby:\n"
        buttons = []
        for elem in data[:5]:
            name = elem.get("tags", {}).get("name", "Unnamed")
            lat_a = elem.get("lat")
            lon_a = elem.get("lon")
            route_url = f"https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route={user_lat},{user_lon};{lat_a},{lon_a}"
            result_text += f"• {name}\n  🚗 [Route]({route_url})\n\n"
            buttons.append([InlineKeyboardButton(text=f"Route to {name}", url=route_url)])
        update.message.reply_text(result_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        print(f"[❌ Overpass error (attractions)]: {e}")
        update.message.reply_text("Error searching for attractions.", reply_markup=start_keyboard(lang))
    return STATE_LOCATION

def find_transport(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    user_id = update.message.from_user.id
    coords = user_locations.get(user_id)
    if not coords:
        update.message.reply_text("Please send your location first.", reply_markup=start_keyboard(lang))
        return STATE_LOCATION
    user_lat, user_lon = coords
    radius = 500  # 500 meters
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:25];
    (
      node["highway"="bus_stop"](around:{radius},{user_lat},{user_lon});
      node["railway"="station"](around:{radius},{user_lat},{user_lon});
      node["public_transport"="platform"](around:{radius},{user_lat},{user_lon});
      node["railway"="tram_stop"](around:{radius},{user_lat},{user_lon});
      node["railway"="subway_entrance"](around:{radius},{user_lat},{user_lon});
    );
    out body;
    """
    try:
        response = requests.post(overpass_url, data={"data": query})
        response.raise_for_status()
        data = response.json().get("elements", [])
        if not data:
            update.message.reply_text("No transport stops found nearby.", reply_markup=start_keyboard(lang))
            return STATE_LOCATION
        result_text = "🚍 Nearby stops:\n"
        for elem in data[:5]:
            name = elem.get("tags", {}).get("name", "Unnamed")
            stop_type = elem.get("tags", {}).get("public_transport") or elem.get("tags", {}).get("highway") or elem.get("tags", {}).get("railway")
            stop_lat = elem.get("lat")
            stop_lon = elem.get("lon")
            route_url = f"https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route={user_lat},{user_lon};{stop_lat},{stop_lon}"
            result_text += f"• {name} ({stop_type})\n  🚗 [Route to stop]({route_url})\n\n"
        update.message.reply_text(result_text, parse_mode='Markdown', reply_markup=start_keyboard(lang))
    except Exception as e:
        print(f"[❌ Overpass error (transport)]: {e}")
        update.message.reply_text("Error searching for transport.", reply_markup=start_keyboard(lang))
    return STATE_LOCATION

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float | None:
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency.upper()}&to={to_currency.upper()}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        result = data["rates"].get(to_currency.upper())
        if result is None:
            print(f"[❌ Ошибка конвертации валют]: Не удалось получить курс для {to_currency}")
            return None
        return result
    except requests.RequestException as e:
        print(f"[❌ Ошибка запроса конвертации]: {e}")
        return None


def handle_currency_conversion(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    text = update.message.text.strip()
    if text == translations[lang]["back"]:
        return start(update, context)
    import re
    match = re.match(r"([\d\.,]+)\s*([A-Z]{3})\s+в\s+([A-Z]{3})", text, re.IGNORECASE)
    if not match:
        currency_buttons = [
            [KeyboardButton("100 USD в EUR"), KeyboardButton("100 EUR в USD")],
            [KeyboardButton("100 USD в RUB"), KeyboardButton("100 RUB в USD")],
            [KeyboardButton("100 EUR в RUB"), KeyboardButton("100 RUB в EUR")],
            [KeyboardButton("100 BGN в USD"), KeyboardButton("100 USD в BGN")],
            [KeyboardButton("100 GBP в JPY"), KeyboardButton("100 JPY в GBP")],
            [KeyboardButton(translations[lang]["back"])]
        ]
        update.message.reply_text(translations[lang]["enter_amount_and_currencies"], parse_mode='Markdown',
                                  reply_markup=ReplyKeyboardMarkup(currency_buttons, resize_keyboard=True))
        return STATE_CONVERT
    amount, from_currency, to_currency = match.groups()
    amount = amount.replace(',', '.')
    try:
        amount = float(amount)
    except ValueError:
        update.message.reply_text(translations[lang]["amount_not_recognized"])
        return STATE_CONVERT
    supported_currencies = {"USD", "EUR", "RUB", "BGN", "GBP", "JPY", "CHF", "AUD", "CAD", "CNY"}
    if from_currency.upper() not in supported_currencies or to_currency.upper() not in supported_currencies:
        update.message.reply_text(translations[lang]["currency_not_supported"].format(', '.join(sorted(supported_currencies))))
        return STATE_CONVERT
    result = convert_currency(amount, from_currency, to_currency)
    if result is None:
        update.message.reply_text(translations[lang]["conversion_failed"], reply_markup=start_keyboard(lang))
        return STATE_CONVERT
    update.message.reply_text(f"💱 {amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}",
                              reply_markup=start_keyboard(lang))
    return STATE_LOCATION

def start_translate(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    buttons = [[KeyboardButton(name)] for code, name in LANGUAGES.items()]
    buttons.append([KeyboardButton(translations[lang]["cancel"])])
    update.message.reply_text(translations[lang]["select_source_language"], reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return STATE_TRANSLATE_FROM

def translate_from(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    text = update.message.text
    if text.lower() == translations[lang]["cancel"].lower():
        update.message.reply_text(translations[lang]["translation_cancelled"], reply_markup=start_keyboard(lang))
        return STATE_LOCATION
    lang_code = None
    for code, name in LANGUAGES.items():
        if name.lower() == text.lower():
            lang_code = code
            break
    if not lang_code:
        update.message.reply_text(translations[lang]["choose_language_list"])
        return STATE_TRANSLATE_FROM
    context.user_data["translate_from"] = lang_code
    update.message.reply_text(translations[lang]["enter_text_to_translate"],
                              reply_markup=ReplyKeyboardMarkup([[KeyboardButton(translations[lang]["cancel"])]], resize_keyboard=True))
    return STATE_TRANSLATE_INPUT

def translate_input(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    text = update.message.text
    if text.lower() == translations[lang]["cancel"].lower():
        update.message.reply_text(translations[lang]["translation_cancelled"], reply_markup=start_keyboard(lang))
        return STATE_LOCATION
    context.user_data["translate_text"] = text
    buttons = [[KeyboardButton(name)] for code, name in LANGUAGES.items()]
    buttons.append([KeyboardButton(translations[lang]["cancel"])])
    update.message.reply_text(translations[lang]["select_target_language"], reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return STATE_TRANSLATE_TO

def translate_to(update: Update, context: CallbackContext):
    lang = context.user_data.get("lang", "en")
    text = update.message.text
    if text.lower() == translations[lang]["cancel"].lower():
        update.message.reply_text(translations[lang]["translation_cancelled"], reply_markup=start_keyboard(lang))
        return STATE_LOCATION
    lang_code = None
    for code, name in LANGUAGES.items():
        if name.lower() == text.lower():
            lang_code = code
            break
    if not lang_code:
        update.message.reply_text(translations[lang]["choose_language_list"])
        return STATE_TRANSLATE_TO
    context.user_data["translate_to"] = lang_code
    text_to_translate = context.user_data.get("translate_text")
    from_lang = context.user_data.get("translate_from")
    to_lang = context.user_data.get("translate_to")
    if not text_to_translate or not from_lang or not to_lang:
        msg = translations[lang].get("error_retry", "An error occurred. Please try again.")
        update.message.reply_text(msg, reply_markup=start_keyboard(lang))
        return STATE_LOCATION

    translated_text = libretranslate_translate(text_to_translate, from_lang, to_lang)
    if translated_text:
        update.message.reply_text(f"{translations[lang]['translation_result_prefix']}\n{translated_text}", reply_markup=start_keyboard(lang))
    else:
        update.message.reply_text(translations[lang]["translation_failed"], reply_markup=start_keyboard(lang))
    return STATE_LOCATION
def libretranslate_translate(text, source_lang, target_lang):
    try:
        url = "https://lt.vern.cc/translate"
        payload = {
            "q": text,
            "source": source_lang,
            "target": target_lang,
            "format": "text"
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("translatedText")
    except Exception as e:
        print(f"[❌ LibreTranslate error]: {e}")
        return None


def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", language_selection)],
        states={
            STATE_LANGUAGE_SELECT: [MessageHandler(Filters.text, set_language)],
            STATE_LOCATION: [MessageHandler(Filters.location | Filters.text, location_handler)],
            STATE_SELECT_EXCURSION_CATEGORY: [MessageHandler(Filters.text & ~Filters.command, filtered_excursions)],
            STATE_CITY: [MessageHandler(Filters.text, handle_city)],
            STATE_CONVERT: [MessageHandler(Filters.text, handle_currency_conversion)],
            STATE_TRANSLATE: [MessageHandler(Filters.text & ~Filters.command, start_translate)],
            STATE_TRANSLATE_FROM: [MessageHandler(Filters.text & ~Filters.command, translate_from)],
            STATE_TRANSLATE_INPUT: [MessageHandler(Filters.text & ~Filters.command, translate_input)],
            STATE_TRANSLATE_TO: [MessageHandler(Filters.text & ~Filters.command, translate_to)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



def convert_currency(amount, from_currency, to_currency):
    try:
        url = f"https://api.exchangerate.host/convert"
        params = {"from": from_currency, "to": to_currency, "amount": amount}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("result")
    except Exception as e:
        print(f"[❌ Currency conversion error]: {e}")
        return None

OPENWEATHER_TOKEN = "your_openweather_api_token"  # Замените на ваш настоящий токен

def get_weather(city_name):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city_name,
            "appid": OPENWEATHER_TOKEN,
            "units": "metric",
            "lang": "ru"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        return f"""🌤 Погода в {city_name}:
Описание: {desc}
Температура: {temp}°C
Влажность: {humidity}%
Ветер: {wind} м/с"""
    except Exception as e:
        print(f"[❌ Weather error]: {e}")
        return "Ошибка при получении погоды."



def get_weather_description(code):
    weather_codes = {
        0: "Ясно",
        1: "Преимущественно ясно",
        2: "Переменная облачность",
        3: "Пасмурно",
        45: "Туман",
        48: "Инейный туман",
        51: "Лёгкая морось",
        53: "Умеренная морось",
        55: "Сильная морось",
        61: "Лёгкий дождь",
        63: "Умеренный дождь",
        65: "Сильный дождь",
        71: "Лёгкий снег",
        73: "Умеренный снег",
        75: "Сильный снег",
        80: "Лёгкий ливень",
        81: "Умеренный ливень",
        82: "Сильный ливень",
    }
    return weather_codes.get(code, "Неизвестная погода")
