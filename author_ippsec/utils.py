#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from apiclient.discovery import build
from apiclient.errors import HttpError

CHANNEL_ID = 'UCa6eh7gCkpPo5XXUDfygQQA'

MAX_PER_PAGE = 50


def _gen_playlistitems_list_request(youtube, playlist_id, page_token, max_results):
	return youtube.playlistItems().list(
		part='snippet',
		playlistId=playlist_id,
		pageToken=page_token,
		maxResults=max_results
	)


def _get_playlist_id(youtube, channel_id, playlist_name):
	channel = youtube.channels().list(part='contentDetails', id=channel_id)
	return channel.execute()['items'][0]['contentDetails']['relatedPlaylists'][playlist_name]


def _get_playlistitems(youtube, playlist_id, count):
	playlistitems = []

	try:
		num_of_results = count if count < MAX_PER_PAGE else MAX_PER_PAGE
		playlistitems_list_request = _gen_playlistitems_list_request(youtube, playlist_id, None, num_of_results)
		playlistitems_list_response = playlistitems_list_request.execute()
		playlistitems_list_response_items = playlistitems_list_response['items']
		playlistitems += playlistitems_list_response_items
		count -= len(playlistitems_list_response_items)

		while 'nextPageToken' in playlistitems_list_response and count:
			next_page_token = playlistitems_list_response['nextPageToken']
			num_of_results = count if count < MAX_PER_PAGE else MAX_PER_PAGE
			playlistitems_list_request = _gen_playlistitems_list_request(youtube, playlist_id, next_page_token, num_of_results)
			playlistitems_list_response = playlistitems_list_request.execute()
			playlistitems_list_response_items = playlistitems_list_response['items']
			playlistitems += playlistitems_list_response_items
			count -= len(playlistitems_list_response_items)

	except HttpError as e:
		print(f'[-] Debug: {e.content}, {e.resp.status}, {next_page_token}')
		return None

	return playlistitems


def _get_urls_titles_and_descriptions(youtube, count, channel_id=CHANNEL_ID, playlist_name='uploads'):
	playlist_id = _get_playlist_id(youtube, channel_id, playlist_name)
	playlistitems = _get_playlistitems(youtube, playlist_id, count)

	result = []
	for item in playlistitems:
		snippet = item['snippet']
		title = snippet['title']
		url = f"https://youtube.com/watch?v={snippet['resourceId']['videoId']}"
		description = snippet['description']
		result.append((title, url, description))

	return result


def extract_htb_videos(youtube, count):
	htb_videos = []
	regex = re.compile(r'^\d\d:\d\d.*?$', re.MULTILINE)

	result = _get_urls_titles_and_descriptions(youtube, count)
	for title, url, description in result:
		if title.startswith('HackTheBox - '):
			description = regex.findall(description)
			description = '\n'.join(description)
			htb_videos.append((title, url, description))

	return htb_videos
