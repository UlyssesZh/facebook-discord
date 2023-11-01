#!/usr/bin/env python3

from facebook_scraper import *
from facebook_scraper import _scraper
import discord

import pickle
import os
import logging

import config
import time

def use_persistent_session(email, password, cookies_file_path):
	try:
		if os.path.getmtime(cookies_file_path) + config.cookies_timeout < time.time():
			cookies = None
			logger.debug("Cookies file expired %s", cookies_file_path)
		else:
			with open(cookies_file_path, "rb") as f:
				cookies = pickle.load(f)
				logger.debug("Loaded cookies from %s", cookies_file_path)
	except FileNotFoundError:
		logger.error("No cookies file found at %s", cookies_file_path)
		cookies = None
	try:
		if not cookies:
			raise exceptions.InvalidCookies()
		set_cookies(cookies)
		logger.debug("Successfully logged in with cookies")
	except exceptions.InvalidCookies:
		logger.exception("Invalid cookies, trying to login with credentials")
		_scraper.login(email, password)
		cookies = _scraper.session.cookies
		with open(cookies_file_path, "wb") as f:
			pickle.dump(cookies, f)
		set_cookies(cookies)
		logger.debug("Successfully logged in with credentials")

use_persistent_session(config.facebook_email, config.facebook_password, config.cookies_file_path)

facebook_user = get_profile(config.scrape_name)

try:
	with open(config.posts_list_path, "r") as f:
		recorded_posts = set(f.read().splitlines())
except FileNotFoundError:
	recorded_posts = set()
new_posts = []
for post in get_posts(config.scrape_name, pages=3):
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
	return discord.Embed.from_dict({
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
			"icon_url": facebook_user['profile_picture']
		}
	})

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
@client.event
async def on_ready():
	channel = client.get_channel(config.channel_id)
	with open(config.posts_list_path, "a") as f:
		for post in reversed(new_posts):
			await channel.send(embed = embed_post(post))
			f.write(post['post_id'] + '\n')
	await client.close()
client.run(config.discord_token)
