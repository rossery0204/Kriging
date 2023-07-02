import Station
import Event
import WavePlot
import DayPlot
import Spectrogram
import Kriging

    
def choose():   
    print("Chọn chương trình bạn muốn thực hiện:")
    print(" 1-Xem các trạm quan trắc")
    print(" 2-Xem các sự kiện địa chấn")
    print(" 3-Vẽ biểu đồ dạng sóng")
    print(" 4-Vẽ biểu đồ dạng quang phổ")
    print(" 5-Vẽ biểu đồ ngày")
    print(" 6-Nội suy Kriging trên bản đồ Việt Nam")
    print(" 0-Dừng chường trình")
    try: 
        choice = int(input())
        if (choice == 1):
            execute_1()
        elif (choice == 2):
            execute_2()
        elif (choice == 3):
            execute_3()
        elif (choice == 4):
            execute_4()
        elif (choice == 5):
            execute_5()
        elif (choice == 6):
            execute_6()
        elif (choice == 0):
            exit
    # except:
    #     print ("Đã xảy rã lỗi. Mời nhập lại!")
    except Exception as e:
        print(e)
        
# INPUT:
# Thời gian bắt đầu:
# 2008-06-01T11:00:00.000
# Thời gian kết thúc:
# 2008-07-31T11:00:00.000 
# Vĩ độ (TP Huế):
# 16.47824423645664
# Kinh độ (TP Huế):
# 107.57367886624145
# Bán kính tối đa:
# 10         
def execute_1():
    print("Nhập thời gian bắt đầu:")
    starttime = input()
    print("Nhập thời gian kết thúc:")
    endtime = input()
    print("Nhập vĩ độ:")
    latitude = input()
    print("Nhập kinh độ:")
    longitude = input()
    print("Nhập bán kinh tối đa:")
    maxradius = input()
    
    station = Station.Station(starttime, endtime, latitude, longitude, maxradius)
    inventory = station.get_stations()
    print(inventory)
    inventory.plot(projection="local")
    
# INPUT: 
#     Thời gian bắt đầu: 
#         2008-07-01T11:00:00.000 
#     Thời gian kết thúc: 
#         2008-12-31T11:00:00.000 
#     Vĩ độ (TP Huế): 
#         16.47824423645664 
#     Kinh độ (TP Huế): 
#         107.57367886624145 
#     Bán kính tối đa: 
#         10 
#     Cường độ tối thiểu: 
#         2    
def execute_2():
    print("Nhập thời gian bắt đầu:")
    starttime = input()
    print("Nhập thời gian kết thúc:")
    endtime = input()
    print("Nhập vĩ độ:")
    latitude = input()
    print("Nhập kinh độ:")
    longitude = input()
    print("Nhập bán kinh tối đa:")
    maxradius = input()
    print("Nhập cường độ tối thiểu:")
    minmagnitude = input()
    
    event = Event.Event(starttime, endtime, latitude, longitude, maxradius, minmagnitude)
    draft = event.get_events()
    return draft

# INPUT:
# Thời gian bắt đầu:
# 2008-06-01T15:00:00.000
# Thời gian kết thúc:
# 2008-06-01T16:00:00.000
# Vĩ độ (TP Huế):
# 16.47824423645664
# Kinh độ (TP Huế):
# 107.57367886624145
# Bán kính tối đa:
# 10    
def execute_3():
    print("Nhập thời gian bắt đầu:")
    starttime = input()
    print("Nhập thời gian kết thúc:")
    endtime = input()
    print("Nhập vĩ độ:")
    latitude = input()
    print("Nhập kinh độ:")
    longitude = input()
    print("Nhập bán kinh tối đa:")
    maxradius = input()
    
    wave = WavePlot.Wave(starttime, endtime, latitude, longitude, maxradius)
    wave.get_waveforms()

# INPUT:
# Mạng:
# IC
# Trạm:
# QIZ
# Vị trí: \ 00
# Kênh:
# BHZ
# Thời gian bắt đầu:
# 2008-06-01T15:00:00.000
# Thời gian kết thúc:
# 2008-06-01T16:00:00.000    
def execute_4():
    print("Nhập tên mạng:")
    network = input()
    print("Nhập tên trạm:")
    station = input()
    print("Nhập vị trí:")
    location = input()
    print("Nhập kênh")
    channel = input()
    print("Nhập thời gian bắt đầu:")
    starttime = input()
    print("Nhập thời gian kết thúc:")
    endtime = input()
    
    spectrogram = Spectrogram.Spectrogram(network, station, location, channel, starttime, endtime)
    spectrogram.get_spectrogram()

# INPUT:
# Mạng:
# IC
# Trạm:
# QIZ
# Vị trí:
# 00
# Kênh:
# BHZ
# Thời gian bắt đầu:
# 2008-06-01T00:00:00.000    
def execute_5():
    print("Nhập tên mạng:")
    network = input()
    print("Nhập tên trạm:")
    station = input()
    print("Nhập vị trí:")
    location = input()
    print("Nhập kênh")
    channel = input()
    print("Nhập thời gian bắt đầu:")
    starttime = input()
    
    dayPlot = DayPlot.DayPlot(network, station, location, channel, starttime)
    dayPlot.get_dayplot()
    
def execute_6():
    event = execute_2()
    #variogram model spherical
    variogram_model = 'spherical'
    s_OK = Kriging.Kriging(variogram_model, event)
    plt1 = s_OK.Interpolation_local()
    plt1.title("Interpolation with spherical")

    plt2 = s_OK.Interpolation_extended()
    plt2.title("Interpolation with spherical")

    # #variogram model gaussian
    variogram_model = 'gaussian'
    g_OK = Kriging.Kriging(variogram_model, event)
    plt3 = g_OK.Interpolation_local()
    plt3.title("Interpolation with gaussian")

    plt4 = g_OK.Interpolation_extended()
    plt4.title("Interpolation with gaussian")

    #variogram model exponential
    variogram_model = 'exponential'
    e_OK = Kriging.Kriging(variogram_model, event)
    plt5 = e_OK.Interpolation_local()
    plt5.title("Interpolation with exponential")

    plt6 = e_OK.Interpolation_extended()
    plt6.title("Interpolation with exponential")
    
def main():
    choose()

if __name__ == "__main__":
    main()