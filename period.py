from datetime import datetime
from itertools import dropwhile , takewhile

import instaloader

#pega a instancia do instaloader
L = instaloader . Instaloader ()

posts = L . get_hashtag_posts ( 'deolhonoscorais' )

desde = datetime ( 2019 , 12 , 1 )	#data maior
ate = datetime ( 2018 , 5 , 1 )	#data menor

#lambda usa para 'variável' desconhecida
#takewhile itera desde que o predicado seja verdadeiro
#dropwhile elimina do iterável desde que o predicado seja verdadeiro
for post in takewhile ( lambda p : p . date > ate , dropwhile ( lambda p : p . date > desde , posts )):
    print ( post . date )
    L . download_post ( post , '#deolhonoscorais' )

