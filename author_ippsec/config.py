#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

YT_DEVELOPER_KEY = ''

if not YT_DEVELOPER_KEY:
	YT_DEVELOPER_KEY = os.environ.get('YT_DEVELOPER_KEY')
