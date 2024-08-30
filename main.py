#!/usr/bin/env python3

from facebook_scraper import *
from facebook_scraper import _scraper
import requests

import logging
import time
import json
import os
import sys

sys.path.append(os.getcwd())
import config

logger.debug("Sleep for %f seconds", config.wait_time)
time.sleep(config.wait_time)

try:
	with open(config.mbasic_headers_path, 'r') as f:
		_scraper.mbasic_headers = headers = json.load(f)
	options = {
		'base_url': 'https://mbasic.facebook.com',
		'start_url': f'https://mbasic.facebook.com/{config.scrape_name}?v=timeline',
		'cookies': dict([s.split('=') for s in headers['cookie'].split('; ')])
	}
except FileNotFoundError:
	options = {}

facebook_user = get_page_info(config.scrape_name, **options)
try:
	with open(config.posts_list_path, "r") as f:
		recorded_posts = set(f.read().splitlines())
except FileNotFoundError:
	recorded_posts = set()
new_posts = []
for post in get_posts(config.scrape_name, pages=3, **options):
	if post['post_id'] in recorded_posts:
		break
	logging.info("New post found: " + post['post_url'])
	new_posts.append(post)

if len(new_posts) == 0:
	logging.info("No new posts found")
	sys.exit(0)

with open(config.posts_list_path, "a") as f:
	for post in reversed(new_posts):
		requests.post(config.webhook_url, json={'content': post['post_url']})
		f.write(post['post_id'] + '\n')
