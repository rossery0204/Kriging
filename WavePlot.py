from obspy.clients.fdsn import Client as FDSN_Client
from obspy import Stream
import Station
from obspy.core import UTCDateTime

#Vẽ biểu đồ sóng
client = FDSN_Client("IRIS")

class Wave:  
    def __init__(self, starttime, endtime, latitude, longitude, maxradius):
        self.starttime = UTCDateTime(starttime)
        self.endtime = UTCDateTime(endtime)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.maxradius = float(maxradius)
        
    def get_waveforms(self):
        stations = Station.Station(self.starttime, self.endtime, self.latitude, self.longitude, self.maxradius)
        inventory = stations.get_stations()
        #Lấy dữ liệu các sóng địa chấn và vẽ biểu đồ sóng
        st= Stream()
        for network in inventory:
            for station in network:
                try:
                    st+= client.get_waveforms(network.code, station.code, "*","*", self.starttime, self.endtime)
                except:
                    pass
        print(st)
        for i in range (0, len(st) - 3, 4):
            st[i:i+3].plot()
        
        
