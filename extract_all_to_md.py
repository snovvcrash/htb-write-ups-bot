#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from datetime import datetime

from author_ippsec.auth import get_youtube
from author_ippsec.utils import extract_htb_videos
from author_0xdf.utils import extract_htb_posts

NEWLINES = '\n\n'


def _add_timecodes_to_description(description, url):
	description_with_timecodes = []

	for line in description.split('\n'):
		timecode_index = line.find(' -', 1)
		timecode, remaining_part = line[:timecode_index], line[timecode_index+1:]

		try:
			if len(timecode) == 5:  # MM:SS
				timestamp = datetime.strptime(timecode, '%M:%S')
			elif len(timecode) == 8:  # HH:MM:SS
				timestamp = datetime.strptime(timecode, '%H:%M:%S')
		except ValueError:
			description_with_timecodes.append(timecode + remaining_part)
		else:
			url_with_timecode_md = f'[{timecode}]({url}&t={int((timestamp - datetime(1900, 1, 1)).total_seconds())})'
			description_with_timecodes.append(url_with_timecode_md + remaining_part)

	return description_with_timecodes


def _get_0xdf_posts(box_name):
	htb_posts = extract_htb_posts()

	post_matches = []
	for title, url in htb_posts:
		if box_name.lower() in title[5:].lower():  # 5 is len('HTB: ')
			post_md = f'0xdf: [{title}]({url})'
			post_matches.append(post_md)

	return post_matches


if __name__ == '__main__':
	youtube = get_youtube()
	htb_videos = extract_htb_videos(youtube, count=31337)

	extracted = []
	for title, url, description in htb_videos:
		if description:
			description = _add_timecodes_to_description(description, url)
			posts_by_0xdf = _get_0xdf_posts(title[13:])  # 13 is len('HackTheBox - ')

			item = f"""\
				ippsec: [{title}]({url})

				{NEWLINES.join(posts_by_0xdf)}

				{NEWLINES.join(description)}\
			""".replace('\t', '')

		else:
			item = f'{title}\n{url}'

		extracted.append(item)

	with open(f"write-ups-md/{time.strftime('%Y-%m-%d', time.localtime())}.md", 'w', encoding='utf-8') as f:
		f.write('\n\n-----------------------------------------------------------\n\n'.join(extracted))
