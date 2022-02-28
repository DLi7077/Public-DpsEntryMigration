import urllib.request
import json
import urllib
# https://www.semicolonworld.com/question/60204/retrieve-youtube-video-title-using-api-python
#change to yours VideoID or change url inparams

params = {"format": "json", "url": "https://www.youtube.com/watch?v=H-yAJrOVymg"}
url = "https://www.youtube.com/oembed"
query_string = urllib.parse.urlencode(params)
url = url + "?" + query_string

with urllib.request.urlopen(url) as response:
    response_text = response.read()
    data = json.loads(response_text.decode())
    print(data["title"])
