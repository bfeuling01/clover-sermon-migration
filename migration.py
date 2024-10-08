#!/usr/bin/env python3

import requests, sys
from bs4 import BeautifulSoup

# Define API key and SA host
# To get the Sermon Audio API KEY:
# https://legacy.sermonaudio.com/new_details.asp?ID=26017
API_KEY = "<INSERT SERMON AUDIO API KEY"
SA_HOST = "https://api.sermonaudio.com"
# https://api.sermonaudio.com/v2/docs#/model-Broadcaster
BROADCASTERID = "<INSERT SERMON AUDIO BROADCASTER ID>"
# Example: www.your_church_website.com/media
SOURCE_URL = "<INSERT URL WHERE VIDEOS CURRENTLY ARE>"


# Function to scrape media URLs from the source URL
def scrape_media_urls():
    url = f'{SOURCE_URL}/media/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extracting media URLs from the source URL
    media_urls = {SOURCE_URL + a['href'] for a in soup.find_all('a', href=True) if 'media/' in a['href']}
    return media_urls

# Scrape media URLs and store them in MEDIA_URLS
MEDIA_URLS = scrape_media_urls()
C_URLS = []
for media_url in MEDIA_URLS:
    response = requests.get(media_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    media_player_containers = soup.find_all('div', class_='media-player-container')
    for container in media_player_containers:
        data_id = container.get('data-id')
        if data_id:
            # Constructing the URL for the media player
            C_URLS.append(f"https://mediaplayer.cloversites.com/players/{data_id}?draft=0")

# Initialize an empty list to store responses
all_sermons = []

# Loop through each URL to fetch sermon data
for URL in C_URLS:
    print(f"Fetching data from {URL}")
    response = requests.get(URL).json()
    all_sermons.append(response)  # Append each response to the list

# Loop through each sermon to process and upload
# This will need to be updated based on the metadata that is coming
# from your videos. It should be the same across all Clover hosting
# but it might be somewhat customized to your instance
for sermon in all_sermons:
    for s in sermon['media']:
        try:
            download_url = s['download_url']
            TITLE = s['title']
            # Extracting Bible reference from the title
            BIBLE = s['title'].split(' - ')[1] if ' - ' in s['title'] else s['title']
            SHORTITLE = s['title'].split(' - ')[0]
            SUBTITLE = TITLE
            # Formatting the preach date
            PREACH_DATE = f"{s['date_string'].split('/')[2]}-{s['date_string'].split('/')[0]}-{s['date_string'].split('/')[1]}"
            PUBLISH_DATE = PREACH_DATE
            SPEAKER = s['speaker']
            LANG = "en"
            EVENT_TYPE = "Sunday Service"
            KEYWORDS = s['series']
            MEDIA_PATH = f"{TITLE}.mp4"
            # Downloading the media file
            with open(MEDIA_PATH, 'wb') as f:
                f.write(requests.get(download_url).content)
            # Preparing JSON for sermon upload
            JSON = {
                "fullTitle": TITLE,
                "displayTitle": BIBLE,
                "subtitle": BIBLE,
                "speakerName": SPEAKER,
                "preachDate": PREACH_DATE,
                "publishDate": PUBLISH_DATE,
                "bibleText": BIBLE,
                "moreInfoText": TITLE,
                "eventType": EVENT_TYPE,
                "languageCode": LANG,
                "keywords": KEYWORDS,
                "acceptCopyright": "true"
            }
            print(f'''JSON Check
{JSON}
''')
            # Sending JSON to get sermon ID
            headers = {'Content-Type': 'application/json','X-API-Key': API_KEY}
            response = requests.post(f"{SA_HOST}/v2/node/sermons", headers=headers, json=JSON)
            UPLOAD_RESPONSE = response.json()
            SERMONID = UPLOAD_RESPONSE['sermonID']
            # Preparing JSON for media upload
            JSON = {
                "sermonID": SERMONID,
                "uploadType": "original"
            }
            response = requests.post(f"{SA_HOST}/v2/media", headers=headers, json=JSON)
            UPLOAD_RESPONSE = response.json()
            URL = UPLOAD_RESPONSE['uploadURL']
            print(f'Uploading {TITLE} {SERMONID} to {URL}')
            # Uploading the media file
            with open(MEDIA_PATH, 'rb') as file:
                response = requests.post(URL, headers=headers, data=file.read())
            print(response.text)
        except:
            print("EXCEPTION: ")
            print(sys.exc_info())
