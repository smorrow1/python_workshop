#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import datashader as ds
from pyproj import Proj, transform
from datashader.utils import lnglat_to_meters as webm
from functools import partial 
from datashader.utils import export_image
from datashader.colors import colormap_select, Greys9
from IPython.core.display import HTML, display
import datashader.transfer_functions as tf


# In[2]:


df = pd.read_csv("/Users/morrow/Documents/Baumkataster_Visualisierung/Baum.csv", sep=";" , decimal=".")

df['Gattung'] = df['Gattung/Art/Deutscher Name'].str.split(',').str[0]
df['Deutscher Name'] = df['Gattung/Art/Deutscher Name'].str.split(',').str[1]
df['HOCHWERT'] = (df['HOCHWERT'].replace('\,','.', regex=True).astype(float))
df['RECHTSWERT'] = (df['RECHTSWERT'].replace('\,','.', regex=True).astype(float))
df['Kronendurchmesser'] = df['Kronendurchmesser'].replace('\,','.', regex=True).astype(float)
df.head()


# In[3]:


df.drop(columns=['Gattung/Art/Deutscher Name'])


# In[ ]:





# In[18]:


#utm15_wgs84 = Proj(init='epsg:32632', proj='utm',zone=10,ellps='WGS84', preserve_units=False)
utm15_wgs84 = Proj(init='epsg:5243', proj='utm', zone='32N', ellps="GRS80")
df[['lon', 'lat']] = df.apply(lambda row:utm15_wgs84(row['RECHTSWERT'], row['HOCHWERT'], inverse=True), axis=1).apply(pd.Series)


# In[5]:


y_range_min = df['lat'].quantile(0.01)
y_range_max = df['lat'].quantile(0.99)
x_range_min = df['lon'].quantile(0.01)
x_range_max = df['lon'].quantile(0.99)


# In[6]:


df.head()
df.drop(columns=['Gattung/Art/Deutscher Name'])
df['Kronendurchmesser'].unique()
np.sort(df['Kronendurchmesser'])


# In[8]:


bins = [0,2,4,6,10,15,20,30,50]
labels = ['mini', 'klein', 'klein_2', 'mittel', 'mittel_2', 'mittel_3', 'groß', 'groß_2']
df['diskret_kronendurchmesser'] = pd.cut(df.Kronendurchmesser, bins=bins, labels=labels)
df.drop(columns=['Gattung/Art/Deutscher Name'])


# In[7]:


# Alle Bäume, die nach 2000 gepflanzt wurden
df['Pflanzjahr'] = (df['Pflanzjahr'].astype(int))
new_df = df[df['Pflanzjahr'] >= 2000].copy()


# In[8]:


sw = webm(x_range_min, y_range_min)
ne = webm(x_range_max, y_range_max)
FFM = zip(sw, ne)


# In[9]:


# Initialize plot for datashader

plot_width = int(2000)
plot_height = int(2000)
background="black"
export = partial(export_image, background = background, export_path="export")
#cm = partial(colormap_select, reverse=(background!="black"))
cm = partial(colormap_select, reverse=(background!="black"))


display(HTML("<style>.container {width:100%} !important; }</style>"))


# In[10]:


cvs = ds.Canvas(plot_width, plot_height, *FFM)
agg = cvs.points(df, 'RECHTSWERT', 'HOCHWERT')


# In[23]:


# Export image on different styles or conditions
export(tf.shade(agg, cmap = cm(Greys9,0.2), how='log'), "Frankfurt_Baumbestand")


# In[22]:


from colorcet import fire
export(tf.shade(agg, cmap = cm(fire,0.4), how='log'), "Frankfurt_Baumbestand_Fire")


# In[21]:


from colorcet import glasbey
export(tf.shade(agg, cmap = cm(glasbey,0.4), how='eq_hist'), "Frankfurt_Baumbestand_Glasbey")


# In[15]:


from colorcet import glasbey
cvs = ds.Canvas(plot_width, plot_height, *FFM)
agg = cvs.points(df, 'RECHTSWERT', 'HOCHWERT', ds.count_cat('diskret_kronendurchmesser'))
export(tf.shade(agg, cmap = cm(glasbey,0.4)), "Frankfurt_Baumbestand_Category")


# In[16]:


legend_elements = list()

# Create legend for tree size colors 
labels = dict(
  zip(
    [
    'mini', 
    'klein', 
    'klein_2', 
    'mittel', 
    'mittel_2', 
    'mittel_3', 
    'groß', 
    'groß_2'],
  np.arange(8) ) )

for category, category_code in labels.items(): 
    element = Line2D(
    [0],
    [0],    
    marker='o',
    color='k',
    label=category,
    markerfacecolor=glasbey[category_code],
    markersize=10)
    
    # append legend entry to list of legend entries
    legend_elements.append(element)

#Create arbitrary plot
fig, ax = plt.subplots()
legend = ax.legend(handles=legend_elements, loc='center')

#Format the legend 
legend.get_frame().set_linewidth(1)
legend.get_frame().set_facecolor('k')
plt.setp(legend.get_texts(), color='w')

# save SVG of legend to file
plt.savefig('legend.png')
plt.close()


# In[ ]:





# In[17]:


from colorcet import fire
y_range_min_new = new_df['lat'].quantile(0.01)
y_range_max_new = new_df['lat'].quantile(0.99)
x_range_min_new = new_df['lon'].quantile(0.01)
x_range_max_new = new_df['lon'].quantile(0.99)

sw_new = webm(x_range_min_new, y_range_min_new)
ne_new = webm(x_range_max_new, y_range_max_new)
FFM_new = zip(sw_new, ne_new)


plot_width = int(2000)
plot_height = int(2000)
background="black"
export = partial(export_image, background = background, export_path="export")
#cm = partial(colormap_select, reverse=(background!="black"))
cm = partial(colormap_select, reverse=(background!="black"))


display(HTML("<style>.container {width:100%} !important; }</style>"))

cvs = ds.Canvas(plot_width, plot_height, *FFM)
agg = cvs.points(new_df, 'RECHTSWERT', 'HOCHWERT')

export(tf.shade(agg, cmap = cm(fire,0.4), how='log'), "Frankfurt_Baumbestand_nach_2000")


# In[17]:


from datashader.utils import lnglat_to_meters
df.loc[:, 'lon'], df.loc[:, 'lat'] = lnglat_to_meters(df.lon,df.lat)


# In[12]:


import holoviews as hv
from holoviews.element.tiles import EsriImagery
from holoviews.operation.datashader import datashade
#from datashader.utils import lnglat_to_meters
hv.extension('bokeh')
from colorcet import fire

#df.loc[:, 'lon'], df.loc[:, 'lat'] = lnglat_to_meters(df.lon,df.lat)
map_tiles  = EsriImagery().opts(alpha=0.5, width=900, height=600, bgcolor='black')
points     = hv.Points(df, ['lon', 'lat'])
baum = datashade(points, x_sampling=1, y_sampling=1, cmap=fire, width=900, height=480)
baum_map = map_tiles * baum

baum_map


# In[12]:


import bokeh
hv.save(baum_map, 'frankfurter_baum.html', backend='bokeh')


# In[24]:





# In[13]:


from keplergl import KeplerGl
import pandas as pd
import geopandas as gpd


# In[22]:


map = KeplerGl(height=800)
map.add_data(data=df, name="test")


# mape = KeplerGl(height=500)

# 

# In[23]:


map


# In[25]:


config = map.config


# In[29]:


map_2 = KeplerGl(height=800, data={"test": df})
map_2


# In[31]:


config_2 = map_2.config
config_2


# In[32]:


map_2.save_to_html(data={"test": df}, config=config_2, file_name="Kepler_Baumkataster_Height.html")


# In[ ]:




