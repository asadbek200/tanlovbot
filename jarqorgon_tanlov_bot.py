from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# Tanlov (Direktorlar) ro'yxati
directors = [
    "Xaydarqulova Dilbar Fayzullayevna",
    "Yarmatova Dilbar Ravshanovna",
    "Normurodova Ra’noXushboqovna",
    "Allaberdiyev Umid Vali o‘g‘li",
    "Qulboyev Ro‘zimurod Ashurovich",
    "Nazarova Muxabbat Utanovna ",
    "Soatov Nurbek Baxodir o‘g‘li",
    "Kucharov Zafar",
    "Xalikov Shokir Adilovichb",
    "Mirzayeva Dilrabo Yuldoshevna",
    "Shaynayeva Zulfiya Qurbonovna",
    "Mamadiyev Majid Qulto‘rayevich",
    "Musurmonkulov Nuriddin Qudrat o'g'li",
    "Parmonov Abdulakim Ravshanovich",
    "Ko‘kiyev Otabek Raxmonqulovich",
    "Mirzayev O‘ktam Xolmuminovich",
    "Usanov Odil Xayitovich",
    "Aliqulov Alisher Amonqul o'g'li",
    "Choriyeva Zarifa Eshqobilovna",
    "Xazratkulov Jumag'ul Eshiddin o'g'li",
    "Nodirov Ziyodulla Xolmamatovich",
    "Qosimov Ilxom Fayzullayevich",
    "Muqimov Ortiq Ergashevich",
    "Turayeva Feruza Mamadaliyevna",
    "Tojiyeva Shoxista Allamovna",
    "Qurbonov To'yli Tursunovich",
    "Do‘sanov Qurbon Mamarasulovich",
    "Choriyeva Umida Po‘latovna",
    "Burxonov Abramat Karamatovich",
    "Abdiyev Yo'lbars Buranovich",
    "Jo‘rayeva Nasiba Mamaradjabovna",
    "Tangirov Abduraxmon Toshtemirovich",
    "Uzoqova Oysara Usanovna",
    "Normurodov Dilshod Davlatovich",
    "Sharipov Allanazar Kavagovich",
    "Eshmuratova Sevara Ruzimuratovna",
    "Eshmurodov Komil Xudoyberdiyevich",
    "Qizilov Oltiboy Valiyevich",
    "Maxmudov Qalandar Mamayusupovich",
    "Egamurodov Eshpo‘lat Xaitmurotovich",
    "Xolmatov Shavkat Boyqobilovich",
    "Gaimov Baxrom Kuchkeldiyevich",
    "Ibroximov Bahriddin Abdijabbor o‘g‘li",
    "Mansurov Urol Mamatovich",
    "Qodirova Nilufar Maxamovna",
    "Javqashova Zuxra Abduxakimovna",
    "Xujamberdiyeva Sarvinoz Yomgirovna",
    "Abdumo‘minov Ilhom Husanovich",
    "Xujamqulov Mashxur Ishqobilovich",
    "Shomurodov Jo'rabek Eshpo'lat o'g'li",
    "Qurbonov Muxammadi Abdimurodovich",
    "Xudayarova Barno Djavliyevna",
    "Raximov O‘tkir Nurqobilovich",
    "Alixonov Abduxoliq Ziyotovich",
    "Mansurov Ahmed Choriyevich",
    "Xudjamqulov Odilbek Xushbaqovich",
    "Qurbonmuratov Xonnazar Abdinazarovich",
    "Usanov Erkin Shopulatovich",
    "Normurodov Abdushukur Xusanovich",
    "Xudoyberdiyeva Zulfiya Xidirovna",
    "Qurbonov Panji Xasanovich",
    "Batashov Jumanazar Bozorovich",
    "Haydarov Panji Rahmonovich",
    "Yodgorov Ibodulla Yakub o‘g‘li",
    "Egamov Sirojiddin Rasulovich",
    "Yo‘ldoshov Yangiboy ",
    "Xayitov Orif Davronovich",
    "Shaymardonov Sherzod Norbekovich",
]

# Foydalanuvchilarning ovozlarini saqlash
user_votes = {}

# Loggerni o'rnatish
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Ovozlar sonini hisoblash funksiyasi
def get_vote_counts():
    director_votes = {director: 0 for director in directors}

    # Har bir direktor uchun ovozlarni hisoblash
    for vote in user_votes.values():
        if vote in director_votes:
            director_votes[vote] += 1

    return director_votes

# /start komandasi
async def start(update: Update, context: CallbackContext) -> None:
    director_votes = get_vote_counts()
    keyboard = [
        [InlineKeyboardButton(f"{director} ({director_votes[director]} ovoz)", callback_data=director)]
        for director in directors
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Tanlovga xush kelibsiz! Iltimos, direktorlar ro\'yxatidan bitta direktor uchun ovoz bering:',
        reply_markup=reply_markup
    )

# Foydalanuvchi ovoz berganda
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Botga javobni tasdiqlash

    user_id = query.from_user.id

    if user_id in user_votes:
        await query.edit_message_text(text="Siz allaqachon ovoz bergansiz!")
    else:
        user_votes[user_id] = query.data
        await query.edit_message_text(text=f"Siz {query.data} direktoriga ovoz berdingiz!")

# Natijalarni ko'rsatish
async def results(update: Update, context: CallbackContext) -> None:
    results_text = "Tanlov natijalari:\n"
    director_votes = get_vote_counts()

    # Natijalarni ko'rsatish
    for director, count in director_votes.items():
        results_text += f"{director}: {count} ovoz\n"

    await update.message.reply_text(results_text)

# Asosiy funksiya
def main():
    # Botni ishga tushirish uchun API tokenini o'zgartiring
    application = Application.builder().token("7248739293:AAH35wET4EZPCyNcJdRxQ3MbO6kJu5LvaP4").build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("results", results))

    # Botni ishga tushirish
    application.run_polling()

if __name__ == '__main__':
    main()
