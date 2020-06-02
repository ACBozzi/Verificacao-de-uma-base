import os, glob
import time

#CONVERTE O TXT PARA LISTA DE CIDADES
#arq = open("deolho.txt","r")
#lines = arq.readlines()
#
listaNome = []
#
#for line in lines:
#	listaNome.append(line.strip())
#
#
home = '/home/carol/Área de Trabalho/IC/deolhonoscorais'

if os.path.isdir(home): #se existe
	os.chdir(home) #então abre
	for file in glob.glob('*'): #criar listas de arquivos a partir de buscas em diretórios
		listaNome.append(file)

home = '/home/carol/Área de Trabalho/IC/#deolhonoscorais'

arquivo = open("excluidos.txt", "w")


if os.path.isdir(home): #se existe
	os.chdir(home) #então abre
	for file in glob.glob('*'): #criar listas de arquivos a partir de buscas em diretórios
		for nome in listaNome:
			if file == nome:
				print('Removendo:',file)
				arquivo.write(file)
				arquivo.write("\n")
				os.remove(file)

			