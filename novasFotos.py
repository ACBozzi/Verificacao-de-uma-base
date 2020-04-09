arq = open("teste.txt","r")
lines = arq.readlines()
arq.close()

arq = open("teste.txt","w")
primeira = 1

for line in lines:
	if primeira!=1 and primeira !=(len(lines)) and primeira != (len(lines)-1):
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

for line in lines:
	if primeira !=(len(lines)) and primeira != (len(lines)-1):
		arq.write(line)
	primeira+=1


arq.close()