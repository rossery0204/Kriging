from obspy.clients.fdsn import Client as FDSN_Client
from obspy.core import UTCDateTime

class Station:  
    def __init__(self, starttime, endtime, latitude, longitude, maxradius):
        self.starttime = UTCDateTime(starttime)
        self.endtime = UTCDateTime(endtime)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.maxradius = float(maxradius)
        
    
    def get_stations(self):
        client = FDSN_Client("IRIS")
        inventory = client.get_stations(starttime = self.starttime, 
                                        endtime = self.endtime,
                                        latitude = self.latitude,
                                        longitude = self.longitude,
                                        maxradius = self.maxradius)
        return inventory
        