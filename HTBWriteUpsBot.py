#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__    = 'Sam Freeside (@snovvcrash)'
__email__     = 'snovvcrash@protonmail[.]ch'
__copyright__ = 'Copyright (C) 2019 Sam Freeside'
__license__   = 'GPL-3.0'
__date__      = '2019-07-08'
__version__   = '0.1'
__site__      = 'https://github.com/snovvcrash/htb-write-ups-bot'
__brief__     = "Telegram bot for pillaging [@ippsec](https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA)'s and [@0xdf](https://0xdf.gitlab.io/)'s HackTheBox write-ups"

import os
from datetime import datetime

import telebot as tb

from author_ippsec.auth import get_youtube
from author_ippsec.utils import extract_htb_videos
from author_0xdf.utils import extract_htb_posts

NEWLINE = '\n'

TG_TOKEN = ''

if TG_TOKEN:
	from telebot import apihelper
	bot = tb.TeleBot(TG_TOKEN)
	apihelper.proxy = {
		'http': 'socks4://IP:PORT',
		'https': 'socks4://IP:PORT'
	}  # TOR
else:
	bot = tb.TeleBot(os.environ.get('TG_TOKEN'))


@bot.message_handler(commands=['start'])
def handle_start(message):
	box_by_name = tb.types.KeyboardButton('Select box by name')
	latest_box = tb.types.KeyboardButton('Latest box')

	markup = tb.types.ReplyKeyboardMarkup()
	markup.row(box_by_name)
	markup.row(latest_box)

	msg = bot.send_message(message.chat.id, 'Make your choice', reply_markup=markup)
	bot.register_next_step_handler(msg, latest_or_by_name)


@bot.message_handler(commands=['about'])
def handle_about(message):
	bot.send_message(
		message.chat.id,
		f'{__brief__}\n(by [{__author__[14:-1]}]({__site__.rsplit("/", 2)[0]}))',
		parse_mode='Markdown'
	)


def latest_or_by_name(message):
	youtube = get_youtube()

	if message.text == 'Select box by name':
		htb_videos = extract_htb_videos(youtube, count=31337)

		boxes = []
		for title, _, _ in htb_videos:
			boxes.append(tb.types.KeyboardButton(title[13:]))  # 13 is len('HackTheBox - ')

		markup = tb.types.ReplyKeyboardMarkup()
		for box in boxes:
			markup.row(box)

		msg = bot.send_message(message.chat.id, 'Select box by name', reply_markup=markup)
		bot.register_next_step_handler(msg, lambda m: get_box_by_name(m, htb_videos))

	elif message.text == 'Latest box':  # get_latest_box()
		htb_videos = extract_htb_videos(youtube, count=1)
		title, url, description = htb_videos[0]
		description = _add_timecodes_to_description(description, url)
		posts_by_0xdf = _get_0xdf_posts(title[13:])

		send_back = f"""\
			ippsec: [{title}]({url})
			{NEWLINE.join(posts_by_0xdf)}

			{NEWLINE.join(description)}\
		""".replace('\t', '')

		bot.send_message(message.chat.id, send_back, parse_mode='Markdown')
		msg = bot.send_message(message.chat.id, 'Happy hacking! Run /start to start over')


def get_box_by_name(message, htb_videos):
	box_name = message.text

	for title, url, description in htb_videos:
		if title[13:].lower().startswith(box_name.lower()):
			if description:
				description = _add_timecodes_to_description(description, url)
				posts_by_0xdf = _get_0xdf_posts(box_name)

				send_back = f"""\
					ippsec: [{title}]({url})
					{NEWLINE.join(posts_by_0xdf)}

					{NEWLINE.join(description)}\
				""".replace('\t', '')

			else:
				send_back = f'{title}\n{url}'

			bot.send_message(message.chat.id, send_back, parse_mode='Markdown')

	msg = bot.send_message(message.chat.id, 'Happy hacking! Run /start to start over')


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


def main():
	bot.polling(none_stop=True, interval=0, timeout=20)


if __name__ == '__main__':
	main()
