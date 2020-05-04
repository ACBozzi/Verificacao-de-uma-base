import os, glob
import time

#CONVERTE O TXT PARA LISTA DE CIDADES
arq = open("listaCidadesPraia.txt","r")
lines = arq.readlines()

listaPraias = []

for line in lines:
	listaPraias.append(line.strip()) #adiciona line e remove /n
#print(listaPraias)

##LISTA DAS GEOLOCALIZAÇÕES
listaLocal = []

home = '/home/carol/Área de Trabalho/IC/coraishipes'

if os.path.isdir(home): #se existe
		os.chdir(home) #então abre
		for file in glob.glob('*.txt'): #criar listas de arquivos a partir de buscas em diretórios
			if file.lower().endswith(('.txt')):
				txt = open(file, "r")
				lines = txt.readlines()
				line = lines.pop(0)
				listaLocal.append(line.strip())
#print(listaLocal)
lista_tem = []
listaNtem = []
tem = 0
for local in listaLocal:
	tem = 0
	for praia in listaPraias:
		if praia == local.upper():
			lista_tem.append(local)
			tem = 1
	if tem == 0:
		listaNtem.append(local)

print("Lista dos que achou igual", lista_tem)
print("Lista dos que não achou igual", listaNtem)

			
