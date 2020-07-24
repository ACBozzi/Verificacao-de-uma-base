import pandas as pd
import json
import numpy as np
import lzma
import os , glob
import csv
from unicodedata import normalize #usada para remover acentos

def find_Foto(file,diretorio):

	name =  file.split('_UTC')[0]
	fotos = []	#é uma lista pq pode ter mais de uma foto

	if os.path.isdir(diretorio):
		os.chdir(diretorio)
		for picture in glob.glob('*.jpg'): #CRIA A LISTA DOS ARQUIVOS DADO PARAMETRO 
			pic = picture.split('_UTC')[0]
			if name == pic:
				fotos.append(picture)

	return fotos	


#PROCURA NO BANCO A LEGENDA
#def findMatchLegend(banco,legendaTxt):
#	
#	indice = -1
#	maior = 0
#	lista = []
#	ehlista = 0
#
#	for i in banco.index:	#navega pelas linhas do banco na coluna de tags
#		tags = banco.loc[i,'Tag de praias']
#		tag = tags.split('\n')	#separa as tags do banco por \n
#		match = 0
#		for hashtag in tag:	#percorre as hashtags
#			for palavra in legendaTxt:	#percorre a legenda
#				if hashtag == palavra:
#					match +=  1
#			if i != 110:
#				if match > maior:
#					ehlista = 0
#					maior = match
#					indice = i
#				elif match == maior:
#					ehlista = 1
#					lista.append(indice)
#					indice = i
#			else:
#				if maior == 0:
#					maior = match
#					indice = i	
#				else:
#					return indice
#	if ehlista == 1 :
#		lista.append(indice)
#		return lista
#
#	else:
#		return indice

def findMatchLegend(banco,legendaTxt):
	
	indice = -1
	maior = 0

	for i in banco.index:	#navega pelas linhas do banco na coluna de tags
		tags = banco.loc[i,'Tag de praias']
		tag = tags.split('\n')	#separa as tags do banco por \n
		match = 0
		for hashtag in tag:	#percorre as hashtags
			for palavra in legendaTxt:	#percorre a legenda
				if hashtag == palavra:
					match +=  1
			if i != 110:
				if match > maior:
					maior = match
					indice = i
			else:
				if maior == 0:
					maior = match
					indice = i	
				else:
					return indice

	return indice
	

#FORMATA A LEGENDA PARA PROCURAR NO BANCO 
def formatLegend(file):

	legendaTxt = []
	txt = open(file,"r")
	lines = txt.readlines()
	for line in lines:
		linha = line.split(' ')
		for elementos in linha:
			elemento = elementos.lower()	#minuscula
			legendaTxt.append(elemento.strip()) #adiciona line e remove /n

	return legendaTxt

#PROCURA OS ARQUIVOS DADO UM NOME PASSADO COMO PARÂMETRO	
def procuraArqs(name,diretorio):

	if os.path.isdir(diretorio): #VERIFICA SE O CAMINHO DADO EXISTE
			os.chdir(diretorio) #ABRE CASO EXISTA
			for file in glob.glob('*UTC.txt'): #CRIA A LISTA DOS ARQUIVOS DADO PARAMETRO 
				loc = file.split('_UTC')[0]
				if name == loc:
					return file

def findLatLng(local,municipios):

	latlng = []
	localidade = normalize('NFKD', local).encode('ASCII', 'ignore').decode('ASCII')# remove acento

	for i in municipios.index:	#navega pelas linhas do municipios na coluna de tags
		cidades = municipios.loc[i,'nome']
		cidade = cidades.lower() #minúscula
		city = normalize('NFKD', cidade).encode('ASCII', 'ignore').decode('ASCII')
		if city == localidade:
			latlng.append(municipios.loc[i,'latitude'])
			latlng.append(municipios.loc[i,'longitude'])
			return latlng

	return 0
		

if __name__ == '__main__':

	#CAMINHO DA PASTA DAS FOTOS E DADOS
	home = '/home/carol/Área de Trabalho/IC/#deolhonoscorais'

	#Cria o CSV que vai receber os dados do Json
	csvF = open("location.csv", 'a+')
	csvfile = csv.writer(csvF)
	csvfile.writerow(["Foto","Latitude","Longitude","Local"])

	#BANCO DA HASHTAGS
	banco = pd.read_csv("banco.csv")
	fotos = []

	#LISTA DE MUNICIPIOS E COORDENADAS IBGE	
	municipios = pd.read_csv("municipios.csv")

	#Percorrer a pasta e ler cada Json baixado no instaloader
	if os.path.isdir(home): #VERIFICA SE O CAMINHO PASSADO EXISTE
		os.chdir(home) #ABRE CASO EXISTA
		for file in glob.glob('*.xz'): #CRIA A LISTA DOS ARQUIVOS DADO PARAMETRO 
			if file.lower().endswith(('.xz')):				
				dados = lzma.open(file) #abriu
				jdados = json.load(dados) #lendo json É UM DICIONARIO/lista
				if jdados['node']['location']:	#TEMOS A GEOLOCALIZAÇÃO
					lat = jdados['node']['location']['lat']
					lng = jdados['node']['location']['lng'] 
					local = jdados['node']['location']['name']
					fotos = find_Foto(file,home)
					foto = ' '.join(map(str,fotos)).strip('[]')
					csvfile.writerow([foto,lat,lng,local])
				else:	#NÃO TEMOS A GEOLOCALIZAÇÃO PROCURAR NA LEGENDA DA FOTO
					name = file.split('_UTC')[0]
					file_legenda = procuraArqs(name, home)
					legendaTxt =  formatLegend(file_legenda)	#CHAMA A FUNÇÃO PARA FORMATAR A LEGENDA
					indice = findMatchLegend(banco,legendaTxt)	#CHAMA A FUNÇÃO QUE VERIFICA A LOCALIZAÇÃO
					fotos = find_Foto(file,home)
					foto = ' '.join(map(str,fotos)).strip('[]')
					if indice == -1: 	# É PQ NÃO ENCOONTROU
						csvfile.writerow([foto,'','',''])
					else:
						local = banco.loc[indice,'Cidade']
						latlng = findLatLng(local,municipios)
						if latlng != 0:
							csvfile.writerow([foto,latlng[0],latlng[1],local])
						else:
							csvfile.writerow([foto,'','',local])
