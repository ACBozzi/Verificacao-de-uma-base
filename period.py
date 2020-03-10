#rodar com python3

from datetime import datetime
from itertools import dropwhile , takewhile
from datetime import date
import instaloader


#pega a instancia do instaloader
L = instaloader . Instaloader ()

posts = L . get_hashtag_posts ( 'deolhonoscorais' )
desde = datetime ( 2018 , 1 , 2 )	#data maior
ate = datetime ( 2017 , 1 , 1 )	#data menor


#lambda usa para 'variável' desconhecida
#takewhile itera desde que o predicado seja verdadeiro
#dropwhile elimina do iterável desde que o predicado seja verdadeiro
for post in takewhile ( lambda p : p . date > ate , dropwhile ( lambda p : p . date > desde , posts )):
   	print ( post . date )
   	L . download_post ( post , '#deolhonoscorais' )

