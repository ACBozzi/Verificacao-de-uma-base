import os, glob
import pandas as pd
import numpy as np
import re


#teste = banco.loc[0, 'Tag de praias']
#texto = teste.split('\n')
#
#tem = 0
#
#for palavra in texto:
#	if palavra == '#alagoas':
#		tem =+1
#
#print(tem)

def formataComentarios(file):
	comentariosTxt = []
	txt = open(file,"r")
	lines = txt.readlines()
	for line in lines:
		linha = line.split(' ')
		for elemento in linha:
			comentariosTxt.append(elemento) #adiciona line e remove /n

	return comentariosTxt

def PrintCidadaeEstado(banco, indice):
	estado = banco.loc[indice,'Estado']
	cidade = banco.loc[indice,'Cidade']
	print('Estado:', estado,'Cidade:',cidade)


#def geoloOUcomentario():
#	#SE COMENTARIO CHAMA A FORMATACOMENTARIOS
#	#SENÃO CHAMA A GEOLOCALIZAÇÃO

def procuraMatch(banco,comentariosTxt):
	indice = 0
	maior = 0

	for i in banco.index:
		tags = banco.loc[i,'Tag de praias']
		tag = tags.split('\n')
		match = 0
		for nome in tag:
			for palavra in comentariosTxt:
				if nome == palavra:
					match = + 1
		if match > maior:
			maior = match
			indice = i

	return indice
	
if __name__ == '__main__':

	#CARREGA A PLANILHA
	banco = pd.read_csv("banco.csv")

	#CAMINHO DA PASTA DAS FOTOS E DADOS
	home = '/home/carol/Área de Trabalho/IC/teste'


	if os.path.isdir(home): #VERIFICA SE O CAMINHO DADO EXISTE
			os.chdir(home) #ABRE CASO EXISTA
			for file in glob.glob('*.txt'): #CRIA A LISTA DOS ARQUIVOS DADO PARAMETRO 
				if file.lower().endswith(('.txt')):
					comentariosTxt =  formataComentarios(file)	#CHAMA A FUNÇÃO PARA FORMATAR OS COMENTÁRIOS
					indice = procuraMatch(banco,comentariosTxt)	#CHAMA A FUNÇÃO QUE VERIFICA A LOCALIZAÇÃO
					print(file,':')
					PrintCidadaeEstado(banco, indice)