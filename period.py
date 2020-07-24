from datetime import datetime
from itertools import dropwhile, takewhile
from datetime import date
import instaloader
import dateutil.relativedelta

L = instaloader.Instaloader()

posts = L.get_hashtag_posts('deolhonoscorais')
SINCE = datetime.now() #data de hoje
UNTIL = SINCE - dateutil.relativedelta.relativedelta(months=4) #um mês antes

for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
    print(post.date)
    L.download_post(post, "#deolhonoscorais")
