import os
os.environ['PROJ_LIB'] = 'C:/Users/bune1/Anaconda3/pkgs/proj4-5.2.0-ha925a31_1/Library/share'

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


map = Basemap()

map.drawcoastlines()

plt.show()
plt.savefig('test.png')