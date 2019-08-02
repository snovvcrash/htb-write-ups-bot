#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

BLOG_URL = 'https://0xdf.gitlab.io'


def _get_post_links(blog_url=BLOG_URL):
	resp = requests.get(blog_url)
	soup = BeautifulSoup(resp.text, 'html.parser')
	return soup.find_all('a', {'class': 'post-link'})


def extract_htb_posts():
	post_links = _get_post_links()

	htb_posts = []
	for link in post_links:
		title = link.text.strip()
		url = f"{BLOG_URL}/{link.get('href')}"
		if title.startswith('HTB: '):
			htb_posts.append((title, url))

	return htb_posts
