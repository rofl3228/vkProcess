from bs4 import BeautifulSoup as bs
from os import listdir
import json
from datetime import datetime

def sortDate(val):
    return val.get(date, 0)

def hour_format(time):
    if (len(time) < 8):
        return "0" + time 
    else:
        return time

def month_num(month):
    if (month == "янв"):
        return '01'
    if (month == "фев"):
        return '02'
    if (month == "мар"):
        return '03'
    if (month == "апр"):
        return '04'
    if (month == "мая"):
        return '05'
    if (month == "июн"):
        return '06'
    if (month == "июл"):
        return '07'
    if (month == "авг"):
        return '08'
    if (month == "сен"):
        return '09'
    if (month == "окт"):
        return '10'
    if (month == "ноя"):
        return '11'
    if (month == "дек"):
        return '12'    

output = open('./output.json', 'w', encoding='utf-8')
data = []

for file in listdir('./decode'):
    print(file)
    document = open('./decode/' + file, mode='r', encoding='utf-8')
    #document = open('./decode/messages10500.html', mode='r', encoding='utf-8')

    content = document.read()
    soup = bs(content, "html.parser")
    raw_messages = soup.find_all("div", "message")
    for raw_message in raw_messages:
        raw_sender = raw_message.contents[1].contents[0]
        sender = ""
        date = ""
        if (hasattr(raw_sender, 'contents')):
            # print(raw_sender.contents[0], raw_message.contents[1].contents[1])
            sender = raw_sender.contents[0]
            date = raw_message.contents[1].contents[1][2:]
        else:
            # print(raw_sender.string)
            split_h = raw_sender.string.split(', ')
            sender = split_h[0]
            date = split_h[1]

        message = raw_message.contents[3].string if raw_message.contents[3].string else 'Attachment'
        # print(sender + ", " + date)
        
        date_arr = date.split(' ')
        new_date = (date_arr[0] if len(date_arr[0]) == 2 else '0' + date_arr[0]) + '-' + month_num(date_arr[1]) + '-' + date_arr[2] + ' ' + hour_format(date_arr[4])
        # print(datetime.strptime(new_date, "%d-%m-%Y %H:%M:%S"))
        
        data.append({"sender": sender, "date": int(datetime.strptime(new_date, "%d-%m-%Y %H:%M:%S").timestamp()), "message": message});    

data.sort(key = sortDate)    
json.dump(data, output, ensure_ascii=False, indent=2)
output.close()  