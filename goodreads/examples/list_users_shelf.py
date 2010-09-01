import sys
sys.path.append('../..')

from goodreads import GoodReadsClient
from secrets import KEY, SECRET

# I get this values from a previous login
token = "uRkhGCTlUpU4a2rS1o4sA"
token_secret = "y61GDMyE5FKfjyqtjCiPtxvhDH34tbanzBZoDvHr0"
# I went to this link and click on "Allow access" with my goodreads account
# http://www.goodreads.com/oauth/authorize/?oauth_token=cbFmWa2r8dLPhut33DGXJA

goodreads = GoodReadsClient(KEY, SECRET, token, token_secret)
response, content = goodreads.users_shelf('humitos')
import ipdb;ipdb.set_trace()
