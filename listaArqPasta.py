import os, glob
import time

home = '/home/carol/Área de Trabalho/IC/#deolhonoscorais'


arquivo = open("listaArquivos#.txt", "w")

if os.path.isdir(home): #se existe
	os.chdir(home) #então abre
	for file in glob.glob('*'): #criar listas de arquivos a partir de buscas em diretórios
		arquivo.write(file)
		arquivo.write("\n")

		