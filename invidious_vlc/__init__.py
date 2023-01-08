"""
Play a YouTube video from Invidious in VLC. Requires vlc in PATH.

Usage: invidious-vlc [search query]
"""


import sys
import re
import subprocess
import requests
import pyquery
from urllib.parse import quote


if len(sys.argv) != 2:
        print(__doc__)
        exit()

query = sys.argv[1]
search_response = requests.get('https://yewtu.be/search?q=' + quote(query)).text
search_document = pyquery.PyQuery(search_response)

video_links = search_document.find('a[href*="/watch"]')
video_titles = video_links.text().split('\n')
video_urls = [a.get('href') for a in video_links]

for i, (title, url) in enumerate(zip(video_titles, video_urls)):
        print('[{:02d}]   {}'.format(i, title, url))


selection = int(input('Enter selection: '))
video_id = video_urls[selection].split('=')[-1]


response = subprocess.getoutput(f'''
curl -v 'https://yewtu.be/latest_version?id={video_id}&itag=22'   -H 'authority: yewtu.be'   -H 'sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"'   -H 'sec-ch-ua-mobile: ?0'   -H 'upgrade-insecure-requests: 1'   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'   -H 'sec-fetch-site: none'   -H 'sec-fetch-mode: navigate'   -H 'sec-fetch-user: ?1'   -H 'sec-fetch-dest: document'   -H 'accept-language: en-GB,en;q=0.9,en-US;q=0.8'   --compressed''')

video_mri = re.findall(r'location: (.+)\n', response)[0]

subprocess.getoutput(f'vlc.exe \'{video_mri}\'')
