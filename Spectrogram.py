from obspy.clients.fdsn import Client as FDSN_Client
from obspy.core import UTCDateTime


#Vẽ biểu đồ sóng
client = FDSN_Client("IRIS")

class Spectrogram:  
    def __init__(self, network, station, location, channel, starttime, endtime):
        self.network = str(network)
        self.station = str(station)
        self.location = str(location)
        self.channel = str(channel)
        self.starttime = UTCDateTime(starttime)
        self.endtime = UTCDateTime(endtime)
        
    def get_spectrogram(self):
        st = client.get_waveforms(self.network, self.station, self.location, self.channel, self.starttime, self.endtime)
        st.trim(self.starttime, self.endtime)
        st.plot()
        st.spectrogram(log= True)



