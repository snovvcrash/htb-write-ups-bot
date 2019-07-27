htb-write-ups-bot
==========

<img src="https://user-images.githubusercontent.com/23141800/60811057-2b4b4e80-a197-11e9-8a17-4df4c758b16f.png" alt="banner.png" align="left" />

**htb-write-ups-bot** — is a proof-of-concept [Telegram bot](https://t.me/HTBWriteUpsBot) that allows you to search through retired [HackTheBox](https://www.hackthebox.eu/ "Hack The Box :: Penetration Testing Labs") machines for write-ups. It is based on the official YouTube API module for Python (for looting the [@ippsec](https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA "IppSec - YouTube")'s YT blog) and bs4 HTML parsing module (for looting the [@0xdf](https://0xdf.gitlab.io/ "0xdf hacks stuff")'s blog).

Inspired by [get_ippsec_details.py](https://gist.github.com/sminez/571bd7bafb1b88630b85c85a0cd66e3a "Find examples of pen testing methods and tools in videos by Ippsec (as of 26th June 2019)").

## Markdown

[Here](Markdown) you can find the Markdown version of all available write-ups with timecodes for the specified date.

Or you can generate such report yourself by running `extract_all_to_md.py` with `YT_DEVELOPER_KEY` set in `author_ippsec/config.py`.

Install dependencies:

```
$ pip3 install google-api-python-client requests bs4
```

Generate report:

```
$ python3 extract_all_to_md.py
```

## Demo

![ios-demo.gif](ios-demo.gif)
