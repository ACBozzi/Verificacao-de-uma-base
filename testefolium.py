import base64
from resizeimage import resizeimage
from PIL import Image
import os, glob
import folium
from folium import plugins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('location.csv')
df.head()

m = folium.Map(location = [-15.7801, -49.9982117], zoom_start=5)

for index, row in df.iterrows():
	folium.Marker([row['Latitude'], row['Longitude']], popup=row['Local'], icon=folium.Icon(icon='flag')).add_to(m)
m.save('prototipo.html')


#home = '/home/carol/Área de Trabalho/IC'
#
#lista = []
#
#if os.path.isdir(home): #VERIFICA SE O CAMINHO PASSADO EXISTE
#		os.chdir(home) #ABRE CASO EXISTA
#		for file in glob.glob('*.jpg'): #CRIA A LISTA DOS ARQUIVOS DADO PARAMETRO 
#			if file.lower().endswith(('.jpg')):
#				with open(file, 'r+b') as f:
#					with Image.open(f) as image:
#						cover = resizeimage.resize_cover(image, [300, 200])
#						cover.save(file, image.format)			
#						m = folium.Map(location = [-25.4213059, -49.9982117])
#						encoded = base64.b64encode(open(file, 'rb').read()).decode()
#						html = '<img src="data:image/jpeg;base64,{}">'.format
#						iframe = folium.IFrame(html(encoded), width=350, height=250)
#						popup = folium.Popup(iframe, max_width=700)
#						folium.Marker([-25.4213059, -49.9982117], popup=popup).add_to(m)
#m.save("test.html")