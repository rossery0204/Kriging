import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pykrige.ok import OrdinaryKriging


class Kriging:
    def __init__(self, variogram_model, event):
        self.variogram_model = str(variogram_model)
        self.event = str(event)
        
    def input_validate(self):
        lats=[]
        lons=[]
        data=[]
        draft = self.event.splitlines()
        #print(draft)
        draft = str(draft)
        draft = draft.split(" | ")
        draft = str(draft)
        #print(draft)
        draft = draft.split(", ")
        for i in range (len(draft)):
            draft[i] = draft[i].replace("'", "")
            draft[i] = draft[i].replace('"', "")
            draft[i] = draft[i].replace(']', "")
            if (i % 4 == 0 and i != 0):
                draft[i] = draft[i].replace(" Ms", "")
                draft[i] = draft[i].replace(" MD", "")
                draft[i] = draft[i].replace(" ML", "")
                draft[i] = draft[i].replace(" mb", "")
                draft[i] = float(draft[i])
                data.append(draft[i])
            elif (i % 4 == 2):
                draft[i] = float(draft[i])
                lats.append(draft[i])
            elif (i % 4 == 3):
                draft[i] = float(draft[i])
                lons.append(draft[i])
        return lats, lons, data
    
    def Interpolation_local(self):
        lats, lons, data = self.input_validate()
        print("data = ", data)
        
        print("---lats", lats)
        print("---lons", lons)
        #data exploration
        #check normal distribution
        #plt.hist(data)
        
        data_len = len(data)
        # Interpolation by kriging equation system
        OK = OrdinaryKriging(
            lons,
            lats,      
            data, 
            variogram_model=self.variogram_model,
            verbose=True,
            enable_plotting=True,
            nlags = data_len
        )

        #plotting
        data_len = len(lats)
        min_lon = min(lons)
        min_lat = min(lats)
        max_lon = max(lons)
        max_lat = max(lats)
        grid_space = 1
        
        grid_lon = np.arange(min_lon, max_lon + 1, grid_space) 
        grid_lat = np.arange(min_lat, max_lat + 1, grid_space)
        z_value, variance = OK.execute('grid', grid_lon, grid_lat)
        # Z-values of specified grid or at the specified set of points.
        # Variance at specified grid points or at the specified set of points.
        print ("z-values = ", z_value)
        print ("variance = ", variance)

        xintrp, yintrp = np.meshgrid(grid_lon, grid_lat)
        fig, ax = plt.subplots()

        # set basemap for background plotting
        m= Basemap(projection= 'merc', llcrnrlat= min_lat, urcrnrlat= max_lat,
                   llcrnrlon= min_lon, urcrnrlon= max_lon, resolution='h', ax =ax)
        # đường bờ biển
        m.drawcoastlines()
        # đường biên giới
        m.drawmapboundary(color='k', fill_color=None, zorder=-1)
        # Bổ sung đường biên giới của Việt Nam bằng dựa trên long lat
        m.drawcountries(linewidth=1, linestyle='solid', color='k')
        # vĩ tuyến
        parallels = np.arange(int(min_lat), max_lat, 1)
        m.drawparallels(parallels, labels= [1, 1, 0, 0], fontsize=9, color='gray')
        #kinh tuyến
        meridians = np.arange(int(min_lon), max_lon, 2)
        m.drawmeridians(meridians, labels=[0,0,0,1], fontsize=9, color='gray')
        x,y=m(xintrp, yintrp) # convert the coordinates into the map scales
        
        #phủ màu
        cs = m.contourf(x,y,z_value,alpha=0.95,extend='both')
        cbar= m.colorbar(cs, pad=0.4, shrink=0.5, aspect=15, location='bottom')
        cbar.outline.set_linewidth(1)
        cbar.ax.tick_params(which='major',width=1,length=3,direction='out',labelsize=9)
        cbar.set_label('Earthquake magnitude',fontsize=9,labelpad=5)
    
        return plt
    
    def Interpolation_extended(self):
        lats, lons, data = self.input_validate()
        #print("data = ", data)
        data_len = len(data)
        # Interpolation by kriging equation system
        OK = OrdinaryKriging(
            lons,
            lats,      
            data, 
            variogram_model=self.variogram_model,
            verbose=True,
            enable_plotting=False,
            nlags = data_len
        )

        #plotting
        data_len = len(lats)
        min_lon = 102.1439
        min_lat = 8.5624 
        max_lon = 109.4653
        max_lat = 23.3925
        grid_space = 1
        
        grid_lon = np.arange(min_lon, max_lon + 1, grid_space) 
        grid_lat = np.arange(min_lat, max_lat + 1, grid_space)
        z_value, variance = OK.execute('grid', grid_lon, grid_lat)
        # Z-values of specified grid or at the specified set of points.
        # Variance at specified grid points or at the specified set of points.
        #print ("z-values = ", z_value)
        #print ("variance = ", variance)

        xintrp, yintrp = np.meshgrid(grid_lon, grid_lat)
        fig, ax = plt.subplots(figsize=(25, 15))

        # set basemap for background plotting
        m= Basemap(projection= 'merc', llcrnrlat= min_lat, urcrnrlat= max_lat,
                    llcrnrlon= min_lon, urcrnrlon= max_lon, resolution='h', ax =ax)
        # đường bờ biển
        m.drawcoastlines()
        # đường biên giới
        m.drawmapboundary(color='k', fill_color=None, zorder=-1)
        # Bổ sung đường biên giới của Việt Nam bằng màu đỏ dựa trên long lat
        m.drawcountries(linewidth=1, linestyle='solid', color='k')
        # vĩ tuyến
        parallels = np.arange(int(min_lat), max_lat, 1)
        m.drawparallels(parallels, labels= [1, 1, 0, 0], fontsize=6, color='gray')
        #kinh tuyến
        meridians = np.arange(int(min_lon), max_lon, 2)
        m.drawmeridians(meridians, labels=[0,0,0,1], fontsize=6, color='gray')
        x,y=m(xintrp, yintrp) # convert the coordinates into the map scales
        
        #phủ màu
        cs = m.contourf(x,y,z_value,alpha=0.95,extend='both')
        cbar= m.colorbar(cs, pad=0.075, shrink=0.15, aspect=5, location='bottom')
        cbar.outline.set_linewidth(0.5)
        cbar.ax.tick_params(which='major',width=1,length=2,direction='out',labelsize=6)
        cbar.set_label('Earthquake magnitude',fontsize=6,labelpad=3)
        
        return plt


