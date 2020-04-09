arq = open("teste.txt","r")
lines = arq.readlines()
arq.close()

arq = open("teste.txt","w")


for line in lines:
	if "exists" in line:
		print('')
	else:
		arq.write(line)

arq.close()