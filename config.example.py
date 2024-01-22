import random
import logging

logging.basicConfig(filename='main.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

mbasic_headers_path = 'mbasic_headers.json'
wait_time = 300 * random.random()
scrape_name = 'LyricaGame'
posts_list_path = 'posts_list.txt'
discord_token = 'DISCORD_TOKEN'
channel_id = 11082004790208848
