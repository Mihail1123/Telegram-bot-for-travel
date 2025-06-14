Важно: Следните инструкции са предназначени за операционна система Windows. Изпълнявайте стъпките последователно, за да стартирате проекта успешно.
Необходим софтуер
Python: Проектът изисква Python версия 3.10 или по-нова (препоръчително 3.10–3.12). Строго не се препоръчва използване на Python 2.x или версии под 3.9, тъй като някои използвани библиотеки може да не работят коректно.
Text Editor (по избор): Notepad++, Visual Studio Code, Sublime Text и др.
Стъпки за стартиране:
      1. Инсталиране на Python
1.1. Изтеглете инсталатора от: https://www.python.org/downloads/windows/
1.2. Стартирайте инсталацията и задължително включете опцията: Add Python to PATH
1.3. След инсталация, проверете версията чрез: python --version (примерен резултат: Python 3.11.6)
2. Подготовка на папка с проекта
2.1. Създайте папка, например: C:\TelegramBot
2.2. Поставете в нея всички проектни файлове: main.py, подпапки (handlers, services, utils, keyboards, states), както и requirements.txt и .env.
3. Създаване на виртуална среда
3.1. Отворете Command Prompt (cmd)
3.2. Навигирайте до папката с проекта: cd C:\TelegramBot
3.3. Създайте виртуална среда: python -m venv venv
3.4. Активирайте я: venv\Scripts\activate
3.5. Ако всичко е наред, ще се появи: (venv) C:\TelegramBot>
4. Инсталиране на зависимости
4.1. Убедете се, че файлът requirements.txt е в папката
4.2. Изпълнете: pip install -r requirements.txt
4.3. Това ще инсталира всички необходими библиотеки: aiogram, requests, python-dotenv, aiohttp и др.
5. Създаване и конфигурация на .env файл
5.1. В основната папка създайте файл .env
5.2. Въведете следните данни:

BOT_TOKEN=тук_въведете_токена_от_BotFather
RAPIDAPI_KEY=вашият_RapidAPI_ключ
WEATHER_API_KEY=ключ_за_погода
TRANSLATE_API_URL=https://libretranslate.com/translate
TRANSLATE_API_LANGUAGES=https://libretranslate.com/languages

5.3. Запазете файла с UTF-8 кодировка
6. Стартиране на бота
6.1. Уверете се, че сте в папката и виртуалната среда е активна
6.2. Изпълнете: python main.py
6.3. При правилна настройка ще получите съобщение, че ботът е стартирал и чака            съобщения от потребители.
7. Проверка в Telegram
7.1. Отворете приложението Telegram
7.2. Потърсете вашия бот по потребителско име
7.3. Натиснете Start или въведете /start
8. Допълнително
8.1. За изключване на бота натиснете Ctrl + C
8.2. За напускане на виртуалната среда въведете: deactivate
8.3. По желание създайте стартиращ .bat файл със съдържание:

@echo off
cd /d C:\TelegramBot

Съдържание на примерен .bat файл:
@echo off
cd /d C:\TelegramBot
call venv\Scripts\activate
python main.py
pause
![image](https://github.com/user-attachments/assets/7ff1c3f3-adb3-4456-a33d-e2409607e707)
