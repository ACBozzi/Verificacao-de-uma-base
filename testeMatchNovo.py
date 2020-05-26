import shutil
import os, glob
import pandas as pd
import numpy as np
import re
from pathlib import Path



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



#FORMATA A GEOLOCALIZAÇÃO PARA PROCURAR NO BANCO
def formatGeoLocation(file):

	listageoloc = []
	listageoloc1 = []
	geoloc = open(file,"r")
	lines = geoloc.readlines()
	if len(lines) > 0:	#verifica se o txt não ta vazio 
		line = lines.pop(0)	#remove o link do google maps
		listageoloc1.append(line.strip('\n'))	#adiciona a lista e remove o \n 
		for elemento in listageoloc1:	#percorre a lista para separar cidade/estado/localidade
			for caracter in elemento:
				if caracter == '“':
					listageoloc1= elemento.lower().split('“')
				elif caracter == '-':
					listageoloc1= elemento.lower().split('-')
				elif caracter == ',':
					listageoloc1= elemento.lower().split(',')
	
	for elemento in listageoloc1:
		listageoloc.append(elemento.strip().lower())

	#retorna uma lista com a localização
	return listageoloc	

def PrintCidadaeEstadoLocal(banco, indice, grau):
	
	if grau == 3:
		estado = banco.loc[indice,'Estado']
		print('Estado:', estado,)
	if grau == 2:
		estado = banco.loc[indice,'Estado']
		cidade = banco.loc[indice,'Cidade']
		print('Estado:', estado,'Cidade:',cidade,)
	if grau == 1:
		cidade = banco.loc[indice,'Cidade']
		estado = banco.loc[indice,'Estado']
		localidade = banco.loc[indice,'Localidade']
		print('Estado:', estado,'Cidade:',cidade, 'Localidade:',localidade)
		

#RECEBE A GEOLOCALIZAÇÃO E O INDICE DO MATCH DA LEGENDA
def findMatchGeoloc(indice,banco,listageoloc):
		
	estado = banco.loc[indice,'Estado']
	cidade = banco.loc[indice,'Cidade']
	localidade = banco.loc[indice,'Localidade']
	for elemento in listageoloc:
		if localidade == elemento.lower():
			return 1 	#se o match for zero é pq encontrou a localidade ja
		if elemento.lower() == cidade:
			return 2
		elif elemento.lower() == estado:
			return 3

	return 0 
					
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
	
#FUNÇÃO QUE RETORNA A GEOLOCALIZAÇÃO CORRESPONDENTE A LEEGENDA
def findFileLocation(name,diretorio):

	if os.path.isdir(diretorio): #VERIFICA SE O CAMINHO DADO EXISTE
			os.chdir(diretorio) #ABRE CASO EXISTA
			for location in glob.glob('*_location.txt'): #CRIA A LISTA DOS ARQUIVOS DADO PARAMETRO 
				loc = location.split('_UTC')[0]
				if name == loc:
					return location


#NÃO ESTA SENDO USADA
#FUNÇÃO QUE DADA A LOCALIZAÇÃO PROCURA INDICE NO BANCO
def findLocation(local, indice, banco):

	matchLocalidade = 0
	matchCidade = 0
	matchEstado = 0

	tags = banco.loc[indice,'Localidade']
	for elemento in local:
		if tags == elemento:
			matchLocalidade =  1

	tags = banco.loc[indice,'Cidade']
	for elemento in local:
			if tags == elemento:
				matchCidade = 1 

	tags = banco.loc[indice,'Estado']
	for elemento in local:
		if tags == elemento:
			matchEstado =  1
 
	if matchCidade == 1 or matchEstado == 1:
		return 1
	else:
		return 0
	
def procuraArqs(name,diretorio,pasta):

	if os.path.isdir(diretorio): #VERIFICA SE O CAMINHO DADO EXISTE
			os.chdir(diretorio) #ABRE CASO EXISTA
			for location in glob.glob('*_location.txt'): #CRIA A LISTA DOS ARQUIVOS DADO PARAMETRO 
				loc = location.split('_location')[0]
				if name == loc:
					shutil.move(location, pasta)

			for picture in glob.glob('*.jpg'): #CRIA A LISTA DOS ARQUIVOS DADO PARAMETRO 
				pic = picture.split('_UTC')[0]
				if name == pic:
					shutil.move(picture, pasta)
	

if __name__ == '__main__':


	percentMatch = 0
	percentN = 0
	total = 0
	vazia = 0
	perceExiste = 0
	semlegenda = 0
	#CARREGA A PLANILHA
	banco = pd.read_csv("banco.csv")

	#CAMINHO DA PASTA DAS FOTOS E DADOS
	home = '/home/carol/Área de Trabalho/IC/#deolhonoscorais'

	#CAMINHO DA PASTA QUE NÃO IDENTIFICOU A LOCALIZAÇÃO PELO COMENTÁRIO
	NaoIdentLoc = '/home/carol/Área de Trabalho/IC/#deolhonoscorais/NaoIdentLoc'
	os.mkdir(NaoIdentLoc)
	
	#CAMINHO DA PASTA DAS POSTAGENS DA PASTA DO DE OLHO NOS CORAIS
	PagDeOlho = '/home/carol/Área de Trabalho/IC/#deolhonoscorais/PagDeOlho'
	os.mkdir(PagDeOlho)

	if os.path.isdir(home): #VERIFICA SE O CAMINHO PASSADO EXISTE
			os.chdir(home) #ABRE CASO EXISTA
			for file in glob.glob('*_UTC.txt'): #CRIA A LISTA DOS ARQUIVOS DADO PARAMETRO 
				if file.lower().endswith(('.txt')):
					legendaTxt =  formatLegend(file)	#CHAMA A FUNÇÃO PARA FORMATAR A LEGENDA
					indice = findMatchLegend(banco,legendaTxt)	#CHAMA A FUNÇÃO QUE VERIFICA A LOCALIZAÇÃO
					if indice == 110:		#fotos da página do de olho nos corais
						name = file.split('_UTC')[0]
						shutil.move(file,PagDeOlho)
						procuraArqs(name, home, PagDeOlho)
					else:
						if indice != -1:	#!= pq não é da pág e encontrou um match	
							name = file.split('_UTC')[0]
							file_location = findFileLocation(name, home)
							if file_location:	#se exixste a geolocalização
								listageoloc = formatGeoLocation(file_location)
								if listageoloc:
									find = findMatchGeoloc(indice, banco, listageoloc)
									if find != 0:	#SE FOR MAIOR QUE ZERO É PQ DEU MATCH
										percentMatch += 1
										total +=1
										print("DEU")
										#print('GEOLOC:',file_location, 'Conteúdo:',listageoloc)
										#print('LEGENDA:',file )
										#PrintCidadaeEstadoLocal(banco, indice, find)
										#print('\n')
									else:	#não deu match de geolocalização com legenda
										percentN += 1
										total += 1
										print('NÃO DEU')
										#print('Não bateu legenda com geolocalização')
										#print('GEOLOC:',file_location, 'Conteúdo:',listageoloc)
										#print('LEGENDA:',file)
										#PrintCidadaeEstadoLocal(banco, indice, 1)
										#print('\n')
								else:
									print('VAZIO')
									vazia += 1
									total += 1
									#print('FILE',file, 'file_location', listageoloc)
									#print('Geolocalização vazia')
									#print('\n')
							else:
								perceExiste +=1
								total += 1
								#print('SEM GEOL')
								#print('Não existe a geolocalização')
								#print('LEGENDA:',file, 'Legenda:', legendaTxt)
								#PrintCidadaeEstadoLocal(banco, indice, 1)
								#print('\n')
								#PrintCidadaeEstadoLocal(banco, indice, 1)
						else: 
							print('SABE DEUS')
							#print(file,':Não foi possível encontrar match')
							procuraArqs(name, home,NaoIdentLoc)
							name = file.split('_UTC')[0]
							shutil.move(file, NaoIdentLoc)
							

	print("Total encontrado foi:", total)
	print("Qtd de legendas que bateram com geolocalização foi:",percentMatch, (percentMatch/total),"%")
	print("Qtd que não deu match entre geolocalização e legenda foi:", percentN, (percentN/total),'%')
	print("Qtd de fotos que não tem geolocalização:", perceExiste, (perceExiste/total),'%')
