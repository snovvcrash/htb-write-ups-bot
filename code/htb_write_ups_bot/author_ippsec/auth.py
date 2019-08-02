#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from apiclient.discovery import build

from htb_write_ups_bot.author_ippsec.settings import YT_API_SERVICE_NAME
from htb_write_ups_bot.author_ippsec.settings import YT_API_VERSION


def _get_youtube_helper(developer_key):
	return build(
		serviceName=YT_API_SERVICE_NAME,
		version=YT_API_VERSION,
		developerKey=developer_key
	)


def get_youtube():
	return _get_youtube_helper(os.getenv('YT_DEVELOPER_KEY'))
