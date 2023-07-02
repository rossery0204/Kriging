from obspy.clients.fdsn import Client as FDSN_Client
from obspy.core import UTCDateTime

client = FDSN_Client("IRIS")

class Event:  
    def __init__(self, starttime, endtime, latitude, longitude, maxradius, minmagnitude):
        self.starttime = UTCDateTime(starttime)
        self.endtime = UTCDateTime(endtime)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.maxradius = float(maxradius)
        self.minmagnitude = float(minmagnitude)
        
    def get_events(self):
        client = FDSN_Client("IRIS")
        cat = client.get_events(starttime = self.starttime, 
                                        endtime = self.endtime,
                                        latitude = self.latitude,
                                        longitude = self.longitude,
                                        maxradius = self.maxradius,
                                        minmagnitude = self.minmagnitude)
        #print(cat.__str__(print_all=True))
        draft = str(cat.__str__(print_all=True))
        _ = cat.plot(projection="local")
        _.savefig('event.png')
        return draft
        

       

