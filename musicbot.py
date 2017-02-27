import requests
import youtube_dl
from bs4 import BeautifulSoup
from slackclient import SlackClient
import os
import time


BOT_TOKEN = 'xoxb-147514957574-h3YIvOojbRMPAb58yGcTKnVm'
slack_client = SlackClient(BOT_TOKEN)


def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        print channels_call['channels']
        return channels_call['channels']
    return None

def upload_file(file_dest,name):
           slack_client.api_call(
               "files.upload",
               file=file_dest,
               token='xoxp-128968699074-129647659430-147244611222-59913fba9940bf7e494cf29f7aa5d1b1',
               filename=name,
               channels='C3T1MU293'
            )


def search(text):
    url = 'https://www.youtube.com'
    r = requests.get(url + '/results', params={'search_query': text})
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find('a', {'rel': 'spf-prefetch'})
    full_title, video_url  = tag.text, url + tag['href']
    print "parsed the string"
    return full_title, video_url


def download(full_title, video_url):
    try:
        author, title = full_title.split('-')
        title = title.strip()
        author = author.strip()
    except:
        title = full_title

    ydl_opts = {
        'outtmpl': 'music/{}.%(ext)s'.format(title),
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        print "downloaded the file"

        return title

'''    music_dict = {
        'audio': open('music/{}.mp3'.format(title), 'rb'),
        'title': title,
}
    try:
        music_dict['performer'] = author
    except:
        pass

    print "music_dict created"
    return music_dict
'''

if not os.path.exists('music'):
    os.makedirs('music')


if slack_client.rtm_connect():
# connect to a Slack RTM websocket. this module helps in downloading the file. gets the url of the file.
        while True:
                a= slack_client.rtm_read()
                if a:
                    print a
                    if (a[0]['type']=='message'):
                        song_name = a[0]['text']
                        print song_name
                        full_title, video_url = search(song_name)
                        title = download(full_title,video_url)
                        name = full_title + ".mp3"
                        print "upload left"
                        #file_q = {'file': ('{}.mp3'.format(title), open('music/{}.mp3'.format(title), 'rb'))}
                        #upload_file(file_q,name)




                time.sleep(1)
