import os
import csv
import random
from random import randrange
import datetime

# common functions
def get_random_value(arr):
    return random.choice(arr)

# functions about address 
def get_addresses(file_path):
    addresses = []
    for line in open(file_path, mode="r", encoding="cp949"):
        line = line.split('\t')
        if line:
            _address = ""
            for idx, word in enumerate(line):
                if idx == len(line)-1:
                    _address += word 
                else:
                    _address += word + " "
            addresses.append(_address.replace("\n", ""))
    return addresses

def save_address(addresses):
    wtr = csv.writer(open('address.csv', 'w'), delimiter=',', lineterminator='\n')
    for address in addresses : 
        wtr.writerow ([address])
    print('saved addresses!')

# functions about date and time
def get_random_date():
    months = [i for i in range(1,13)]
    dates = [i for i in range(1,32)]
    random_month = random.choice(months)
    random_date = random.choice(dates)

    while True:
        if random_month in [4,6,9,11] and random_date == 31:
            random_date = random.choice(months)
        if random_month == 2 and random_date > 28:
            random_date = random.choice(months)
        else: break
    
    return random_month, random_date

def get_random_time():
    startDate = datetime.datetime(2000, 1, 1, 00, 00)
    random_time = startDate + datetime.timedelta(hours=randrange(24), minutes=randrange(60))
    _times = [str(i)+'시' for i in range(0,25)]
    _time1 = random_time.strftime("%s:%s" % (random_time.hour, random_time.minute)), #랜덤한 시각 추출
    _time2 = random.choice(_times) #0시~24시 중 랜덤한 값 추출
    return random.choice([_time1[0], _time2])

def get_random_date_format():
    # tag
    DATE_TAG = 'DAT-B'
    TIME_TAG = 'TIM-B'

    # random 데이터 생성
    sign = random.choice(['.','/'])
    month1, date1 = get_random_date()
    month2, date2 = get_random_date()

    days = ['월', '화', '수', '목', '금', '토', '일','']
    day1 = random.choice(days)
    if day1:
        day1 = random.choice(['({day})'.format(day=day1), day1])
    day2 = random.choice(days)
    if not day1: day2 = ''
    else:
        day2 = random.choice(['({day})'.format(day=day2), day2])

    # 같은 format의 random time 2개 생성
    space = ' ' # 시간 앞 스페이스 여부 저장
    time1 = random.choice([get_random_time(), ''])
    time2 = get_random_time()
    has_time = False if time1 == '' else True 
    
    if not has_time: time2 = '' # 빈 텍스트일 경우
    while True:
        if ('시' in time1 and '시' not in time2) or ('시' not in time1 and '시' in time2):
            time2 = random.choice(get_random_time())
        else: break
    # 시간 구간 생성
    time_period = str(time1) + '~' + str(time2)
    if not has_time: 
        time_period = ''
        space = ''

    # [type, data] 형식
    full_date1 = '{month}{sign}{date}{day}'.format(month=month1, sign=sign, date=date1, day=day1)
    full_date2 = '{month}{sign}{date}{sign}{day}'.format(month=month1, sign=sign, date=date1, day=day1)
    full_date = random.choice([full_date1, full_date2])

    data = [
        # single day, single time
        ['normal', '{full_date}{space}{time}'.format(full_date=full_date, time=time1, space=space)],

        # single day, time period
        ['time_period', '{full_date}{space}{time_period}'.format(full_date=full_date, time_period=time_period, space=space)],

        # period
        ['period', '{full_date}{space}{time1}~{full_date}{space}{time2}'.format(full_date=full_date, time1=time1, time2=time2, space=space)],
    ]

    random_data = random.choice(data) 
    type = random_data[0]
    _data = random_data[1]
    result = []

    if type == 'normal':
        result = [[full_date, DATE_TAG]]
        if has_time: result.append([time1, TIME_TAG])
    elif type == 'time_period':
        result = [full_date, DATE_TAG]
        if has_time: result.append([time_period, TIME_TAG])
    else:
        result = [[full_date, DATE_TAG]]
        if has_time: 
            result.append([time1, TIME_TAG])
            result.append([full_date, DATE_TAG])
            result.append([time2, TIME_TAG])

    return result

# main
if __name__ == '__main__':
    # path
    current_path = os.getcwd()
    address_data_path = current_path+"/generate_message_data/data/address.txt"

    # 주소
    addresses = get_addresses(address_data_path)
    save_address(addresses)
    print(get_random_value(addresses))

    # 날짜, 시간
    print(get_random_date_format())
 