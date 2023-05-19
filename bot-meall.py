
import telebot,requests,redis
from telebot import types

bot = telebot.TeleBot("6167116890:AAGCn5c95UQfKDc00912LCkSZlPDVcas28Q")

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == "private":
        key = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="- الحصول على ايميل .", callback_data="getEmail")
        btn2 = types.InlineKeyboardButton(text="- حالة السيرفرات .", callback_data="check")
        btn3 = types.InlineKeyboardButton(text="- المطور الاساسي .", url="https://t.me/LLLEA")
        btn4 = types.InlineKeyboardButton(text="- المطور الثانوي .", url="https://t.me/xxxxJ")
        key.row_width = 2
        key.add(btn1, btn2)
        key.add(btn3)
        key.add(btn4)
        bot.reply_to(message, "اهلا بك في بوت الايميلات الوهمية\n- اليك التحكم من الازرار ادناه .", reply_markup=key)
    else:
        bot.reply_to(message,"البوت لايعمل في مجموعات .")
        bot.leave_chat(message.chat.id)
@bot.callback_query_handler(func=lambda call: True)
def qwere(call):
    global myMail,user,domain
    if call.data == "getEmail":
        key2 = types.InlineKeyboardMarkup()
        rr = types.InlineKeyboardButton(text="- تحديث .",callback_data="refresh")
        key2.row_width = 1
        key2.add(rr)
        myMail = requests.get(f"https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
        bot.send_message(call.message.chat.id,f"- الايميل الخاص بك : {myMail}")
        bot.send_message(call.message.chat.id,f"- لم يتم العثور على رسائل .",reply_markup=key2)
    if call.data == "home":
        start(call.message)
    if call.data == "refresh":
        strd = f"{myMail}"
        domain = strd.split("@")[1]
        user = strd.split("@")[0]
        getMessages = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}")
        if "[]" in getMessages.text:
            key2 = types.InlineKeyboardMarkup()
            rr = types.InlineKeyboardButton(text="- تحديث .", callback_data="refresh")
            key2.row_width = 1
            key2.add(rr)
            bot.edit_message_text(chat_id=call.message.chat.id,text=f"- لم يتم العثور على رسائل!",message_id=call.message.id,reply_markup=key2)
        else:
            key3 = types.InlineKeyboardMarkup()
            btn5 = types.InlineKeyboardButton(text=f"- الصفحة الرئيسية .",callback_data="home")
            key3.row_width = 1
            key3.add(btn5)
            gett = getMessages.json()[0]
            subject = gett["subject"]
            date = gett['date']
            id = gett['id']
            fr = gett['from']
            getmessage = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={domain}&id={id}").json()['textBody']
            bot.edit_message_text(chat_id=call.message.chat.id,text=f"رسالة جديده!\n- المرسل : {fr}\n- العنوان : {subject}\n- الوقت : {date}\n- الرسالة : \n\n{getmessage}",message_id=call.message.id,reply_markup=key3)
bot.infinity_polling()
