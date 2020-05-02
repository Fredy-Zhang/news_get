import requests
from time import sleep

CLIENT_ID = "nnhQAF0e5cmr4A"
CLIENT_SECRET = "vCAgW6docqOH8a2dlhVEatpF1tk"
USER_AGENT = "Python automatic replybot v2.0 (by /u/GoldenSights )"
USERNAME = "fredyzhang"
PASSWORD = "zhang0926"

def login(username, password):
    headers = {"User-Agent": USER_AGENT}
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "password", "username": username, "password": password}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth,
            data=post_data, headers=headers)
    return response.json()

token = login(USERNAME, PASSWORD)
print(token)

def worldnews(token):
    subreddit = "worldnews"
    url = "https://oauth.reddit.com/r/{}".format(subreddit)

    headers = {"Authorization": "bearer {}".format(token['access_token']),
            "User-Agent": USER_AGENT}

    response = requests.get(url, headers=headers)
    
    return response.json()

# aresult = worldnews(token)
# for story in result['data']['children']:
#    print(story['data']['title'])

def get_links(subreddit, token, n_pages=5):
    stories = []
    after = None
    for page_number in range(n_pages):
        headers = {"Authorization": "bearer {}".format(token['access_token']),
                "User-Agent": USER_AGENT}
        url = "https://oauth.reddit.com/r/{}?limit=100".format(subreddit)
        if after:
            url += "&after={}".format(after)
        response = requests.get(url, headers=headers)
        result = response.json()
        after = result['data']['after']
        sleep(2)
        stories.extend([(story['data']['title'], story['data']['url'],
            story['data']['score'])
            for story in result['data']['children']])
    return stories

stories = get_links("worldnews", token)


import os
# data_folder = os.path.join(os.path.expanduser("/home/pi/fredy/projects/news_get/"), "Data", "websites", "raw")
data_folder = "Data/websites/raw/"
import hashlib
number_errors = 0
num = 0

for title, url, score in stories:
    output_filename = hashlib.md5(url.encode()).hexdigest()
    fullpath = os.path.join(data_folder, output_filename + ".txt")
    if number_errors > 50:
        print("Too much errors, stop!")
        break
    try:
        response = requests.get(url, timeout=1)
        print("No. ", num, "Url: ", url)
        data = response.text
        num += 1
        with open(fullpath, 'w') as outf:
            outf.write(data)
    except Exception as e:
        number_errors += 1
        print(e)

