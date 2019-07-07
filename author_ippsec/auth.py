#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from apiclient.discovery import build

from author_ippsec.config import YT_DEVELOPER_KEY

YT_API_SERVICE_NAME = 'youtube'
YT_API_VERSION = 'v3'


def _get_youtube_helper(developer_key):
	return build(
		serviceName=YT_API_SERVICE_NAME,
		version=YT_API_VERSION,
		developerKey=developer_key
	)


def get_youtube():
	return _get_youtube_helper(YT_DEVELOPER_KEY)
