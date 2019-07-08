htb-write-ups-bot
==========

[![htb-write-ups-bot-version.svg](https://img.shields.io/badge/ver-0.1-red.svg)](https://github.com/snovvcrash/htb-write-ups-bot)
[![python-version.svg](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads)
[![license.svg](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/snovvcrash/htb-write-ups-bot/master/LICENSE)
[![built-with-love.svg](https://img.shields.io/badge/built%20with-%F0%9F%92%97%F0%9F%92%97%F0%9F%92%97-lightgrey.svg)](https://emojipedia.org/growing-heart)

<img src="HTBWriteUpsBot.png" alt="banner.png" align="left" />

**htb-write-ups-bot** — is a proof-of-concept [Telegram bot](https://t.me/HTBWriteUpsBot) that allows you to search through retired [HackTheBox](https://www.hackthebox.eu/ "Hack The Box :: Penetration Testing Labs") machines for write-ups. It is based on the official YouTube API module for Python (for looting the [@ippsec](https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA "IppSec - YouTube")'s YT blog) and bs4 HTML parsing module (for looting the [@0xdf](https://0xdf.gitlab.io/ "0xdf hacks stuff")'s blog).

Inspired by [get_ippsec_details.py](https://gist.github.com/sminez/571bd7bafb1b88630b85c85a0cd66e3a "Find examples of pen testing methods and tools in videos by Ippsec (as of 26th June 2019)").

## Markdown

[Here](write-ups-md) you can find the Markdown version of all available write-ups with timecodes for the specified date.

Or you can generate such report yourself by running (with `YT_DEVELOPER_KEY` set in `author_ippsec/config.py`):

```
$ python3 -m pip install google-api-python-client requests bs4
$ python3 extract_all_to_md.py
```
