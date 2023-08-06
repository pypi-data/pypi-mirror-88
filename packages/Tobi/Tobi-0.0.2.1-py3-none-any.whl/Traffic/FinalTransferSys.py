import time
from Traffic import NearStation, ShuttleDict, ShuttleTimeGo, SpanTimeNaver, SubTime


# , SubDict, SpanTime
# from Util import *
# dict_go.py 있어야함 -> 딕셔너리의 키는 시간, 값은 셔틀 분 데이터 값
# h1 : 학교 도착해야 하는 시간   |원래는 eclass에서 자체적으로 받아왔음
# m1 : 학교 도착해야 하는 분     |원래는 eclass에서 자체적으로 받아왔음
# station_name : 갈산, 금정, 강남, 기흥 중 택1 : 원래는 가까운 역을 탐색하는 api로 굴렸음.
# h1 -> h2 -> h3 -> h4.... 이런식으로 역추적 하여 사용자에게 출발 추천시간을 알려줌.
# 시연용 파일이다.

def finalTransferSys(station_name, h1, m1):
    m = time.localtime().tm_mon
    d = time.localtime().tm_mday
    y = time.localtime().tm_year
    w = time.localtime().tm_wday
    m0 = time.localtime().tm_min
    h0 = time.localtime().tm_hour

    year = str(y)
    month, day = SpanTimeNaver.timeToTempTime(m, d)
    hour, minute = SpanTimeNaver.timeToTempTime(h0, m0)

    dictgo = ShuttleDict.timetableGo
    # now_location = ['37.494769', '127.026635']  # 강남
    # now_location = ['37.517565', '126.723319']  # 갈산
    now_location = ['37.374364', '126.950909']  # 금정
    # now_location = ['37.278692', '127.112100']  # 기흥
    # now_location = Now_LatNLon()
    nearsub1 = NearStation.nearSubStation(now_location[0], now_location[1])  # 좌표(현재 위치) -> 정왕역 (좌표로 부터 가까운 역 검색)

    index1 = nearsub1.rstrip('역')  # 정왕역 -> 정왕
    n = w
    # if n == 5 or n == 6:
    #     n = 1

    weeks = ['월', '화', '수', '목', '금']
    # data = Eclass.eclass.eclass("2015162013", 'mouse3178!')[weeks[n]]
    # data = Eclass.eclass("2019152015", 'hoho1023!')[1][weeks[n]]
    # h1 = int(data['hour'])
    # m1 = int(data['minute'])
    # if h0 >= h1 and m0 > m1:
    #     n += 1
    #     if n == 5 or n == 6:
    #         n = 1

    std = ShuttleTimeGo.shuttleTimeGo(h1, m1, dictgo)
    h2 = int(std[0])  # 수업 시간으로 부터 가장 가까운 셔틀시간
    m2 = int(std[1])

    lis = SpanTimeNaver.returnListu(station_name, year, month, day, h2, m2)
    i = 0

    # 1순위 2순위 3순위 데이터를 가져오는 방식으로 패치할 예정이다.
    # dict1 = {}
    # dict1['starty'], dict1['startx'] = SubDict.subDict[index1]
    # 정왕 -> 정왕역 좌표 [37.351735, 126.742989] (역이름으로 좌표 반환)

    time_info = lis[i][4]  # 역 -> 정왕역까지 소요시간
    h3, m3 = lis[i][2], lis[i][3]  # 정왕역에 도착하는 시간
    h4, m4 = lis[i][0], lis[i][1]  # 역에서 출발해야 하는 시간

    try:
        Travel_time_bus = NearStation.nearBusStation(now_location[0], now_location[1])
    except:
        Travel_time_bus = 0

    h5, m5 = SubTime.subTime(h4, m4, Travel_time_bus)  # 사용되지 않을 예정(버스 소요시간)
    h6, m6 = SubTime.subTime(h5, m5, 0)  # 출발 추천시간

    h1, m1 = SpanTimeNaver.timeToTempTime(h1, m1)
    h2, m2 = SpanTimeNaver.timeToTempTime(h2, m2)
    h3, m3 = SpanTimeNaver.timeToTempTime(h3, m3)
    h4, m4 = SpanTimeNaver.timeToTempTime(h4, m4)
    h5, m5 = SpanTimeNaver.timeToTempTime(h5, m5)
    h6, m6 = SpanTimeNaver.timeToTempTime(h6, m6)

    return index1, h6, m6, h4, m4, time_info, h3, m3, h2, m2, h1, m1, h5, m5


station_name = "금정"  # 받아올 역 (갈산, 금정, 강남, 기흥 중 택 1)
h1 = 9  # 받아올 시간
m1 = 30  # 받아올 분

data = finalTransferSys(station_name, h1, m1)

print("등교 시스템" + "-" * 60)
print("현재 위치에서 가장 가까운 역은 " + data[0] + "역입니다.\n")
print("출발 추천시간 : " + data[1] + "시 " + data[2] + "분\n")
print(data[0] + "역에서 출발해야하는 시간 : " + data[3] + "시 " + data[4] + "분(예상소요시간 : " + data[5] + "분)")
print("정왕역에 도착하는 시간 : " + data[6] + "시 " + data[7] + "분\n")

print("정왕역에서 출발하는 " + data[8] + "시 " + data[9] + "분 셔틀 탑승")
print("학교에 도착해야하는 시간 : " + data[10] + "시 " + data[11] + "분 (시간표 정보 읽어오기)")
print(data[12], data[13])
