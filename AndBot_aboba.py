from aiogram import Bot, Dispatcher , executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from openpyxl import Workbook, load_workbook
from openpyxl.styles.numbers import BUILTIN_FORMATS
from datetime import date
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMusage(StatesGroup):
    age = State()
    city = State()
    change = State()
    books = State()
    rating = State()
    crossroad = State()
    done = State()
    done_fr = State()
    first_time = State()
    
rate_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]    

b_yes = KeyboardButton("Да")
b_no = KeyboardButton("Нет")
b_skip = KeyboardButton("/skip")

### prompts
global hello_message
hello_message = "Привет! Я бот для подбора книг. Для использования функционала воспользуйся командой - /menu"
global menu_main
menu_main = "Вы в главном меню"
search_book = "Искать книги"
book_not_found = "Такой книги нет в нашей базе данных"



### For menu
b_list_text = "Книги на прочтении"
b_list = KeyboardButton(b_list_text)
b_change_text = "Смена данных"
b_change = KeyboardButton(b_change_text)
b_done_text = "Прочитанные книги"
b_done = KeyboardButton(b_done_text)
b_books = KeyboardButton(search_book)
b_add_done_text = "Оценить прочитанную книгу"
b_add_done = KeyboardButton(b_add_done_text)

global keyboard
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row(b_yes, b_no)

global keyboard_menu
keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_menu.add(b_books).add(b_list).add(b_done).add(b_add_done)

global keyboard_skip
keyboard_skip = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_skip.add(b_skip)

storage = MemoryStorage()
conn2 = sqlite3.connect("C:\prog_questionmark\AndBot\ANDlogs.db")
cursor_logs = conn2.cursor()
conn = sqlite3.connect("C:\prog_questionmark\AndBot\ANDbooks.db")
cursor = conn.cursor()
TOKEN = "6079464798:AAGPhgVx8qiu6Do4Mrbeptg3cG8L_W2idEg"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
wb = load_workbook("C:/prog_questionmark/AndBot/database.xlsx")
ws = wb.active
#async def reply(message : types.message, tg_reply):
    #await bot.send_message(message.from_user.id, tg_reply)
async def reply(tg_reply):
    await bot.send_message(Global_message.from_user.id, f"{tg_reply}")




@dp.message_handler(commands=["start", "help"], state=None)
async def start(message : types.Message):
    global Global_message
    Global_message = message
    if message.text in ["/start", "/help"]:
        await reply(hello_message)
        await FSMusage.first_time.set()

@dp.message_handler(state=FSMusage.first_time)
async def first_time(message : types.Message):
    global Global_message
    Global_message = message    
    if message.text == "/menu":
        await bot.send_message(message.from_user.id,menu_main, reply_markup=keyboard_menu)
        await FSMusage.crossroad.set()
    else:
        await reply(hello_message)
    
# @dp.message_handler(state=FSMusage.age)
# async def age(message : types.Message):
#     global Global_message
#     Global_message = message
#     global age
#     try:
#         age = int(message.text)
#         print(age)
#         if age > 99 or age < 10:
#             await reply("Доступ запрещён!")
#         else:
#             await FSMusage.city.set()
#             await reply("В какой стране ты живёшь?")
#     except:
#         await reply("Введи целое число")


# @dp.message_handler(state=FSMusage.city)
# async def city(message : types.Message, state: FSMContext):
#     global Global_message
#     Global_message = message
#     city = message.text
#     cursor_logs.execute("INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `age`, `city`) VALUES (?, ?, ?, ?, ?)", (message.chat.id, message.chat.first_name, message.chat.last_name, age, city))
#     conn2.commit()
#     await FSMusage.crossroad.set()
#     await reply("Введи книгу ")
#     #await state.finish()


# @dp.message_handler(commands=["books"], state=None)
# async def books(message : types.Message):
#     global Global_message
#     Global_message = message
#     await FSMusage.books.set()
#     await reply("Введи книгу ")

# @dp.message_handler(state=FSMusage.change)
# async def change(message : types.Message, state: FSMContext):
#     global Global_message
#     Global_message = message
#     #await reply("Изменить данные?")
#     #keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
#     #keyboard.row(b_yes, b_no)
#     #await bot.send_message(message.from_user.id, "Изменить данные?", reply_markup=keyboard)
#     if message.text == "Да" or message.text == b_change_text:
#         cursor_logs.execute(f"DELETE FROM users WHERE user_id={message.chat.id}")
#         #conn.commit()
#         await FSMusage.age.set()
#         await reply("Возраст?")
#     elif message.text == "Нет":
#         await bot.send_message(message.from_user.id, "Главное меню", reply_markup=keyboard_menu)
#         await FSMusage.crossroad.set()

@dp.message_handler(state=FSMusage.books)
async def books(message : types.Message):
    global Global_message
    Global_message = message

    telegram_id = message.chat.id
    #

    #user_book = input("Книга ")

    #
    # try:
    #     #conn.execute(f"CREATE TABLE user_{telegram_id} (Book , reviewers)")
    #     conn.execute(f"CREATE TABLE user_{telegram_id} (Title UNIQUE, status DEFAULT not_rated)")
    # except:
        # None
        # print("cringe")
    user_book = f'{message.text}'
    if "'" in user_book:
        cursor.execute(f"""SELECT * FROM main WHERE Title="{user_book}" """)
    elif '"' in user_book:
        cursor.execute(f"""SELECT * FROM main WHERE Title='{user_book}'""")
    elif "'" in user_book and '"' in user_book:
        print("pizda")
    elif "'" not in user_book and '"' not in user_book:
        cursor.execute(f"""SELECT * FROM main WHERE Title='{user_book}'""")
    row = cursor.fetchall()
    if bool(row) == False:
        await reply(book_not_found)
    else:
        book_ISBN = []  
        for i, value in enumerate(row):
            book_ISBN.append(value[0])
        book_ISBN = tuple(book_ISBN)
        #print(book_ISBN)
        #print(book_ISBN[0])
        if len(book_ISBN) == 1:
            cursor.execute(f"""SELECT * FROM rews WHERE ISBN='{book_ISBN[0]}' AND rating IN ('7', '8', '9', '10');""")
        else:
            cursor.execute(f"SELECT * FROM rews WHERE ISBN IN {book_ISBN} AND rating IN ('7', '8', '9', '10');")
        user_book_rating = cursor.fetchall()
        #print(user_book_rating)
        user_book_rating_avg = None
        user_book_rating_sum = 0
        reviwers = []
        for i, value in enumerate(user_book_rating):
            try:
                mark = int(value[2])
                user_book_rating_sum += mark
                reviwers.append(value[0])
            except:
                None
        reviwers = tuple(reviwers)

        cursor.execute(f"SELECT * FROM rews WHERE user_id IN {reviwers} AND rating IN ('7', '8', '9', '10');")
        all_rews = cursor.fetchall()

        error =0
        unique_ISBN = []
        for i, value in enumerate(all_rews):
            if value[1] not in unique_ISBN and value[1]:# not in book_ISBN:
                unique_ISBN.append(value[1])
        unique_ISBN = tuple(unique_ISBN)
        crude_sum = []
        dups_ISBN = []
        dups_rates = []
        rate_sum = []
        rate_sum_divide = []
        temp_list = []
        first_pos_list = []
        temp = 0
        res = None

        for value in unique_ISBN:
            crude_sum.append(1)

        ###



        ###

        for i, value in enumerate(all_rews):
            try:
                first_pos = unique_ISBN.index(value[1])#+1
            except:
                error +=1
            first_pos_list.append(first_pos)
            temp = int(all_rews[i][2])
            temp_list.append(temp)
            try:
                crude_sum[first_pos] += temp
            except:
                error +=1
        crude_sum[0] = 1
        max_list = []
        for i in range(20):
            max_1 = max(crude_sum)
            isbn_max = crude_sum.index(max_1)
            max_list.append(unique_ISBN[isbn_max])
            crude_sum[isbn_max] = 0

        recc_list = []
        for i in max_list:
            v = unique_ISBN.index(i)
            recc_list.append(unique_ISBN[v])
        recc_list = tuple(recc_list)


        if "'" in user_book:
            cursor.execute(f"""SELECT ISBN, Title, Author, main."Image-3" FROM main WHERE ISBN IN {recc_list} AND Title != "{user_book}";""")
        elif '"' in user_book:
            cursor.execute(f"SELECT ISBN, Title, Author, main.'Image-3' FROM main WHERE ISBN IN {recc_list} AND Title != '{user_book}';")
        elif "'" in user_book and '"' in user_book:
            print("pizda")
        elif "'" not in user_book and '"' not in user_book:
            cursor.execute(f"SELECT ISBN, Title, Author, main.'Image-3' FROM main WHERE ISBN IN {recc_list} AND Title != '{user_book}';")

        #cursor.execute(f"SELECT Title FROM main WHERE ISBN IN {recc_list} AND Title != '{user_book}';")  ###
        global recs
        recs = cursor.fetchall()
        for i, value in enumerate(recs):
            str_reply = str(value[1])
            str_author = str(value[2])
            await reply(f"{i+1}. {str_reply}\nАвтор - {str_author}")
            try:
                await bot.send_photo(message.chat.id, photo=f"{value[3]}")
            except:
                await reply(value[3])
        await bot.send_message(message.from_user.id, f"Какие произведения будешь читать дальше?\nВведи номера через запятую (7, 3, 1).\nЕсли таковых нет, отправь /skip", reply_markup = keyboard_skip)
        await FSMusage.rating.set()


@dp.message_handler(state=FSMusage.rating)
async def rating(message : types.Message, state: FSMContext):
    global Global_message
    Global_message = message
    if message.text == "/skip":
        await bot.send_message(message.from_user.id,menu_main, reply_markup=keyboard_menu)
        await FSMusage.crossroad.set()

    else:
        try:
            recs_list = message.text.split(", ")
            choosen_books = []
            choosen_isbn = []
            for value in recs_list:
                value = int(value)
                value -= 1
                if recs[value][1] not in choosen_books:
                    choosen_books.append(recs[value][1])
                    choosen_isbn.append(recs[value][0])
            books_reply = ""
            
            temp = None
            for i,value in enumerate(choosen_isbn):
                cursor.execute(f"SELECT * FROM `rews` WHERE user_id= {message.chat.id} AND ISBN = '{value}'")
                temp = cursor.fetchone()
                print(temp)
                print(bool(temp))
                try:
                    if bool(temp) == False:
                        cursor.execute(f"INSERT INTO `rews` (`user_id`, `ISBN`, `rating`) VALUES (?, ?, ?)", (message.chat.id, value, None))
                        #await reply(f"Список пополнен. ({recs_list[i]})")
                        books_reply += f"Список пополнен. ({recs_list[i]})\n"
                        #await bot.send_message(message.from_user.id,menu_main, reply_markup=keyboard_menu)
                        await FSMusage.crossroad.set()
                    else:
                        raise KeyError()
                except:
                    #await bot.send_message(message.from_user.id, f"Список не пополнен. ({recs_list[i]})", reply_markup=keyboard_menu)
                    books_reply += f"Список не пополнен. ({recs_list[i]})\n"
                    await FSMusage.crossroad.set()
            await bot.send_message(message.from_user.id, books_reply, reply_markup=keyboard_menu)
            await bot.send_message(message.from_user.id, menu_main, reply_markup=keyboard_menu)
            conn.commit()
        except:
            await reply("Каво? Непонел. Повтори")
    
#conn.commit()

@dp.message_handler(commands=["menu"])
async def main_menu(message : types.Message):
    global Global_message
    Global_message = message
    await bot.send_message(message.from_user.id, "Главное меню", reply_markup=keyboard_menu)
    await FSMusage.crossroad.set()

@dp.message_handler(state=None)
async def all(message : types.Message):
    global Global_message
    Global_message = message
    await reply(hello_message)

@dp.message_handler(state=FSMusage.crossroad)
async def main_menu(message : types.Message):
    global Global_message
    Global_message = message
    if message.text == b_list_text:
        cursor.execute(f"SELECT main.ISBN, Title FROM main JOIN rews ON main.ISBN = rews.ISBN WHERE user_id = {message.chat.id} AND rating IS NULL")
        books_list = cursor.fetchall()
        for i, value in enumerate(books_list):
            await reply(f"""{i+1}. {value[1]} """)
        if bool(books_list) == False:
            await reply("Список пуст")
    elif message.text == b_done_text:
        cursor.execute(f"""SELECT main.ISBN, Title, rews.rating FROM main JOIN rews ON main.ISBN = rews.ISBN WHERE user_id = {message.chat.id} AND rating IS NOT NULL """)
        done_list = cursor.fetchall()
        done_reply = ""
        for i, value in enumerate(done_list):
            done_reply += f"""{i+1}. {value[1]}\nВаша оценка {value[2]}\n """
            #await reply(f"""{i+1}. {value[1]}\nВаша оценка {value[2]} """)
        if bool(done_reply) == True:
            await reply(done_reply)
        else:
            await reply("Список пуст")
    # elif message.text == b_change_text:
    #     await bot.send_message(message.from_user.id, "Изменить эти данные?", reply_markup=keyboard)
    #     cursor_logs.execute(f"SELECT `age`, `city` FROM `users` WHERE user_id = {message.chat.id}")
    #     await reply(cursor_logs.fetchone())
    #     await FSMusage.change.set()
    elif message.text == search_book:
        await FSMusage.books.set()
        await reply("Введи название книги - мы покажем книги, которые могут вам понравиться: ") # С вас 300$
    elif message.text == b_add_done_text:
        cursor.execute(f"SELECT main.ISBN, Title FROM main JOIN rews ON main.ISBN = rews.ISBN WHERE user_id = {message.chat.id} AND rating IS NULL")
        books_list = cursor.fetchall()
        if bool(books_list) == False:
            await reply("В данный момент вы ничего не читаете - вы не можете оценить книгу")
        else:
            global done_book
            done_book = []
            global done_book_ISBN
            done_book_ISBN = []
            for i, value in enumerate(books_list):
                await reply(f"""{i+1}. {value[1]} """)
                done_book.append(value[1])
                done_book_ISBN.append(value[0])
            
            await reply("Введи номер прочитанной книги. 1 за раз.")
            await FSMusage.done.set()

@dp.message_handler(state=FSMusage.done)
async def done(message : types.Message, state: FSMContext):
    global Global_message
    Global_message = message
    try:
        choosen_one = int(message.text)
        choosen_one -= 1
        await reply(f"{done_book[choosen_one]}\nОцени эту книгу целым числом от 1 до 10")
        global readed_book
        readed_book = done_book_ISBN[choosen_one]
        await FSMusage.done_fr.set()
    except:
        None

@dp.message_handler(state=FSMusage.done_fr)
async def done_fr(message : types.Message, state: FSMContext):
    global Global_message
    Global_message = message
    if message.text in rate_list:
        if "'" in readed_book and '"' not in readed_book:
                # cursor.execute(f"""DELETE FROM user_{message.chat.id} WHERE Title = "{readed_book}" AND status IS NULL   """)
                # conn.commit()
                cursor.execute(f"""UPDATE `rews` SET rating= "{int(message.text)}" WHERE ISBN = "{readed_book}" AND user_id = {message.chat.id}""")
                conn.commit()
                await reply("Принято")
                await bot.send_message(message.from_user.id, "Главное меню", reply_markup=keyboard_menu)
                await FSMusage.crossroad.set()
        elif '"' in readed_book and "'" not in readed_book:
                # cursor.execute(f"""DELETE FROM user_{message.chat.id} WHERE Title = '{readed_book}' AND status IS NULL""")
                # conn.commit()
                cursor.execute(f"""UPDATE `rews` SET rating= '{int(message.text)}' WHERE ISBN = '{readed_book}' AND user_id = {message.chat.id} """)
                conn.commit()
                await reply("Принято")
                await bot.send_message(message.from_user.id, "Главное меню", reply_markup=keyboard_menu)
                await FSMusage.crossroad.set()
        elif '"' not in readed_book and "'" not in readed_book:
                # cursor.execute(f'DELETE FROM user_{message.chat.id} WHERE Title = "{readed_book}" AND status IS NULL')
                # conn.commit()
                cursor.execute(f"""UPDATE `rews` SET rating= ({int(message.text)}) WHERE ISBN = "{readed_book}" AND user_id = {message.chat.id} """)
                conn.commit()
                await reply("Принято")
                await bot.send_message(message.from_user.id, "Главное меню", reply_markup=keyboard_menu)
                await FSMusage.crossroad.set()
    else:
        await reply("Введите целое число от 1 до 10")
        #print("abpba")

executor.start_polling(dp, skip_updates=True)