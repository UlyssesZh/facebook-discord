#!/usr/bin/env python3

from facebook_scraper import *
from facebook_scraper import _scraper
import discord

import logging
import time
import json

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

def embed_post(post):
	lines = post['text'].splitlines()
	if len(lines) > 0:
		title = lines[0][:255]
	else:
		title = ""
	embed_data = {
		"title": title,
		"type": "rich",
		"description": post['text'][:4095],
		"url": post['post_url'],
		"timestamp": post['time'].isoformat(),
		"image": {
			"url": post['image']
		},
		"author": {
			"name": post['username'],
			"url": post['user_url'],
			"icon_url": facebook_user.get('profile_picture', None)
		}
	}
	return discord.Embed.from_dict(embed_data)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
@client.event
async def on_ready():
	channel = client.get_channel(config.channel_id)
	with open(config.posts_list_path, "a") as f:
		for post in reversed(new_posts):
			await channel.send(embed=embed_post(post))
			f.write(post['post_id'] + '\n')
	await client.close()
client.run(config.discord_token)
