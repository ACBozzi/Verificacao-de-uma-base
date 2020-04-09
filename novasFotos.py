arq = open("teste.txt","r")
lines = arq.readlines()
arq.close()

arq = open("teste.txt","w")
primeira = 1

for line in lines:
	if primeira!=1:	#o instaloader printa uma primeira linha avisando que esta realizando o dowload das fotos
		if "exists" in line:
			print('')
		else:
			arq.write(line)
	primeira+=1

arq = open("teste.txt","r")
lines = arq.readlines()
arq.close()

arq = open("teste.txt","w")
primeira = 1

#instaloader printa as duas ultimas linhas com informações de encerramento
for line in lines:
	if primeira !=(len(lines)) and primeira != (len(lines)-1):
		lista = line.split("/")[1] 	#separar apenas o nome
		arq.write(lista)
	primeira+=1

arq.close()