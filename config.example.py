import random
import logging
import requests

logging.basicConfig(filename='main.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

mbasic_headers_path = 'mbasic_headers.json'
wait_time = 300 * random.random()
scrape_name = 'LyricaGame'
posts_list_path = 'posts_list.txt'
webhook_url = 'https://discord.com/api/webhooks/11082004790208848/SOME_SECRET'

def login_required(e):
	requests.post(
		"https://ntfy.sh/facebook-discord",
		data="Cookies expired. Please provide new mbasic headers.",
		headers={
			"Title": "Facebook Discord cookies expired",
			"Priority": "high"
		}
	)
