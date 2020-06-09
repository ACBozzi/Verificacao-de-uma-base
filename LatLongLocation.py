import pandas as pd
import json
import numpy as np
import lzma
import os , glob
import csv

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

def findMatchLegend(banco,legendaTxt):
	
	indice = -1
	maior = 0
	lista = []
	ehlista = 0

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
					ehlista = 0
					maior = match
					indice = i
				elif match == maior:
					ehlista = 1
					lista.append(indice)
					indice = i
			else:
				if maior == 0:
					maior = match
					indice = i	
				else:
					return indice
	if ehlista == 1 :
		lista.append(indice)
		return lista

	else:
		return indice


if __name__ == '__main__':


	#CAMINHO DA PASTA DAS FOTOS E DADOS
	home = '/home/carol/Área de Trabalho/IC/#deolhonoscorais'

	#Cria o CSV que vai receber os dados do Json
	csvF = open("location.csv", 'w')
	csvfile = csv.writer(csvF)
	csvfile.writerow(["Foto","Latitude","Longitude","Local"])

	banco = pd.read_csv("banco.csv")
	fotos = []
	#Percorrer a pasta e ler cada Json
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
					#for file in glob.glob('*_UTC.txt'): #CRIA A LISTA DOS ARQUIVOS DADO PARAMETRO 
					#	if file.lower().endswith(('.txt')):
					#		legendaTxt =  formatLegend(file)
					#		indice = findMatchLegend(banco,legendaTxt)
					#		if type(indice) is list:
					#			#alguma coisa
					#		else:
					#			
					#print(file)
					fotos = find_Foto(file,home)
					#print(fotos)
					#print('não tem localização')

