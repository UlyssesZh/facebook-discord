import random
import logging

logging.basicConfig(filename='main.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

mbasic_headers_path = 'mbasic_headers.json'
wait_time = 300 * random.random()
scrape_name = 'LyricaGame'
posts_list_path = 'posts_list.txt'
webhook_url = 'https://discord.com/api/webhooks/11082004790208848/SOME_SECRET'
