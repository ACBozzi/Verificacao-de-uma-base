
from selenium import webdriver #abrir navegador
from selenium.webdriver.common.keys import Keys #simula teclas do teclado
import time immport
import random
import os


class InstagramBot:
	def __init__ (self,username, password):
		self.username = username
		self.password = password
		self.driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")


	def login(self):
		driver = self.driver
		driver.get("https://www.instagram.com ")
		
		#tempo de carregar a página
		time.sleep(3)

		#clicar no campo usuario e digitar login
		campo_usuario = driver.find_element_by_xpath("//input[@name='username']")	#inspesionando a tela pra pegar a tag do user
		campo_usuario.click()	#simula um click no campo
		campo_usuario.clear()	#limpa pra garantir
		campo_usuario.send_keys(self.username)	#digita o usuário
		
		#clicar no caampo senha e digitar
		campo_senha = driver.find_element_by_xpath("//input[@name='password']")	#inspesionando a tela pra pegar a tag da senha
		campo_senha.click()	#simula um click
		campo_senha.clear()	#limpa pra garantir
		campo_senha.send_keys(self.password)	#digita a senha
		
		#clicar no botão de entar
		campo_senha.send_keys(Keys.RETURN)	
		time.sleep(5)	#tempo de carregar a página

		self.comentario('deolhonohipesteste')	#chama a função com a #


	@staticmethod
	def digite_como_uma_pessoa(frase, local):
		for letra in frase:
			local.send_keys(letra)
			time.sleep(random.randint(1,5)/30)	#velocidade aleatória


	#função que pesquisa a #
	def comentario(self,hashtag):
		driver = self.driver

		#URL da respectiva #
		driver.get("https://www.instagram.com/explore/tags/"+ hashtag +"/")
		time.sleep(3)	#tempo de carregar a página

		#carrega mais fotos, tres scroll na tela
		for i in range(1,3):
			driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
			time.sleep(5)	#tempo de carregar a página

		#pegas as hrefs
		hrefs = driver.find_elements_by_tag_name('a')
		pic_hrefs = [elem.get_attribute('href') for elem in hrefs]	#lista com os atributos que precisa
		#filtra
		[href for href in pic_hrefs if hashtag in href]
		print(hashtag + 'fotos ' + str(len(pic_hrefs)))	#printa quantas referencias conseguiu encontrar

		#abrir as fotos 
		for pic_hrefs in pic_hrefs:
			driver.get(pic_hrefs)
			driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')

			#clicar no campo comentario
			try:
				#lista de comentarios
				comentarios = ["teste", "comentario", "nota 10"]
				time.sleep(3)
				driver.find_element_by_xpath("//button[contains(text()), 'Publicar')]").click()
				campo_comentario = driver.find_element_by_class_name("Ypffh")
				time.sleep(random.randint(2,5))	#espera de 2 a 5 seg entre uma ação e outra
				self.digite_como_uma_pessoa(random.choice(comentarios),campo_comentario)
				time.sleep(random.randint(30,40))

				#clicar botão publicar
				driver.find_element_by_xpath("//button[contains(text()), 'Publicar')]").click()
				time.sleep(5)
			except Exception as e:
				print(e)
				time.sleep(5)


#login e senha para entrar
teste = InstagramBot('coraishipes', 'deolhonoscorais2020')
teste.login()
