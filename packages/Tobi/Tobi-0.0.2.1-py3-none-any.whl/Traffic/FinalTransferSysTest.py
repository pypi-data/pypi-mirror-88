import time
from Traffic import ShuttleDict, ShuttleTimeGo, SpanTimeNaver, SubTime


# , SubDict, SpanTime, NearStation
# from Util import *
# dict_go.py 있어야함 -> 딕셔너리의 키는 시간, 값은 셔틀 분 데이터 값
# h1 : 학교 도착해야 하는 시간   |원래는 eclass에서 자체적으로 받아왔음
# m1 : 학교 도착해야 하는 분     |원래는 eclass에서 자체적으로 받아왔음
# station_name : 갈산, 금정, 강남, 기흥 중 택1 : 원래는 가까운 역을 탐색하는 api로 굴렸음.
# h1 -> h2 -> h3 -> h4.... 이런식으로 역추적 하여 사용자에게 출발 추천시간을 알려줌.
# 시연용 파일이다.


def finalTransferSys(station_name, h1, m1):
    if h1[0] == '0':
        h1i = int(h1[1])
    else:
        h1i = int(h1)
    if m1[0] == '0':
        m1i = int(m1[1])
    else:
        m1i = int(m1)

    m = time.localtime().tm_mon
    d = time.localtime().tm_mday
    y = time.localtime().tm_year
    hour = time.localtime().tm_hour
    year = str(y)
    month, day = SpanTimeNaver.timeToTempTime(m, d)
    dictgo = {}
    dictgo.update(ShuttleDict.timetableGo)
    if 17 <= hour <= 18:
        h1i, m1i = SubTime.subTime(h1i, m1i, 10)
    std = ShuttleTimeGo.shuttleTimeGo(h1i, m1i, dictgo)
    h2 = int(std[0])
    m2 = int(std[1])

    lis = SpanTimeNaver.returnListu(station_name, year, month, day, h2, m2)

    h3, m3 = lis[2], lis[3]
    h4, m4 = lis[0], lis[1]
    h6, m6 = SubTime.subTime(h4, m4, 30)

    time_info = lis[4]  # station_name역 -> 정왕역까지 소요시간
    h1, m1 = SpanTimeNaver.timeToTempTime(h1, m1)  # 처음 받아온 시간
    h2, m2 = SpanTimeNaver.timeToTempTime(h2, m2)  # 수업 시간으로 부터 가장 가까운 셔틀시간
    h3, m3 = SpanTimeNaver.timeToTempTime(h3, m3)  # 정왕역에 도착하는 시간
    h4, m4 = SpanTimeNaver.timeToTempTime(h4, m4)  # 역에서 출발해야 하는 시간
    h6, m6 = SpanTimeNaver.timeToTempTime(h6, m6)  # 출발 추천시간

    t1 = h1 + "시 " + m1 + "분"
    t2 = h2 + "시 " + m2 + "분"
    t3 = h3 + "시 " + m3 + "분"
    t4 = h4 + "시 " + m4 + "분"
    t6 = h6 + "시 " + m6 + "분"
    if 17 <= h1i <= 18:
        t2 = "상시 운행"
    return station_name, t6, t4, time_info, t3, t2, t1


# 버스 시간을 넣지 않은 이유는 갈산 버스를 지원하지 않는다.
# 받아올 역 (갈산, 금정, 강남, 기흥 중 택 1)
# 받아올 시간
# 받아올 분

# 함수 출력 예시 : python
n = time.localtime().tm_wday  # 현재 요일
week = ['월', '화', '수', '목', '금']  # 요일 리스트

data = {
    '화': [['컴퓨터구조', '11:30~13:20'], ['파이썬프로그래밍', '13:30~15:20'], ['자바', '15:30~17:20'], ['글로벌시장과경제의이해', '19:05~21:40']],
    '월': [['데이터베이스', '18:15~19:55']],
    '수': [['컴퓨터구조', '11:30~12:20'], ['진로와미래', '17:25~18:15'], ['데이터베이스', '18:15~19:55']],
    '금': [['스마트센서개론', '13:30~16:20']],
    '목': [['파이썬프로그래밍', '13:30~15:20'], ['자바', '15:30~17:20']]
}
# 서버에서 받아오는 시간표 데이터
eclass = "" # 모호한 값을 방지하기 위해 eclass값 초기화
for i in range(5):
    try:
        eclass = data[week[n]][0]
    except:
        n += 1
        if n >= 5:
            n = 0
# 모호한 값을 방지하기 위한 for문 5번 (공강, 예외적인 데이터 때문)

data = finalTransferSys("강남", str(eclass[1])[0:2], str(eclass[1])[3:5])
data = finalTransferSys("강남", "17", "45")
print(data)



# print("현재 위치에서 가장 가까운 역은 " + data[0] + "역입니다.\n")
#
# print("출발 추천시간 : " + data[1]+ "\n")
#
# print(data[0] + "역에서 출발해야하는 시간 : " + data[2] + " (예상소요시간 : " + data[3] + "분)")
# print("정왕역에 도착하는 시간 : " + data[4] + "\n")
#
# print("정왕역에서 출발하는 " + data[5] + " 셔틀 탑승")
# print("학교에 도착해야하는 시간 : " + data[6] + " (시간표 정보 읽어오기)")
