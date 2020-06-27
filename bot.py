import telebot
import os
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup,ForceReply,ReplyKeyboardMarkup
import requests
import json

BAGYT_API = os.environ.get('BAGYT_API')
BAGYT_BOT_TOKEN = os.environ.get('BAGYT_BOT_TOKEN')

bot = telebot.TeleBot(BAGYT_BOT_TOKEN)

filter_dict = {}

subjectList = ["Биология",
               "Физика",
               "Химия",
               "География",
               "История",
               "Литература",
               "Иностр.язык",
               "Творч.экз"]

cityList = [
     "Актау",
     "Актобе", 
     "Алматы",
     "Аркалык",
     "Астана",
     "Атырау",
     "Балхаш", 
     "Жетысай",
     "Жезказган",
     "Караганда",
     "Кокшетау",
     "Каскелен",
     "Костанай",
     "Кызылорда",
     "Павлодар",
     "Петропавловск",
     "Рудный" ,
     "Семей",
     "Степногорск",
     "Талдыкорган",
     "Тараз",
     "Темиртау",
     "Туркестан",
     "Уральск",
     "Усть-Каменогорск",
     "Шымкент",
     "Экибастуз"
]


def queryGetMajorList():
    return """query{
                allMajors{
                        id
                        name
                    }
                } """

def queryGetMajorBySubject(subjectName, skipVal):
    return """query{
                allMajors(filter: {
                subject_contains:\"""" + subjectName + """\"
                    },
                    first: 15, 
                    skip: """ + str(skipVal) + """,
                    orderBy: name_ASC
                    ){
                        id
                        name
                    }
                }"""

def queryGetMajorBySubject_Meta(subjectName):
    return """query{
                _allMajorsMeta(filter: {
                subject_contains:\"""" + subjectName + """\"
                    }
                    ){
                        count
                    }
                }"""


def queryGetMajorById(majorId):
    return """query{
            Major(id: \"""" + majorId + """\"){
                id
                name
                profilSubject
                object
                index
                subject
                description
            }
        }"""


def queryGetUniversityListByTheMajor(majorId):
    return """query{
                allMajorPoints(filter: {
                    major: {
                    id: \"""" + majorId + """\"
                    }
                }){
                    kazPoint
                    kazSelPoint
                    majorIndex
                    majorName
                    rusPoint
                    rusSelPoint
                    university{
                    id
                    name
                    }
                }
            }"""


def queryGetUniversityById(universityId):
    return """query{
                University(id: \"""" + universityId + """\"){
                    id
                    city
                    name
                    address
                    description
                    email
                    phone
                    photo
                    webSite
                }

                }"""

def queryGetUniversitySearchwithFilter_meta(cityName, subjectName, majorName, searchVal):
    return """ query{
                _allUniversitiesMeta(filter:{
                    city_contains: \"""" + cityName + """\",
                    name_contains: \""""  + searchVal  + """\",
                    majorPoints_some: {
                    major:{
                        name_contains: \"""" + majorName + """\",
                        subject_contains: \"""" + subjectName + """\",
                    }
                    }
                }) { count }
                }"""

def queryGetUniversitySearchwithFilter(cityName, subjectName, majorName, searchVal, skipVal):
    return """ query{
                allUniversities(filter:{
                    city_contains: \"""" + cityName + """\",
                    name_contains: \""""  + searchVal  + """\",
                    majorPoints_some: {
                    major:{
                        name_contains: \"""" + majorName + """\",
                        subject_contains: \"""" + subjectName + """\",
                    }
                    }
                },
                    orderBy: name_ASC,
                    first: 30, 
                    skip: """ + str(skipVal) + """
                 ) {
                    id
                    name 
                    
                    }
                }"""

def queryGetUniversitySearch_meta(searchVal):
    return """ query{
                _allUniversitiesMeta(filter:{
                    name_contains: \""""  + searchVal  + """\"
                    }
                ) { count }
                }"""

def queryGetUniversitySearch(searchVal, skipVal):
    return """ query{
                allUniversities(filter:{
                    name_contains: \""""  + searchVal  + """\"
                },
                    orderBy: name_ASC,
                    first: 30, 
                    skip: """ + str(skipVal) + """
                 ) {
                    id
                    name 
                    
                    }
                }"""

def queryGetUniversityByFilter_Meta(cityName, subjectName, majorName):
        return """query{
                _allUniversitiesMeta(filter:{
                    city_contains: \"""" + cityName + """\",
                    majorPoints_some: {
                    major:{
                        name_contains: \"""" + majorName + """\",
                        subject_contains: \"""" + subjectName + """\",
                    }
                    }
                }) {
                    count
                }}"""

def queryGetUniversityByFilter(cityName, subjectName, majorName, skipVal):
    return """ query{
                allUniversities(filter:{
                    city_contains: \"""" + cityName + """\",
                    majorPoints_some: {
                    major:{
                        name_contains: \"""" + majorName + """\",
                        subject_contains: \"""" + subjectName + """\",
                    }
                    }
                },
                    orderBy: name_ASC,
                    first: 30, 
                    skip: """ + str(skipVal) + """
                 ) {
                    id
                    name 
                }}"""

def queryGetMajorListByUniversityId(universityId):
    return """query{
                allMajors(filter:{
                    majorPoints_some:{
                    university:{
                        id: \"""" + universityId + """\"
                    }
                    }
                },
                    orderBy: name_ASC){
                    id
                    name
                    majorPoints{
                            kazPoint
                            kazSelPoint
                            rusPoint
                            rusSelPoint}
                }
            }"""

def queryGetAllUniverisities():
    return """"query{
        _allUniversitiesMeta{
            count
            }
        }"""


def queryGetUniversityWithFilterByPoint(chat_id, skipVal):
    filterD = filter_dict[chat_id]
    return """ query{
            allMajorPoints(filter: {   
            kazPoint_lte: """ + str(filterD.kaz) + """,
            rusPoint_lte: """ + str(filterD.rus) + """,
            kazSelPoint_lte: """ + str(filterD.kazSel) + """,
            rusSelPoint_lte:""" + str(filterD.rusSel)+ """,
            university: {
                city_contains: \"""" + filterD.city + """\",
            },
            major: {
                name_contains:\"""" + filterD.major + """\",
                subject_contains: \"""" + filterD.subject + """\",
            }
        },
        orderBy: majorName_ASC,
        first: 15, 
        skip: """ + str(skipVal) + """){
        major {
            id
            name
        }
        university {
            id
            name
        }
        kazPoint
        rusPoint
        kazSelPoint
        rusSelPoint
    }
    }"""

def queryGetUniversityWithFilterByPoint_Meta(chat_id):
    filterD = filter_dict[chat_id]
    return """query{
            _allMajorPointsMeta(filter: {   
            kazPoint_lte: """ + str(filterD.kaz) + """,
            rusPoint_lte: """ + str(filterD.rus) + """,
            kazSelPoint_lte: """ + str(filterD.kazSel) + """,
            rusSelPoint_lte:""" + str(filterD.rusSel)+ """,
            university: {
                
                city_contains: \"""" + filterD.city + """\"
            },
            major: {
                name_contains: \"""" + filterD.major + """\",
                subject_contains:  \"""" + filterD.subject + """\"
            }
            }){
        count
    }
    }"""

majorList = []
majorListByUniverityId = []
universityList = []
callbackBackArg = ",back"
prevUni = "prevUni"
nextUni = "nextUni"
prevSearchUni = "pSUni"
nextSearchUni = "nSUni"
byPointSaveText = "byPointSave"
filterValue = ["Город:", "Предмет:", "Cпециальность:",  "Сохранить"]
kaz = "kaz"
rus = "rus"
kazSel = "kazSel"
rusSel = "rusSel"
prevUniByPoint = "prevUniByPoint"
nextUniByPoint = "nextUniByPoint"
prevMajor = "prevMajor"
nextMajor = "nextMajor"
majorF = "majorF"
major = "major"

class Filter:
    def __init__(self):
        self.city = ""
        self.major = ""
        self.subject = ""
        self.school = ""
        self.kaz = 0
        self.rus = 0
        self.kazPoint = 0
        self.rusPoint = 0
        self.saveParam = filterValue[3]
        self.point = 0
        self.search = ""
        self.majorSelect = "major"

@bot.message_handler(
    commands=['start']
)
def send_welcome(message):
    bot.reply_to(message, """Привет, дорогой друг!
    \nЯ тебе помогу выбрать университет и специальность
    \nКоманды:  \n/majors - выбрав предмет, можно найти весь список специальностей в Казахстане
                \n/universities - вы можете посмотреть весь список университетов в Казахстане
                \n/filter - для комфортабельности можете делать фильтр и сохранять как вам удобно,
                \n/point - введите балл ЕНТ и можете посмотреть список университетов на которые студенты поступили на грант в 2018 году,
                \n/search - введите на русском языке название университета, и вам выйдут результаты по поиску 
                \n/help -  поможет вам посмотреть мануал обратно
    \nТак как данные собирались из разных ресурсов, могут быть допущены ошибки. 
     Это мой первый БОТ☺️ и если будут ошибки, прошу понять и простить, просто напишите мне проблему и я исправлю
    \n@balamanova
    \nКак закончу уроки в универе, залью приложение в AppStore, PlayMarket с дополнительной функциональностью и конечно же, уведомлю Вас
    \nПользуйтесь с удовольствием :) 
              """)

@bot.message_handler(
    commands=['help']
)
def send_welcome(message):
    bot.reply_to(message, """
    Команды:  \n/majors - выбрав предмет, можно найти весь список специальностей в Казахстане
                \n/universities - вы можете посмотреть весь список университетов в Казахстане
                \n/filter - для комфортабельности можете делать фильтр и сохранять как вам удобно,
                \n/point - введите балл ЕНТ и можете посмотреть список университетов на которые студенты поступили на грант в 2018 году,
                \n/search - введите на русском языке название университета, и вам выйдут результаты по поиску 
                \n/help -  поможет вам посмотреть мануал обратно
    \nТак как данные собирались из разных ресурсов, могут быть допущены ошибки. 
     Это мой первый БОТ☺️ и если будут ошибки, прошу понять и простить, просто напишите мне проблему и я исправлю
    \n@balamanova
    \nКак закончу уроки в универе, залью приложение в AppStore, PlayMarket с дополнительной функциональностью и конечно же, уведомлю Вас
    \nПользуйтесь с удовольствием :) 
              """)

@bot.message_handler(
    commands=['majors']
)
def majors_command(msg):
    filterD = Filter()
    chat_id = msg.chat.id
    dictChecking(chat_id)
    filter_dict[chat_id] = filterD
    k = get_subjectList(",majorBySub", InlineKeyboardMarkup())   
    bot.reply_to(
        msg, "Выбери предмет, и ты увидишь список специальностей", reply_markup=k)

def get_subjectList(subList, k):
    for p in subjectList:
        callbackData = p + subList
        k.add(InlineKeyboardButton(str(p), callback_data = callbackData))
    return k

@bot.message_handler(
    commands=['universities']
)
def university_command(msg):
    chat_id = msg.chat.id
    dictChecking(chat_id)
    filterD = filter_dict[chat_id] 
    resultCount = run_query(queryGetUniversityByFilter_Meta(filterD.city, filterD.subject, filterD.major,))
    universityListSize = int(resultCount["data"]["_allUniversitiesMeta"]["count"])
    result = run_query(queryGetUniversityByFilter(filterD.city, filterD.subject, filterD.major, 0))
    k = getUniversity_list(result, 0, universityListSize, prevUni, nextUni)
    bot.reply_to(msg, "Список университетов", reply_markup=k)

def getUniversity_list(result, prevRange, universityListSize, valPrevUni, valNextUni):
    k = InlineKeyboardMarkup()
    universityList = []
    for p in result['data']['allUniversities']:
        universityList.append([p['name'], p['id']])
    for p in universityList:
        callbackData = p[1] + ",university"
        k.add(InlineKeyboardButton(str(p[0]), callback_data=callbackData))
    nextRange = prevRange + 30
    if prevRange > 0 and nextRange < universityListSize:
        k.add(InlineKeyboardButton("⬅️" , 
                callback_data = str(prevRange) + '-' + str(universityListSize) + ','+ valPrevUni),
            InlineKeyboardButton("➡️" , 
                callback_data = str(nextRange) + '-' + str(universityListSize) + ','+ valNextUni))
    elif nextRange < universityListSize:
        k.add(InlineKeyboardButton("➡️" , 
                callback_data = str(nextRange) + '-' + str(universityListSize) + ','+ valNextUni))
    elif prevRange > 0:
         k.add(InlineKeyboardButton("⬅️" , 
                callback_data = str(prevRange) + '-' + str(universityListSize) + ','+ valPrevUni))
    return k
    

@bot.message_handler(
    commands=['filter']
)
def filter_command(msg):
    chat_id = msg.chat.id
    dictChecking(chat_id)
    filterD = filter_dict[chat_id]
    filterD.saveParam = filterValue[3]
    filter_handler(msg)

def dictChecking(chat_id):
    if chat_id not in filter_dict:
        filter_dict[chat_id] = Filter()

def filter_handler(msg):
    chat_id = msg.chat.id
    dictChecking(chat_id)
    filterD = filter_dict[chat_id]
    k = InlineKeyboardMarkup() 
    cityFilter = "Все" if filterD.city  == ""  else filterD.city
    subjectFilter = "Все" if filterD.subject  == "" else filterD.subject
    majorFilter = "Все" if filterD.major == "" else filterD.major

    k.add(InlineKeyboardButton(str(filterValue[0] + ' ' + cityFilter), 
                                    callback_data=filterValue[0] + ",filter"))
    k.add(InlineKeyboardButton(str(filterValue[1] + ' ' + subjectFilter), 
                                    callback_data=filterValue[1] + ",filter"))
    k.add(InlineKeyboardButton(str(filterValue[2] + ' ' + majorFilter), 
                                    callback_data=filterValue[2] + ",filter") )   
    k.add(InlineKeyboardButton(str(filterValue[3]), 
                                    callback_data= filterD.saveParam + ",filter") )                                  
    bot.reply_to(msg, "Выберите спецификации для фильтрации", reply_markup=k)   

@bot.message_handler(
    commands=['search']
)   
def search_handler(msg):
    dictChecking(msg.chat.id)
    replied_message = bot.send_message(
        msg.chat.id, "Пожалуйста введите название университета"
    )
    bot.register_next_step_handler(replied_message, search_university)

def search_university(msg):
    resultCount = run_query(queryGetUniversitySearch_meta(msg.text))
    chat_id = msg.chat.id
    dictChecking(chat_id)
    filterD = filter_dict[chat_id]
    filterD.search = msg.text
    universityListSize = int(resultCount["data"]["_allUniversitiesMeta"]["count"])
    result = run_query(queryGetUniversitySearch(msg.text, 0))
    k = getUniversity_list(result, 0, universityListSize, prevSearchUni, nextSearchUni)
    bot.reply_to(msg, "Список университетов", reply_markup=k)

@bot.message_handler(
    commands=['point']
)   
def byPoint_handler(msg):
    dictChecking(msg.chat.id)
    replied_message = bot.send_message(
        msg.chat.id, "Пожалуйста введите балл"
    )
    bot.register_next_step_handler(replied_message, select_schoolType)

def select_schoolType(msg):
    chat_id = msg.chat.id
    dictChecking(chat_id)
    filterD = filter_dict[chat_id]
    try:
        if int(msg.text) > 0:
            filterD.point = str(int(msg.text))
            k = InlineKeyboardMarkup()
            k.add(InlineKeyboardButton("Казахская", callback_data = kaz + ",byPoint"),
                    InlineKeyboardButton("Русская", callback_data = rus + ",byPoint"))
            k.add(InlineKeyboardButton("Каз-сельский", callback_data = kazSel + ",byPoint"))
            k.add(InlineKeyboardButton("Рус-сельский", callback_data = rusSel + ",byPoint"))
            bot.send_message(msg.chat.id, "Выберите тип школы ", reply_markup=k)
        else:
            bot.reply_to(msg, "Введите числовое значение")
            byPoint_handler(msg)
    except:
        bot.reply_to(msg, "Введите числовое значение")
        byPoint_handler(msg)


     
@bot.callback_query_handler(lambda q: q.message.chat.type == "private")
def private_query(query):
    dictChecking(query.message.chat.id)
    queryData = query.data.split(',')
    queryType = queryData[1]
    if queryType == 'major':
        get_majorById(queryData[0], query.message)

    elif queryType == 'majorBySub':
        chat_id = query.message.chat.id
        filterD = filter_dict[chat_id]
        filterD.subject = queryData[0]
        filterD.majorSelect = "major"
        resultCount = run_query(queryGetMajorBySubject_Meta(filterD.subject))
        majorListSize = int(resultCount["data"]["_allMajorsMeta"]["count"])
        k = queryGetMajorWithRangeBySubject(0, query.message, majorListSize)
        bot.reply_to(query.message,  "Список специальностей", reply_markup=k)

    elif queryType == 'universityList':
        majorId = queryData[0]
        result = run_query(queryGetUniversityListByTheMajor(majorId))
        k = InlineKeyboardMarkup()
        listUniversity = []

        for p in result['data']['allMajorPoints']:
            if p['university'] is not None:
                htmlMarkup = [str(p['kazPoint']), str(p['kazSelPoint']), str(
                    p['rusPoint']), str(p['rusSelPoint'])]
                listUniversity.append([p['university'], htmlMarkup])

        for university in listUniversity:
            callbackData = university[0]['id'] + ",university"
            k.add(InlineKeyboardButton(
                str(university[0]['name']), callback_data=callbackData))
            k.add(InlineKeyboardButton("Каз:" + university[1][0] + " Cел:" + university[1][1], callback_data="1,2"),
                  InlineKeyboardButton("Рус:" + university[1][2] + " Cел:" + university[1][3], callback_data="1,2"))

        bot.reply_to(query.message, "Список университетов", reply_markup=k)

    elif queryType == 'university':
        universityId = queryData[0]
        get_universityById(universityId, query.message)

    elif queryType == 'majorList':
        universityId = queryData[0]
        result = run_query(queryGetMajorListByUniversityId(universityId))
        majorListByUniverityId.clear()
        k = InlineKeyboardMarkup()
        for p in result['data']['allMajors']:
            htmlMarkup = ''
            for point in p['majorPoints']:
                htmlMarkup = [str(point['kazPoint']), str(point['kazSelPoint']),
                     str(point['rusPoint']), str(point['rusSelPoint'])]

            majorListByUniverityId.append([p['name'], p['id'], htmlMarkup])

        for major in majorListByUniverityId:
            callbackData = major[1] + ",majUni"
            k.add(InlineKeyboardButton(str(major[0]), callback_data = callbackData))
            # k.add(InlineKeyboardButton("Каз:" + major[2][0] + " Cел:" +  major[2][1], callback_data = "1,2"),
            #     InlineKeyboardButton("Рус:" + major[2][2] + " Cел:" +  major[2][3], callback_data = "1,2"))
        bot.reply_to(query.message, "Список специальностей", reply_markup=k)

    elif queryType == 'subMF':
        chat_id = query.message.chat.id
        filterD = filter_dict[chat_id]
        filterD.subject = queryData[0]
        filterD.majorSelect = "majorF"
        resultCount = run_query(queryGetMajorBySubject_Meta(filterD.subject))
        majorListSize = int(resultCount["data"]["_allMajorsMeta"]["count"])
        k = queryGetMajorWithRangeBySubject(0, query.message, majorListSize)
        bot.reply_to(query.message,  "Список специальностей", reply_markup=k)

    elif queryType == 'filter':
        k = InlineKeyboardMarkup()
        if queryData[0] == filterValue[0]:
            callBackArg = ",cityF"
            k.add(InlineKeyboardButton("Все", callback_data = callBackArg))
            for city in cityList:
                callbackData = city + callBackArg
                k.add(InlineKeyboardButton(city, callback_data = callbackData))
            k.add(InlineKeyboardButton("Назад", callback_data = callbackBackArg ))
            bot.reply_to(query.message, "Список городов", reply_markup=k)

        elif queryData[0] == filterValue[2]:
            k = get_subjectList(",subMF", k)
            bot.reply_to(query.message, 
                "Выбери предмет, и ты увидишь список специальностей", 
                reply_markup=k
                )
        elif queryData[0] == filterValue[1]:
            callBackArg = ",subF"
            k.add(InlineKeyboardButton("Все", callback_data = callBackArg))
            k = get_subjectList(callBackArg, k)
            k.add(InlineKeyboardButton("Назад", callback_data = callbackBackArg))
            bot.reply_to(query.message, 
                "Список предметов", 
                reply_markup=k
                )                
        elif queryData[0] == filterValue[3]:
            university_command(query.message)
            
        elif queryData[0] == byPointSaveText:
            byPointSave(query.message)

    elif queryType == "byPoint":
        chat_id = query.message.chat.id
        filterD = filter_dict[chat_id]
        filterD.school = queryData[0]
        filterD.saveParam = byPointSaveText
        filter_handler(query.message)
         
    elif queryType == majorF:
        chat_id = query.message.chat.id
        filterD = filter_dict[chat_id]
        filterD.major = '' if queryData[0]=='' else get_majorNameById(queryData[0])
        filter_handler(query.message)
    elif queryType == 'subF':
        chat_id = query.message.chat.id
        filterD = filter_dict[chat_id]
        filterD.subject = queryData[0]
        filter_handler(query.message)
    elif queryType == 'cityF':
        chat_id = query.message.chat.id
        filterD = filter_dict[chat_id]
        filterD.city = queryData[0]
        filter_handler(query.message)
    elif queryType == 'back':
        filter_handler(query.message)
    elif queryType == nextUni:
        rangeData = queryData[0].split('-')
        bot.edit_message_text(chat_id = query.message.chat.id,
                                message_id = query.message.message_id,
                                text = "Список университетов",
                                reply_markup = edit_universityListPagination(
                                    rangeData[0], 
                                    query.message, 
                                    int(rangeData[1])
                                    ),
                                parse_mode='HTML'
                                )
        

    elif queryType == prevUni:
        rangeData = queryData[0].split('-')
        bot.edit_message_text(chat_id = query.message.chat.id,
                                message_id = query.message.message_id,
                                text = "Список университетов",
                                reply_markup = edit_universityListPagination(
                                    int(rangeData[0]) - 30, 
                                    query.message, 
                                    int(rangeData[1])
                                    ),
                                parse_mode='HTML'
                                )
    elif queryType == nextSearchUni:
        rangeData = queryData[0].split('-')
        bot.edit_message_text(chat_id = query.message.chat.id,
                                message_id = query.message.message_id,
                                text = "Список университетов",
                                reply_markup = edit_filterUniversityListPagination(
                                    rangeData[0], 
                                    query.message, 
                                    int(rangeData[1])
                                    ),
                                parse_mode='HTML'
                                )
    elif queryType == prevSearchUni:
        rangeData = queryData[0].split('-')
        bot.edit_message_text(chat_id = query.message.chat.id,
                                message_id = query.message.message_id,
                                text = "Список университетов",
                                reply_markup = edit_filterUniversityListPagination(
                                    int(rangeData[0]) - 30, 
                                    query.message, 
                                    int(rangeData[1])
                                    ),
                                parse_mode='HTML'
                                )
    elif queryType == nextUniByPoint:
        rangeData = queryData[0].split('-')
        bot.edit_message_text(chat_id = query.message.chat.id,
                                message_id = query.message.message_id,
                                text = "Список университетов и специальностей",
                                reply_markup = edit_byPointUniversityListPagination(
                                    rangeData[0], 
                                    query.message, 
                                    int(rangeData[1])
                                    ),
                                parse_mode='HTML'
                                )
    elif queryType == prevUniByPoint:
        rangeData = queryData[0].split('-')
        bot.edit_message_text(chat_id = query.message.chat.id,
                                message_id = query.message.message_id,
                                text = "Список университетов и специальностей",
                                reply_markup = edit_byPointUniversityListPagination(
                                    int(rangeData[0]) - 15, 
                                    query.message, 
                                    int(rangeData[1])
                                    ),
                                parse_mode='HTML'
                                )
    elif queryType == nextMajor:
        rangeData = queryData[0].split('-')
        bot.edit_message_text(chat_id = query.message.chat.id,
                                message_id = query.message.message_id,
                                text = "Список специальностей",
                                reply_markup = queryGetMajorWithRangeBySubject(
                                    rangeData[0], 
                                    query.message, 
                                    int(rangeData[1])
                                    ),
                                parse_mode='HTML'
                                )
    elif queryType == prevMajor:
        rangeData = queryData[0].split('-')
        bot.edit_message_text(chat_id = query.message.chat.id,
                                message_id = query.message.message_id,
                                text = "Список специальностей",
                                reply_markup = queryGetMajorWithRangeBySubject(
                                    int(rangeData[0]) - 15, 
                                    query.message, 
                                    int(rangeData[1])
                                    ),
                                parse_mode='HTML'
                                )

def edit_universityListPagination(range, msg, rangeOfUniversityList):
    chat_id = msg.chat.id
    dictChecking(chat_id)
    filterD = filter_dict[chat_id]
    result = run_query(queryGetUniversityByFilter(filterD.city, filterD.subject, filterD.major, range))
    return getUniversity_list(result, int(range), rangeOfUniversityList, prevUni, nextUni )

def edit_filterUniversityListPagination(range, msg, rangeOfUniversityList):
    chat_id = msg.chat.id
    dictChecking(chat_id)
    filterD = filter_dict[chat_id]
    result = run_query(queryGetUniversitySearch(filterD.search, range))
    return getUniversity_list(result, int(range), rangeOfUniversityList, prevSearchUni, nextSearchUni)

def edit_byPointUniversityListPagination(range, msg, rangeOfUniversityList):
    chat_id = msg.chat.id
    dictChecking(chat_id)
    result = run_query(queryGetUniversityWithFilterByPoint(chat_id, range))
    return byPointSave_getList(result, int(range), rangeOfUniversityList, prevUniByPoint, nextUniByPoint)


def queryGetMajorWithRangeBySubject(range, msg, rangeOfMajorList):
    chat_id = msg.chat.id
    dictChecking(chat_id)
    filterD = filter_dict[chat_id]
    result = run_query(queryGetMajorBySubject(filterD.subject, range))
    k = InlineKeyboardMarkup()
    callBackArg = "," + filterD.majorSelect 
    if callBackArg == majorF:
        k.add(InlineKeyboardButton("Все", callback_data = callBackArg))
        k = get_majorList(result, k, callBackArg, int(range), rangeOfMajorList)
        k.add(InlineKeyboardButton("Назад", callback_data = callbackBackArg ))
    else:
        k = get_majorList(result, k, callBackArg, int(range), rangeOfMajorList)
    return k


def get_majorList(result, k, callBackArg, prevRange, majorListSize):
    majorList = []
    for p in result['data']['allMajors']:
        majorList.append([p['name'], p['id']])
    for p in majorList:
        callbackData = str(p[1]) + callBackArg
        k.add(InlineKeyboardButton(str(p[0]), callback_data=callbackData))
    nextRange = prevRange + 15
    if prevRange > 0 and nextRange < majorListSize:
        k.add(InlineKeyboardButton("⬅️" , 
                callback_data = str(prevRange) + '-' + str(majorListSize) + ','+ prevMajor),
            InlineKeyboardButton("➡️" , 
                callback_data = str(nextRange) + '-' + str(majorListSize) + ','+ nextMajor))
    elif nextRange < majorListSize:
        k.add(InlineKeyboardButton("➡️" , 
                callback_data = str(nextRange) + '-' + str(majorListSize) + ','+ nextMajor))
    elif prevRange > 0:
         k.add(InlineKeyboardButton("⬅️" , 
                callback_data = str(prevRange) + '-' + str(majorListSize) + ','+ prevMajor))
    return k
    

def get_majorById(majorId, message):
    result = run_query(queryGetMajorById(majorId))
    getUniversityMarkup = InlineKeyboardMarkup()
    result = result['data']['Major']
    callbackData = result['id'] + ',universityList'
    getUniversityMarkup.add(InlineKeyboardButton(
        "Cписок университeтов с этой специальностью", callback_data=callbackData))
    bot.reply_to(message, """ *Специалность:* {0} \n *Индекс:* {1} \n *Предметы:* {2}, {3}
                                    \n *Описание:* {4}
                                    \n *Объект:* {5} """.format(
        result['name'],
        result['index'],
        result['subject'],
        result['profilSubject'],
        result['description'],
        result['object']),
        parse_mode='Markdown',
        reply_markup=getUniversityMarkup)

def byPointSave(msg):
    chat_id = msg.chat.id
    dictChecking(chat_id)
    filterD = filter_dict[chat_id]
    school = filterD.school
    if school == kaz:
        filterD.kaz = filterD.point
        filterD.rus = 0
        filterD.kazSel = 0
        filterD.rusSel = 0
    elif school == rus:
        filterD.kaz = 0
        filterD.rus = filterD.point
        filterD.kazSel = 0
        filterD.rusSel = 0
    elif school == kazSel:
        filterD.kaz = 0
        filterD.rus = 0
        filterD.kazSel = filterD.point
        filterD.rusSel = 0
    elif school == rusSel:
        filterD.kaz = 0
        filterD.rus = 0
        filterD.kazSel = 0
        filterD.rusSel = filterD.point
    resultCount = run_query(queryGetUniversityWithFilterByPoint_Meta(chat_id))
    universityListSize = int(resultCount["data"]["_allMajorPointsMeta"]["count"])
    result = run_query(queryGetUniversityWithFilterByPoint(chat_id, 0))
    k = byPointSave_getList(result, 0, universityListSize, prevUniByPoint, nextUniByPoint)
    bot.reply_to(msg, "Список университетов и специальностей", reply_markup=k)

def byPointSave_getList(result, prevRange, listSize, valPrevUni, valNextUni):
    k = InlineKeyboardMarkup()
    listUniversity = []
    for p in result['data']['allMajorPoints']:
        if p['university'] is not None:
            htmlMarkup = [str(p['kazPoint']), str(p['kazSelPoint']), str(
                p['rusPoint']), str(p['rusSelPoint'])]
            listUniversity.append([p['university'], htmlMarkup, p['major']])

    for university in listUniversity:
            callbackDataUniver = university[0]['id'] + ",university"
            callbackDataMajor = university[2]['id'] + ",major"
            k.add(InlineKeyboardButton(
                str(university[0]['name']), callback_data=callbackDataUniver))
            k.add(InlineKeyboardButton(
                str(university[2]['name']), callback_data=callbackDataUniver))   
            k.add(InlineKeyboardButton("Каз:" + university[1][0] + " Cел:" + university[1][1], callback_data="1,2"),
                  InlineKeyboardButton("Рус:" + university[1][2] + " Cел:" + university[1][3], callback_data="1,2"))
    nextRange = prevRange + 15
    if prevRange > 0 and nextRange + 1 <= listSize:
        k.add(InlineKeyboardButton("⬅️" , 
                callback_data = str(prevRange) + '-' + str(listSize) + ','+ valPrevUni),
            InlineKeyboardButton("➡️" , 
                callback_data = str(nextRange) + '-' + str(listSize) + ','+ valNextUni))
    elif nextRange < listSize:
        k.add(InlineKeyboardButton("➡️" , 
                callback_data = str(nextRange) + '-' + str(listSize) + ','+ valNextUni))
    elif prevRange > 0:
         k.add(InlineKeyboardButton("⬅️" , 
                callback_data = str(prevRange) + '-' + str(listSize) + ','+ valPrevUni))
    return k


def get_majorNameById(majorId):
    result = run_query(queryGetMajorById(majorId))
    result = result['data']['Major']
    return result['name']
     

def get_universityById(universityId, message):
    result = run_query(queryGetUniversityById(universityId))
    result = result['data']['University']
    callbackData = result['id'] + ',majorList'
    getUniversityMarkup = InlineKeyboardMarkup()
    getUniversityMarkup.add(InlineKeyboardButton(
        "Cписок специальностей ", callback_data=callbackData))

    bot.reply_to(message, """{7}\n<b>Название:</b> {0}
                                \n<b>Город:</b>  {1}
                                \n<b>Описание:</b> {2}
                                \n<b>Почта: </b> {3}
                                \n<b>Телефон:</b>  {4}
                                \n<b>Веб - сайт:</b>  {5}
                                \n<b>Адресс:</b>  {6} """.format(
        result['name'],
        result['city'],
        result['description'],
        result['email'],
        result['phone'],
        result['webSite'],
        result['address'],
        result['photo']),
        parse_mode='HTML',
        reply_markup=getUniversityMarkup)


def run_query(query):
    request = requests.post(BAGYT_API,
        json={'query': query}
        )
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))


if __name__ == '__main__':
    bot.polling(none_stop=True)
