import random
import logging

logging.basicConfig(filename='main.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

facebook_email = 'email@example.com'
facebook_password = 'password'
cookies_file_path = 'cookies.pckl'
cookies_timeout = 86400 * random.randrange(20, 40)
cookies_timeout_path = 'cookies_timeout.date'
wait_time = 300 * random.random()
scrape_name = 'LyricaGame'
posts_list_path = 'posts_list.txt'
discord_token = 'DISCORD_TOKEN'
channel_id = 11082004790208848
