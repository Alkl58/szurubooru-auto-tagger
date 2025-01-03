import sys
import json
import time
import argparse
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

from config import SZURU_ENDPOINT, SZURU_USERNAME, SZURU_PASSWORD
from config import SLEEP_TIME, ALLOW_POSSIBLE_MATCH

HTTP_AUTH = HTTPBasicAuth(SZURU_USERNAME, SZURU_PASSWORD)

def get_booru_post_info(post_number: int) -> tuple[str, str]:
    """
    Get required post information from the booru.
    We need to know the content url, so that IQDB can download the picture
    and we need the version of the post, as it's required for updating the tags.

    :param post_number: The post number
    :return contentUrl, version
    """
    booru_api_url = "{}/api/post/{}".format(SZURU_ENDPOINT, post_number)
    response_json = requests.get(booru_api_url, headers={'Accept':'application/json'}, auth=HTTP_AUTH).json()
    return response_json['contentUrl'], response_json['version']

def update_booru_post_info(post_number: int, post_version: int, post_tags: list) -> int:
    """
    Update the booru post with new tags.
    See: https://github.com/rr-/szurubooru/blob/master/doc/API.md#updating-post

    :param post_number: The post number
    :param post_version: The post version
    :param post_tags: The post tags
    :return contentUrl, version
    """
    payload = json.dumps({ "version": post_version, "tags": post_tags })
    headers = {'Accept':'application/json', 'Content-Type': 'application/json'}
    booru_api_url = "{}/api/post/{}".format(SZURU_ENDPOINT, post_number)
    requests.put(booru_api_url, headers=headers, auth=HTTP_AUTH, data=payload)

def query_iqdb(content_url: str) -> str:
    """
    Query IQDB with our image

    :param content_url: The image url accessible from the internet
    :return html_response
    """
    iqdb_url = "https://iqdb.org/?url={}/{}".format(SZURU_ENDPOINT, content_url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    html_response = requests.get(iqdb_url, headers=headers).text
    return html_response

def parse_iqdb(html_doc: str) -> list:
    """
    Parse IQDB response

    :param html_doc: The html document returned by IQDB
    :return tags: A string with all containing tags seperated by space
    """
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Select first div with pages class
    div = soup.select_one('#pages')
    # Get all tables
    tables = div.find_all("table")

    # Parse tables
    for table in tables:
        # Get table header
        header = [th.text.strip() for th in table.find_all('th')][0]
        # Skip our own image
        if header == 'Your image': 
            continue
        if header == 'Best match' or (header == 'Possible match' and ALLOW_POSSIBLE_MATCH):
            # Get image alt text
            alt_text = table.find_all('img')[0]['alt']
            return alt_text.split('Tags:')[1].strip().split()
        
    # No tags found
    return []

if not SZURU_ENDPOINT:
    sys.exit("Please specify your szurubooru endpoint in the config.py file!")

if not SZURU_USERNAME:
    sys.exit("Please specify your szurubooru username in the config.py file!")

if not SZURU_PASSWORD:
    sys.exit("Please specify your szurubooru password in the config.py file!")

parser = argparse.ArgumentParser(description='Commandline usage of AutoTagger')
parser.add_argument("--post", required=True, help="Required - Post number to tag, e.g. 69")
parser.add_argument("--postend", help="Optional - When set, it will tag all posts between the 'post' number and 'postend' number.")
args = parser.parse_args()

start = int(args.post)
end = start
if args.postend is not None:
    end = int(args.postend)

if start > end:
    start, end = end, start

for post_number in range(start, end + 1):
    try:
        content_url, post_version = get_booru_post_info(post_number)
        iqdb_html = query_iqdb(content_url)
        tags = parse_iqdb(iqdb_html)

        if not tags:
            print("Post {} - No tags found!".format(post_number))
            continue

        update_booru_post_info(post_number, post_version, tags)
        print("Post {} Tagged Successfully".format(post_number))

        # Wait before querying IQDB again
        if post_number < end:
            time.sleep(SLEEP_TIME)
    except Exception as error:
        print("Error occured: ", error)
