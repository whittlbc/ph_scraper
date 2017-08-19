import os
from ph_py import ProductHuntClient
from time import sleep
import redis

r = redis.StrictRedis.from_url(os.environ.get('REDIS_URL'))

client_id = os.environ.get('PH_CLIENT_ID')
client_secret = os.environ.get('PH_CLIENT_SECRET')
redirect_uri = 'http://localhost:3000/ph/oauth'
dev_token = os.environ.get('PH_DEV_TOKEN')

ph = ProductHuntClient(client_id, client_secret, redirect_uri, dev_token)
ph_lifetime = 1274  # days

for i in range(ph_lifetime):
  try:
    # Get redirect_urls for each post for that day
    urls = [p.redirect_url for p in ph.get_previous_days_posts(i) if p and p.redirect_url]
    
    # Convert list of urls into hash
    url_hash = {u: '0' for u in urls}
    
    # Store these in redis
    r.hmset('ph_urls', url_hash)
    
    # Sleep just in case of API rate limit
    sleep(0.5)

    if (i + 1) % 50 == 0:
      print 'Days of posts fetched: {}'.format(i + 1)
      
  except BaseException:
    print 'Error fetching urls for previous day {}'.format(i)