from obspy.clients.fdsn import Client as FDSN_Client
from obspy.core import UTCDateTime

#Vẽ biểu đồ sóng
client = FDSN_Client("IRIS")

class DayPlot:  
    timelong = 86400 #số giây 1 ngày
    def __init__(self, network, station, location, channel, starttime):
        self.network = str(network)
        self.station = str(station)
        self.location = str(location)
        self.channel = str(channel)
        self.starttime = UTCDateTime(starttime)

    def get_dayplot(self):
        #Vẽ biểu đồ day_plot
        st = client.get_waveforms(self.network, self.station, self.location, self.channel, self.starttime, 
                                  UTCDateTime(self.starttime + self.timelong))
        _ = st.plot(type="dayplot")
        _.savefig('waveform dayplot.png')
